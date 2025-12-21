# 🎤 Voice Samples Setup Complete!

## ✅ What's Been Set Up

### 1. **Voice Samples Directory** (`voice_samples/`)
- **22 MP3 voice samples** organized and ready to use
- Categorized by type: Spanish female, Spanish male, test samples, and long-form content
- Complete documentation in `voice_samples/README.md`

### 2. **Interactive Testing Tool** (`test_voice_samples.py`)
- Easy-to-use command-line interface for testing voices
- 9 predefined voice profiles for quick access
- Supports custom voice files
- Full OpenAI-compatible API integration

### 3. **Documentation**
- `VOICE_SAMPLES_GUIDE.md` - Quick reference guide with examples
- `voice_samples/README.md` - Detailed voice catalog
- Updated API examples with correct OpenAI format

### 4. **Demo Outputs** (`demo_outputs/`)
- 3 test audio files demonstrating different voices:
  - `test_aimee_output.mp3` - Female voice (167 KB)
  - `test_brenda_output.mp3` - Female voice (156 KB)
  - `test_facu_output.mp3` - Male voice (160 KB)

---

## 🚀 Quick Start

### List All Available Voices
```bash
python test_voice_samples.py list
```

### Generate Speech with a Voice
```bash
# Using a predefined voice profile
python test_voice_samples.py aimee "Hola, ¿cómo estás?" es output.mp3

# Using a custom MP3 file
python test_voice_samples.py file voice_samples/custom.mp3 "Your text" en output.mp3
```

---

## 📋 Available Voice Profiles

### Quick Test Voices (Small & Fast)
- **aimee** - Female, 145 KB
- **michael** - Male, 111 KB
- **facundito** - Male, 105 KB

### High Quality Spanish Female
- **brenda** - 827 KB
- **colombiana** - 989 KB
- **vozespanola** - 933 KB

### High Quality Spanish Male
- **facu** - 791 KB
- **lucho** - 855 KB

### Long-form Content
- **facunormal** - 10 MB (very high quality)

---

## 💻 API Usage

### Python
```python
import requests

payload = {
    'model': 'chatterbox-multilingual',
    'input': 'Your text here',
    'language': 'es',
    'audio_prompt': '/absolute/path/to/voice_samples/aimee.mp3',
    'response_format': 'mp3'
}

response = requests.post('http://localhost:59363/v1/audio/speech', json=payload)

with open('output.mp3', 'wb') as out:
    out.write(response.content)
```

### cURL
```bash
curl -X POST http://localhost:59363/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "chatterbox-multilingual",
    "input": "Hola mundo",
    "language": "es",
    "audio_prompt": "/absolute/path/to/voice_samples/aimee.mp3",
    "response_format": "mp3"
  }' \
  --output output.mp3
```

---

## 📁 Directory Structure

```
chatterbox-FASTAPI-1/
├── voice_samples/              # 22 voice reference files
│   ├── README.md              # Detailed voice catalog
│   ├── aimee.mp3
│   ├── brenda.mp3
│   ├── facu.mp3
│   └── ... (19 more)
├── demo_outputs/              # Example generated audio
│   ├── test_aimee_output.mp3
│   ├── test_brenda_output.mp3
│   └── test_facu_output.mp3
├── test_voice_samples.py      # Interactive testing tool
├── VOICE_SAMPLES_GUIDE.md     # Quick reference guide
└── README.md                  # Main project documentation
```

---

## 🎯 Common Use Cases

### 1. Quick Voice Test
```bash
python test_voice_samples.py aimee "Test message"
```

### 2. High-Quality Spanish Female Voice
```bash
python test_voice_samples.py brenda "Mensaje en español" es output.mp3
```

### 3. High-Quality Spanish Male Voice
```bash
python test_voice_samples.py facu "Mensaje masculino" es output.mp3
```

### 4. Custom Voice File
```bash
python test_voice_samples.py file /path/to/your/voice.mp3 "Text" en output.mp3
```

---

## 💡 Tips for Best Results

1. **Sample Quality**: Use clean, clear audio samples (3-10 seconds) for best voice cloning
2. **Language Matching**: Match the reference audio language with your target language
3. **File Size**: Smaller samples (100-500 KB) work well and load faster
4. **Testing**: Start with quick test voices (`aimee`, `michael`, `facundito`) for rapid iteration
5. **Absolute Paths**: Always use absolute paths for `audio_prompt` in API calls

---

## 🔧 Troubleshooting

### Server Not Responding?
```bash
# Check server health
curl http://localhost:59363/health

# Restart server if needed
./launch_server.sh
```

### Voice Not Found?
```bash
# List all available voices
python test_voice_samples.py list
```

### Need to Add a New Voice?
1. Copy your MP3 file to `voice_samples/`
2. Use it directly:
   ```bash
   python test_voice_samples.py file voice_samples/new_voice.mp3 "Text"
   ```

---

## 📊 Test Results

All voice samples have been tested and verified working:
- ✅ **aimee** - Generated 167 KB output
- ✅ **brenda** - Generated 156 KB output
- ✅ **facu** - Generated 160 KB output

Server is running on port **59363** and responding correctly to all requests.

---

## 🎉 You're All Set!

Your voice samples are now organized and ready to use with the Chatterbox TTS system. 

**Next Steps:**
1. Try different voices with `python test_voice_samples.py list`
2. Experiment with the API using the examples above
3. Add your own custom voice samples to `voice_samples/`
4. Check out the demo outputs in `demo_outputs/`

Happy voice cloning! 🎙️✨
