"""OpenAI-compatible API endpoints"""

import logging
from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, StreamingResponse
from api.schemas.openai import (
    OpenAISpeechRequest,
    VoiceInfo,
    VoicesResponse,
)
from api.services.tts_service import get_tts_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["OpenAI Compatible"])


@router.post("/audio/speech")
async def create_speech(request: OpenAISpeechRequest):
    """
    OpenAI-compatible text-to-speech endpoint

    Generates audio from text using the Chatterbox multilingual model.
    Compatible with OpenAI's speech API.
    """
    try:
        # Get TTS service
        service = await get_tts_service()

        # Extract language from model name if specified (e.g., chatterbox-multilingual-es)
        # This allows OpenWebUI to select language via model name instead of language parameter
        model_name = request.model
        language_override = None

        # Check if model name has language suffix
        if "-" in model_name:
            parts = model_name.split("-")
            potential_lang = parts[-1]
            # Check if it's a valid language code
            supported_langs = service.get_supported_languages()
            if potential_lang in supported_langs:
                language_override = potential_lang
                # Extract base model name (remove language suffix)
                model_name = "-".join(parts[:-1])
                logger.info(
                    f"Detected language '{language_override}' from model name '{request.model}'"
                )

        # Validate base model
        supported_models = [
            "chatterbox-multilingual",
            "chatterbox-turbo",
            "chatterbox",
            "tts-1",
            "tts-1-hd",
        ]
        if model_name not in supported_models:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported model: {request.model}. Supported: {', '.join(supported_models)} or with language suffix (e.g., chatterbox-multilingual-es)",
            )

        # Use language from model name if detected, otherwise use request language
        final_language = language_override if language_override else request.language

        # SANITIZATION: Add punctuation to prevent run-on/hallucination
        sanitized_input = request.input.strip()
        if sanitized_input and not sanitized_input[-1] in ".!?,:;" :
            sanitized_input += "."
            logger.info(f"Sanitized input: '{request.input}' -> '{sanitized_input}'")


        # Resolve voice name to audio file path
        # Priority: audio_prompt (explicit file path) > voice (name-based resolution)
        audio_prompt_path = request.audio_prompt

        if not audio_prompt_path and request.voice and request.voice != "default":
            # Import voice mapper here to avoid circular imports
            from api.services.voice_mapper import get_voice_mapper

            voice_mapper = get_voice_mapper()
            resolved_path = voice_mapper.get_voice_path(request.voice)

            if resolved_path:
                audio_prompt_path = str(resolved_path)
                logger.info(
                    f"Resolved voice '{request.voice}' to '{resolved_path.name}'"
                )
            else:
                available_voices = voice_mapper.list_voice_names()
                raise HTTPException(
                    status_code=400,
                    detail=f"Voice '{request.voice}' not found. Available voices: {', '.join(available_voices[:10])}{' and more...' if len(available_voices) > 10 else ''}",
                )

        # Generate audio
        logger.info(
            f"Generating speech: text_len={len(request.input)}, lang={final_language}, voice={request.voice}, format={request.response_format}, model={request.model}"
        )

        audio = await service.generate_audio(
            text=sanitized_input,
            language=final_language,
            audio_prompt_path=audio_prompt_path,
            temperature=request.temperature,
            cfg_weight=request.cfg_weight,
            exaggeration=request.exaggeration,
        )

        # Convert to requested format
        audio_bytes = service.convert_audio_format(
            audio, format=request.response_format, sample_rate=service.model.sr
        )

        # Post-process: Trim silence/artifacts (Pydub)
        try:
            from pydub import AudioSegment
            from pydub.silence import split_on_silence
            import io
            
            # Load generated audio (usually wav container from service)
            # Note: service.convert_audio_format likely returns wav/mp3 bytes
            seg = AudioSegment.from_file(io.BytesIO(audio_bytes))
            
            # Split on silence to remove trailing artifacts
            # min_silence_len=200ms, thresh=-40dB
            chunks = split_on_silence(seg, min_silence_len=200, silence_thresh=-40)
            if chunks:
                logger.info(f"Silence trimming: kept {len(chunks)} chunks")
                cleaned_seg = chunks[0]
                # Heuristic: If text is short (<30 chars), likely single word/phrase.
                # If multiple chunks found, it's likely repetition/hallucination.
                # Only keep adjacent chunks if they are close? Or just keep first?
                # For this use case (game assets), keeping first chunk is safest for short text.
                should_keep_all = len(request.input) > 50
                if should_keep_all:
                    for c in chunks[1:]:
                        cleaned_seg += c
                else:
                    logger.info(f"Short text detected ({len(request.input)} chars). Keeping only first chunk of {len(chunks)}.")
                
                out_io = io.BytesIO()
                # Export matching the requested format
                fmt = request.response_format if request.response_format != 'pcm' else 'wav'
                cleaned_seg.export(out_io, format=fmt)
                audio_bytes = out_io.getvalue()
            else:
                logger.warning("Silence trimming found no audio! Keeping original.")
        except Exception as e:
            logger.warning(f"Silence trimming failed: {e}")

        # Set content type
        content_types = {
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "opus": "audio/opus",
            "flac": "audio/flac",
            "pcm": "audio/pcm",
            "aac": "audio/aac",
        }
        content_type = content_types.get(request.response_format, "audio/wav")

        return Response(
            content=audio_bytes,
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename=speech.{request.response_format}"
            },
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating speech: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/audio/voices", response_model=VoicesResponse)
async def list_voices():
    """
    List available voices and languages

    Returns information about supported voices and languages
    for the multilingual model.
    """
    try:
        from api.services.voice_mapper import get_voice_mapper

        service = await get_tts_service()
        languages = service.get_supported_languages()
        voice_mapper = get_voice_mapper()

        # Get all discovered voice samples
        discovered_voices = voice_mapper.list_voice_names()

        # Create voice info for each discovered voice
        # All voices support all languages via voice cloning
        voices = []

        # Add default voice (no cloning)
        voices.append(
            VoiceInfo(
                id="default",
                name="Default (No Voice Cloning)",
                languages=list(languages.keys()),
            )
        )

        # Add discovered voice samples
        for voice_name in discovered_voices:
            voices.append(
                VoiceInfo(
                    id=voice_name,
                    name=voice_name.capitalize(),
                    languages=list(languages.keys()),
                )
            )

        return VoicesResponse(voices=voices)

    except Exception as e:
        logger.error(f"Error listing voices: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/models")
async def list_models():
    """
    List available models

    Returns information about available TTS models, including
    language-specific variants (e.g., chatterbox-multilingual-es).
    """
    try:
        service = await get_tts_service()
        supported_langs = service.get_supported_languages()

        # Base models
        models = [
            {
                "id": "chatterbox-multilingual",
                "object": "model",
                "created": 1704067200,
                "owned_by": "resemble-ai",
                "description": "Multilingual TTS model supporting 23+ languages",
            },
            {
                "id": "tts-1",
                "object": "model",
                "created": 1704067200,
                "owned_by": "openai-compatible",
                "description": "Alias for chatterbox-multilingual",
            },
            {
                "id": "tts-1-hd",
                "object": "model",
                "created": 1704067200,
                "owned_by": "openai-compatible",
                "description": "Alias for chatterbox-multilingual",
            },
        ]

        # Add language-specific variants
        for lang_code, lang_name in supported_langs.items():
            models.append(
                {
                    "id": f"chatterbox-multilingual-{lang_code}",
                    "object": "model",
                    "created": 1704067200,
                    "owned_by": "resemble-ai",
                    "description": f"Multilingual TTS model (auto-set to {lang_name})",
                }
            )

        return {"object": "list", "data": models}
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
