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
        
        # Validate model
        supported_models = ["chatterbox-multilingual", "chatterbox-turbo", "chatterbox", "tts-1", "tts-1-hd"]
        if request.model not in supported_models:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported model: {request.model}. Supported: {', '.join(supported_models)}"
            )
        
        # Generate audio
        logger.info(f"Generating speech: text_len={len(request.input)}, lang={request.language}, format={request.response_format}")
        
        audio = await service.generate_audio(
            text=request.input,
            language=request.language,
            audio_prompt_path=request.audio_prompt,
            temperature=request.temperature,
            cfg_weight=request.cfg_weight,
            exaggeration=request.exaggeration,
        )
        
        # Convert to requested format
        audio_bytes = service.convert_audio_format(
            audio,
            format=request.response_format,
            sample_rate=service.model.sr
        )
        
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
            }
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
        service = await get_tts_service()
        languages = service.get_supported_languages()
        
        # Create voice info for the multilingual model
        # The model uses voice cloning, so we list supported languages
        voices = [
            VoiceInfo(
                id="default",
                name="Default Multilingual Voice",
                languages=list(languages.keys())
            )
        ]
        
        return VoicesResponse(voices=voices)
        
    except Exception as e:
        logger.error(f"Error listing voices: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/models")
async def list_models():
    """
    List available models
    
    Returns information about available TTS models.
    """
    return {
        "object": "list",
        "data": [
            {
                "id": "chatterbox-multilingual",
                "object": "model",
                "created": 1704067200,
                "owned_by": "resemble-ai",
                "description": "Multilingual TTS model supporting 23+ languages"
            },
            {
                "id": "tts-1",
                "object": "model",
                "created": 1704067200,
                "owned_by": "openai-compatible",
                "description": "Alias for chatterbox-multilingual"
            },
            {
                "id": "tts-1-hd",
                "object": "model",
                "created": 1704067200,
                "owned_by": "openai-compatible",
                "description": "Alias for chatterbox-multilingual"
            }
        ]
    }
