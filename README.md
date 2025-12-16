```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    ╔═╗╦ ╦╔═╗╔╦╗╔╦╗╔═╗╦═╗╔╗ ╔═╗═╗ ╦                          ║
║    ║  ╠═╣╠═╣ ║  ║ ║╣ ╠╦╝╠╩╗║ ║╔╩╦╝                          ║
║    ╚═╝╩ ╩╩ ╩ ╩  ╩ ╚═╝╩╚═╚═╝╚═╝╩ ╚═                          ║
║         FastAPI - OpenAI Compatible TTS                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

# Chatterbox FastAPI

[![Alt Text](https://img.shields.io/badge/listen-demo_samples-blue)](https://resemble-ai.github.io/chatterbox_turbo_demopage/)
[![Alt Text](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-sm.svg)](https://huggingface.co/spaces/ResembleAI/chatterbox-turbo-demo)
[![Alt Text](https://static-public.podonos.com/badges/insight-on-pdns-sm-dark.svg)](https://podonos.com/resembleai/chatterbox)
[![Discord](https://img.shields.io/discord/1377773249798344776?label=join%20discord&logo=discord&style=flat)](https://discord.gg/rJq9cRJBJ6)

_Made with ♥️ by <a href="https://resemble.ai" target="_blank"><img width="100" alt="resemble-logo-horizontal" src="https://github.com/user-attachments/assets/35cf756b-3506-4943-9c72-c05ddfa4e525" /></a>

**Chatterbox FastAPI** is an OpenAI-compatible REST API wrapper for Chatterbox TTS models. This fork adds FastAPI support with OpenAI-compatible endpoints, focusing on the multilingual model with 23+ language support, and removes watermarking to save resources.

## ✨ Features

- 🌐 **OpenAI-Compatible API** - Drop-in replacement for OpenAI's TTS API
- 🗣️ **Multilingual Support** - 23+ languages with zero-shot voice cloning
- ⚡ **FastAPI Backend** - Modern, fast, production-ready API
- 🚀 **No Watermarking** - Optimized for performance, watermarking removed
- 🎯 **Simple Integration** - Compatible with OpenAI Python client

## 🚀 Quick Start

### Installation

```shell
pip install chatterbox-tts
```

Or install from source:
```shell
git clone https://github.com/groxaxo/chatterbox-FASTAPI.git
cd chatterbox-FASTAPI
pip install -e .
```

### Start the FastAPI Server

```shell
python -m api.main
```

Or with uvicorn directly:
```shell
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

## 📖 API Usage

### Using OpenAI Python Client

```python
from openai import OpenAI

# Initialize client pointing to local server
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"  # API key not required for local server
)

# Generate speech
response = client.audio.speech.create(
    model="chatterbox-multilingual",
    voice="default",
    input="Hello! This is a test of the Chatterbox multilingual TTS system.",
    language="en"  # Optional: specify language code
)

# Save to file
response.stream_to_file("output.mp3")
```

### Using requests

```python
import requests

# Generate speech
response = requests.post(
    "http://localhost:8000/v1/audio/speech",
    json={
        "model": "chatterbox-multilingual",
        "input": "Bonjour! Ceci est un test du système TTS multilingue Chatterbox.",
        "voice": "default",
        "language": "fr",  # French
        "response_format": "mp3"
    }
)

# Save audio
with open("output.mp3", "wb") as f:
    f.write(response.content)
```

### Multilingual Examples

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

# Spanish
response = client.audio.speech.create(
    model="chatterbox-multilingual",
    voice="default",
    input="Hola, ¿cómo estás?",
    language="es"
)
response.stream_to_file("spanish.mp3")

# Chinese
response = client.audio.speech.create(
    model="chatterbox-multilingual",
    voice="default",
    input="你好，今天天气真不错。",
    language="zh"
)
response.stream_to_file("chinese.mp3")

# Japanese
response = client.audio.speech.create(
    model="chatterbox-multilingual",
    voice="default",
    input="こんにちは、お元気ですか？",
    language="ja"
)
response.stream_to_file("japanese.mp3")
```

### Voice Cloning with Audio Prompt

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

response = client.audio.speech.create(
    model="chatterbox-multilingual",
    voice="default",
    input="This will be spoken in the voice from the audio prompt.",
    audio_prompt="path/to/your/reference_audio.wav"
)
response.stream_to_file("cloned_voice.mp3")
```

