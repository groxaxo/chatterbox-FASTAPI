"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    ╔═╗╦ ╦╔═╗╔╦╗╔╦╗╔═╗╦═╗╔╗ ╔═╗═╗ ╦                          ║
║    ║  ╠═╣╠═╣ ║  ║ ║╣ ╠╦╝╠╩╗║ ║╔╩╦╝                          ║
║    ╚═╝╩ ╩╩ ╩ ╩  ╩ ╚═╝╩╚═╚═╝╚═╝╩ ╚═                          ║
║         FastAPI - OpenAI Compatible TTS                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Chatterbox FastAPI Server
OpenAI-compatible text-to-speech API with multilingual support
"""

import logging
import sys
from contextlib import asynccontextmanager
from typing import Optional

import torch
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routers.openai import router as openai_router
from api.services.tts_service import get_tts_service
from api.schemas.openai import HealthResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for model initialization"""
    logger.info("Starting Chatterbox FastAPI server...")
    
    # Initialize TTS service
    try:
        service = await get_tts_service()
        device = service.device
        model_name = service.model_name
        
        startup_msg = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    ╔═╗╦ ╦╔═╗╔╦╗╔╦╗╔═╗╦═╗╔╗ ╔═╗═╗ ╦                          ║
║    ║  ╠═╣╠═╣ ║  ║ ║╣ ╠╦╝╠╩╗║ ║╔╩╦╝                          ║
║    ╚═╝╩ ╩╩ ╩ ╩  ╩ ╚═╝╩╚═╚═╝╚═╝╩ ╚═                          ║
║         FastAPI - OpenAI Compatible TTS                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
        logger.info(startup_msg)
        logger.info(f"Model: {model_name}")
        logger.info(f"Device: {device}")
        if device == "cuda":
            logger.info(f"CUDA available: {torch.cuda.is_available()}")
            if torch.cuda.is_available():
                logger.info(f"CUDA device: {torch.cuda.get_device_name(0)}")
        elif device == "mps":
            logger.info("Using Apple Metal Performance Shaders (MPS)")
        else:
            logger.info("Running on CPU")
        
        logger.info(f"Supported languages: {len(service.get_supported_languages())}")
        logger.info("Server ready!")
        logger.info("API docs: http://localhost:8000/docs")
        logger.info("Health check: http://localhost:8000/health")
        
    except Exception as e:
        logger.error(f"Failed to initialize service: {e}")
        raise
    
    yield
    
    logger.info("Shutting down Chatterbox FastAPI server...")


# Create FastAPI app
app = FastAPI(
    title="Chatterbox FastAPI",
    description="OpenAI-compatible text-to-speech API with multilingual support",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(openai_router, prefix="/v1")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Chatterbox FastAPI",
        "description": "OpenAI-compatible text-to-speech API with multilingual support",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "speech": "/v1/audio/speech",
            "voices": "/v1/audio/voices",
            "models": "/v1/models"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        service = await get_tts_service()
        return HealthResponse(
            status="healthy",
            model=service.model_name,
            device=service.device
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
