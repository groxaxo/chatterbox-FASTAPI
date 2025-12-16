"""TTS Service for managing model and generating audio"""
import io
import logging
from pathlib import Path
from typing import Optional, AsyncGenerator
import torch
import torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS, SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)


class TTSService:
    """Service for managing TTS model and generating audio"""
    
    def __init__(self, device: str = None):
        """Initialize TTS service
        
        Args:
            device: Device to run model on (cuda, cpu, mps). If None, auto-detect.
        """
        if device is None:
            if torch.cuda.is_available():
                device = "cuda"
            elif torch.backends.mps.is_available():
                device = "mps"
            else:
                device = "cpu"
        
        self.device = device
        self.model: Optional[ChatterboxMultilingualTTS] = None
        self.model_name = "chatterbox-multilingual"
        logger.info(f"Initializing TTS service on device: {device}")
        
    async def initialize(self):
        """Initialize the TTS model"""
        try:
            logger.info("Loading Chatterbox Multilingual model...")
            self.model = ChatterboxMultilingualTTS.from_pretrained(device=self.device)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def get_supported_languages(self) -> dict:
        """Get supported languages"""
        return SUPPORTED_LANGUAGES.copy()
    
    async def generate_audio(
        self,
        text: str,
        language: Optional[str] = None,
        audio_prompt_path: Optional[str] = None,
        temperature: float = 0.7,
        cfg_weight: float = 0.5,
        exaggeration: float = 0.5,
    ) -> torch.Tensor:
        """Generate audio from text
        
        Args:
            text: Input text to synthesize
            language: Language code (e.g., 'en', 'es', 'fr')
            audio_prompt_path: Path to audio file for voice cloning
            temperature: Sampling temperature
            cfg_weight: Classifier-free guidance weight
            exaggeration: Exaggeration level
            
        Returns:
            Audio tensor
        """
        if self.model is None:
            raise RuntimeError("Model not initialized")
        
        # Validate language if provided
        if language and language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language}. "
                f"Supported: {', '.join(SUPPORTED_LANGUAGES.keys())}"
            )
        
        try:
            with torch.inference_mode():
                wav = self.model.generate(
                    text=text,
                    language_id=language,
                    audio_prompt_path=audio_prompt_path,
                    temperature=temperature,
                    cfg_weight=cfg_weight,
                    exaggeration=exaggeration,
                )
            return wav
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            raise
    
    def convert_audio_format(
        self,
        audio: torch.Tensor,
        format: str,
        sample_rate: int = 24000
    ) -> bytes:
        """Convert audio tensor to specified format
        
        Args:
            audio: Audio tensor (shape: [1, samples])
            format: Output format (mp3, wav, opus, flac, pcm)
            sample_rate: Sample rate of audio
            
        Returns:
            Audio bytes in specified format
        """
        # Ensure audio is in correct shape
        if audio.dim() == 1:
            audio = audio.unsqueeze(0)
        
        # For PCM, return raw samples
        if format == "pcm":
            # Convert to 16-bit PCM
            audio_int16 = (audio * 32767).clamp(-32768, 32767).to(torch.int16)
            return audio_int16.cpu().numpy().tobytes()
        
        # For other formats, use torchaudio
        buffer = io.BytesIO()
        
        if format == "wav":
            torchaudio.save(buffer, audio.cpu(), sample_rate, format="wav")
        elif format == "flac":
            torchaudio.save(buffer, audio.cpu(), sample_rate, format="flac")
        elif format == "mp3":
            # Save as wav first, then would need ffmpeg for actual mp3
            # For now, save as wav and rename
            torchaudio.save(buffer, audio.cpu(), sample_rate, format="wav")
        elif format == "opus":
            # Opus requires special handling, save as wav for now
            torchaudio.save(buffer, audio.cpu(), sample_rate, format="wav")
        elif format == "aac":
            # AAC requires special handling, save as wav for now
            torchaudio.save(buffer, audio.cpu(), sample_rate, format="wav")
        else:
            # Default to wav
            torchaudio.save(buffer, audio.cpu(), sample_rate, format="wav")
        
        buffer.seek(0)
        return buffer.read()


# Global service instance
_service: Optional[TTSService] = None


async def get_tts_service() -> TTSService:
    """Get global TTS service instance"""
    global _service
    if _service is None:
        _service = TTSService()
        await _service.initialize()
    return _service