## 🌍 Supported Languages

Arabic (ar) • Danish (da) • German (de) • Greek (el) • English (en) • Spanish (es) • Finnish (fi) • French (fr) • Hebrew (he) • Hindi (hi) • Italian (it) • Japanese (ja) • Korean (ko) • Malay (ms) • Dutch (nl) • Norwegian (no) • Polish (pl) • Portuguese (pt) • Russian (ru) • Swedish (sv) • Swahili (sw) • Turkish (tr) • Chinese (zh)

## 🔌 API Endpoints

### POST `/v1/audio/speech`

Generate speech from text.

**Request Body:**
```json
{
  "model": "chatterbox-multilingual",
  "input": "Text to synthesize",
  "voice": "default",
  "language": "en",
  "response_format": "mp3",
  "speed": 1.0,
  "temperature": 0.7,
  "cfg_weight": 0.5,
  "exaggeration": 0.5,
  "audio_prompt": null
}
```

**Supported Formats:** mp3, wav, opus, flac, pcm

### GET `/v1/audio/voices`

List available voices and supported languages.

### GET `/v1/models`

List available TTS models.

### GET `/health`

Health check endpoint.

### GET `/docs`

Interactive API documentation (Swagger UI).

## ⚙️ Configuration

### Request Parameters

- `model`: Model to use (`chatterbox-multilingual`, `tts-1`, `tts-1-hd`)
- `input`: Text to synthesize (required)
- `voice`: Voice ID (default: "default")
- `language`: Language code (e.g., "en", "es", "fr", "zh")
- `response_format`: Output format (mp3, wav, opus, flac, pcm)
- `speed`: Speech speed (0.25 to 4.0, default: 1.0)
- `temperature`: Sampling temperature (0.0 to 1.0, default: 0.7)
- `cfg_weight`: Classifier-free guidance weight (0.0 to 1.0, default: 0.5)
- `exaggeration`: Expressiveness level (0.0 to 1.0, default: 0.5)
- `audio_prompt`: Path to reference audio for voice cloning

## 🔧 Direct Python Usage (without API)

You can still use the models directly in Python:

```python
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

# Load model
model = ChatterboxMultilingualTTS.from_pretrained(device="cuda")

# Generate speech
text = "Bonjour, comment ça va?"
wav = model.generate(text, language_id="fr")

# Save
ta.save("output.wav", wav, model.sr)
```

## 🎯 Changes from Original Chatterbox

This fork includes the following modifications:

1. **FastAPI Integration** - Added OpenAI-compatible REST API
2. **Watermark Removal** - Removed PerTh watermarking to save resources
3. **Multilingual Focus** - Optimized for multilingual model usage
4. **API Documentation** - Added comprehensive API docs and examples

## 📚 Original Chatterbox Models

**Chatterbox** is a family of three state-of-the-art, open-source text-to-speech models by Resemble AI:

| Model | Size | Languages | Key Features |
|-------|------|-----------|--------------|
| **Chatterbox-Turbo** | 350M | English | Paralinguistic Tags (`[laugh]`), Lower Compute |
| **Chatterbox-Multilingual** | 500M | 23+ | Zero-shot cloning, Multiple Languages |
| **Chatterbox** | 500M | English | CFG & Exaggeration tuning |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project maintains the same license as the original Chatterbox project.

## 🙏 Acknowledgements

- [Resemble AI](https://resemble.ai) for the original Chatterbox models
- [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) for API implementation inspiration
- Original Chatterbox acknowledgements:
  - [Cosyvoice](https://github.com/FunAudioLLM/CosyVoice)
  - [Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning)
  - [HiFT-GAN](https://github.com/yl4579/HiFTNet)
  - [Llama 3](https://github.com/meta-llama/llama3)
  - [S3Tokenizer](https://github.com/xingchensong/S3Tokenizer)

## ⚠️ Disclaimer

This is a modified version of Chatterbox. For production use with guarantees and support, consider [Resemble AI's TTS service](https://resemble.ai).

Don't use this model for malicious purposes. Prompts are sourced from freely available data on the internet.
