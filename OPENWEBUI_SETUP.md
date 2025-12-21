# Open-WebUI Integration Guide

## 🎙️ Automatic Voice Selection with Chatterbox TTS

This guide shows you how to configure Open-WebUI to use Chatterbox's automatic voice sample mapping. When configured, you can select voices like "aimee", "facu", or "brenda" directly in Open-WebUI's interface!

---

## ✅ What's Been Implemented

Chatterbox now supports automatic voice name resolution:
- **21 voices discovered** from your `voice_samples/` directory
- Voice names automatically mapped to MP3 files
- Open-WebUI compatible `/v1/audio/voices` endpoint
- Standard OpenAI TTS API format

---

## 🚀 Quick Setup

### Step 1: Verify Chatterbox Server is Running

```bash
# Check server health
curl http://localhost:59363/health

# List available voices
curl http://localhost:59363/v1/audio/voices | jq '.voices[] | .id'
```

You should see voices like: `default`, `aimee`, `brenda`, `colombiana`, `facu`, etc.

### Step 2: Configure Open-WebUI

1. **Open Open-WebUI** in your browser
2. **Click your profile** (bottom left)
3. **Select "Admin Panel"** or "Settings"
4. **Navigate to "Audio"** tab

### Step 3: Configure TTS Settings

In the Audio settings page:

| Setting | Value |
|---------|-------|
| **Text-to-Speech Engine** | OpenAI |
| **API Base URL** | `http://localhost:59363/v1` |
| **API Key** | (leave empty or use dummy key) |
| **TTS Model** | `chatterbox-multilingual` or `tts-1` |
| **TTS Voice** | Select from dropdown (aimee, facu, brenda, etc.) |

> **Note**: If running Open-WebUI in Docker, use `http://host.docker.internal:59363/v1` instead

### Step 4: Save and Test

1. Click **"Save"** at the bottom of the settings page
2. Go to a chat conversation
3. Type a message and click the **speaker icon** to generate TTS
4. The audio should use the selected voice!

---

## 🎯 Available Voices

Your Chatterbox installation currently has these voices:

### Quick Test Voices (Fast)
- **default** - Base model (no voice cloning)
- **aimee** - Female voice (145 KB)
- **michael** - Male voice (111 KB)
- **facundito** - Male voice (105 KB)

### High Quality Spanish Female
- **brenda** - Female voice (827 KB)
- **colombiana** - Colombian female voice (989 KB)
- **vozespanola** - Spanish female voice (933 KB)

### High Quality Spanish Male
- **facu** - Male voice (791 KB)
- **lucho** - Male voice (855 KB)

### Long-form/Other Voices
- **facunormal** - Very high quality male (10 MB)
- **faculiado**, **gemini_generated_video_0b2ae980**, and more...

---

## 🧪 Testing Without Open-WebUI

### Test with cURL

```bash
# Test with Aimee's voice
curl -X POST http://localhost:59363/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "chatterbox-multilingual",
    "input": "Hola, soy Aimee y esta es mi voz.",
    "language": "es",
    "voice": "aimee",
    "response_format": "mp3"
  }' \
  --output test_aimee.mp3

# Test with Facu's voice
curl -X POST http://localhost:59363/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "chatterbox-multilingual",
    "input": "Hola, soy Facu.",
    "language": "es",
    "voice": "facu",
    "response_format": "mp3"
  }' \
  --output test_facu.mp3
```

### Test with Python

```python
import requests

payload = {
    'model': 'chatterbox-multilingual',
    'input': 'Hello, this is a test with voice cloning.',
    'language': 'en',
    'voice': 'aimee',  # Use voice name here!
    'response_format': 'mp3'
}

response = requests.post('http://localhost:59363/v1/audio/speech', json=payload)

with open('output.mp3', 'wb') as f:
    f.write(response.content)
```

---

## 🔄 Adding New Voices

Want to add your own voice samples?

1. **Add MP3 file** to `voice_samples/` directory
   ```bash
   cp my_custom_voice.mp3 voice_samples/
   ```

2. **Wait 60 seconds** for auto-discovery (or restart server for immediate recognition)

3. **Verify it's discovered**:
   ```bash
   curl http://localhost:59363/v1/audio/voices | jq '.voices[] | select(.id == "my_custom_voice")'
   ```

4. **Use in Open-WebUI**: The voice will now appear in the dropdown!

---

## 🔧 Troubleshooting

### Voice dropdown is empty in Open-WebUI
- Verify the API Base URL is correct
- Check that the server is accessible from Open-WebUI
- Try refreshing the page or clearing browser cache

### Voice not found error
```bash
# Check available voices
curl http://localhost:59363/v1/audio/voices
```

### Server not responding
```bash
# Restart the server
./launch_server.sh

# Or manually:
PORT=59363 conda run -n chatterbox-fastapi python -m api.main
```

### Voices not appearing after adding new MP3
- Wait 60 seconds for cache refresh
- Or restart the server immediately: `pkill -f "python -m api.main" && ./launch_server.sh`

---

## 📊 API Behavior

### Voice Parameter Priority

1. **`audio_prompt`** (explicit file path) - Highest priority
2. **`voice`** (voice name) - Resolved to file path
3. **None** - Uses base model without cloning

Example:
```json
{
  "voice": "aimee",           // ✅ Automatically resolves to voice_samples/aimee.mp3
  "audio_prompt": null        // Can be omitted
}
```

### Language Support

All voices support all languages via multilingual voice cloning:
- Spanish (es)
- English (en)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- And 20+ more languages!

---

## ✨ Features

- ✅ **Auto-discovery**: New MP3 files automatically detected
- ✅ **Caching**: Voice list cached for 60 seconds for performance
- ✅ **Error handling**: Helpful messages if voice not found
- ✅ **Backward compatible**: Still supports `audio_prompt` parameter
- ✅ **OpenAI compatible**: Works with any OpenAI TTS client

---

## 🎉 You're All Set!

Your Chatterbox server is now ready for Open-WebUI integration. Users can select voices by name, and the system will automatically use the corresponding voice sample files.

**Next Steps:**
1. Configure Open-WebUI with your Chatterbox server URL
2. Select a voice from the dropdown
3. Generate some speech and enjoy the voice cloning!

For more details, see the main [Voice Samples Guide](VOICE_SAMPLES_GUIDE.md).
