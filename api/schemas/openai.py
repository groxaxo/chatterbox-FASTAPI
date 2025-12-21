"""Pydantic schemas for API requests and responses"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from api.config import DEFAULT_TEMPERATURE, DEFAULT_CFG_WEIGHT, DEFAULT_EXAGGERATION


class OpenAISpeechRequest(BaseModel):
    """OpenAI-compatible speech request schema"""

    model: str = Field(
        default="chatterbox-multilingual",
        description="The model to use for generation. Supported: chatterbox-multilingual, chatterbox-turbo, chatterbox",
    )
    input: str = Field(..., description="The text to generate audio for")
    voice: str = Field(
        default="default",
        description="Voice name to use (e.g., 'aimee', 'facu', 'brenda'). "
        "Automatically resolved from voice_samples/ directory. "
        "Use 'default' for base model voice without cloning.",
    )
    response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = Field(
        default="mp3", description="The format to return audio in"
    )
    speed: float = Field(
        default=1.0,
        ge=0.25,
        le=4.0,
        description="The speed of the generated audio (0.25 to 4.0)",
    )
    language: Optional[str] = Field(
        default=None,
        description="Language code for multilingual model (e.g., 'en', 'es', 'fr', 'zh')",
    )
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        ge=0.0,
        le=2.0,
        description="Sampling temperature (0.0 to 2.0)",
    )
    cfg_weight: float = Field(
        default=DEFAULT_CFG_WEIGHT,
        ge=0.0,
        le=1.0,
        description="Classifier-free guidance weight (not supported in turbo)",
    )
    exaggeration: float = Field(
        default=DEFAULT_EXAGGERATION,
        ge=0.0,
        le=2.0,
        description="Exaggeration level for expressiveness (not supported in turbo)",
    )
    audio_prompt: Optional[str] = Field(
        default=None, description="Path to audio file for voice cloning"
    )


class VoiceInfo(BaseModel):
    """Information about an available voice"""

    id: str = Field(..., description="Voice identifier")
    name: str = Field(..., description="Human-readable voice name")
    languages: List[str] = Field(
        default_factory=list, description="Supported language codes"
    )


class VoicesResponse(BaseModel):
    """Response containing list of available voices"""

    voices: List[VoiceInfo] = Field(..., description="List of available voices")


class HealthResponse(BaseModel):
    """Health check response"""

    status: str = Field(..., description="Service status")
    model: str = Field(..., description="Loaded model name")
    device: str = Field(..., description="Device model is running on")
