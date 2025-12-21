# 🎤 Voice Samples Quick Reference

## Quick Start

```bash
# List all available voices
python test_voice_samples.py list

# Test with a predefined voice profile
python test_voice_samples.py aimee "Hola, ¿cómo estás?"

# Test with custom language and output file
python test_voice_samples.py facu "Buenos días" es my_audio.mp3

# Use a custom MP3 file
python test_voice_samples.py file voice_samples/custom.mp3 "Hello world" en
```

## 🌟 Recommended Voices

### For Quick Tests (Small & Fast)
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

## 📝 Usage Examples

### Python API
```python
import requests

payload = {
    'model': 'chatterbox-multilingual',
    'input': 'Tu texto aquí',
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

### Command Line Tool
```bash
# Basic usage
python test_voice_samples.py aimee "Hola mundo"

# With all options
python test_voice_samples.py brenda "¿Cómo estás?" es output.mp3
```

## 💡 Tips

1. **Start Small**: Use `aimee`, `michael`, or `facundito` for quick tests
2. **Match Language**: Use Spanish voices for Spanish text, English for English
3. **Quality vs Speed**: Smaller files (100-500 KB) are faster but still high quality
4. **Sample Length**: 3-10 second samples work best for voice cloning
5. **Clean Audio**: Clear, noise-free samples produce better results

## 🗂️ File Organization

```
chatterbox-FASTAPI-1/
├── voice_samples/          # All voice reference files
│   ├── README.md          # Detailed documentation
│   ├── aimee.mp3
│   ├── brenda.mp3
│   └── ...
└── test_voice_samples.py  # Interactive testing tool
```

## 🔧 Troubleshooting

**Server not responding?**
```bash
# Check if server is running
curl http://localhost:59363/health

# Restart server if needed
./launch_server.sh
```

**Voice not found?**
```bash
# List all available voices
python test_voice_samples.py list
```

**Want to add a new voice?**
1. Copy your MP3 to `voice_samples/`
2. Use it with: `python test_voice_samples.py file voice_samples/your_voice.mp3 "text"`
