# Voice Samples Directory

This directory contains reference voice samples for use with the Chatterbox TTS system.

## Available Voice Samples

### Spanish Voices
- **aimee.mp3** - Female voice (148 KB)
- **brenda.mp3** - Female voice (847 KB)
- **colombiana.mp3** - Colombian female voice (1.0 MB)
- **colombiana_test.mp3** - Colombian test sample
- **vozespanola.mp3** - Spanish voice (955 KB)
- **story_spanish.mp3** - Spanish story narration (167 KB)
- **Luisana Lopilato explicó por qué no formará parte de la gira que marcará el regreso de Erreway [zPKRgQEcMGo].mp3** - Interview clip (1.3 MB)

### Male Voices
- **facu.mp3** - Male voice (810 KB)
- **faculiado.mp3** - Male voice variant (2.8 MB)
- **facundito.mp3** - Male voice short sample (107 KB)
- **facunormal.mp3** - Male voice normal (10.3 MB)
- **lucho.mp3** - Male voice (876 KB)
- **michael.mp3** - Male voice (114 KB)

### Test/Generated Samples
- **gemini_generated_video_0B2AE980.mp3** - AI generated (139 KB)
- **test_audio.mp3** - Test audio (8.6 MB)
- **test_output.mp3** - Test output (178 B)
- **test_output_corrected.mp3** - Corrected test (444 KB)
- **test_spanish_model_variant.mp3** - Spanish model test (171 KB)
- **speed_test.mp3** - Speed test (1.9 MB)
- **se_fue_alabosta.mp3** - Test sample (468 KB)

### Long-form Content
- **part_01_approx.mp3** - Long audio part 1 (28.8 MB)
- **part_01_valid.mp3** - Validated part 1 (481 KB)

## Usage

### Using with the API

```python
import requests

# Use a voice sample as reference
payload = {
    'model': 'chatterbox-multilingual',
    'input': 'Your text here',
    'language': 'es',  # or 'en'
    'audio_prompt': '/absolute/path/to/voice_samples/aimee.mp3',
    'response_format': 'mp3'
}

response = requests.post('http://localhost:59363/v1/audio/speech', json=payload)

with open('output.mp3', 'wb') as out:
    out.write(response.content)
```

### Using with the Test Script

```bash
# Quick test with a predefined voice
python test_voice_samples.py aimee "Your text here" es output.mp3

# List all available voices
python test_voice_samples.py list
```

## Recommended Samples by Use Case

- **Quick Tests**: `facundito.mp3`, `michael.mp3`, `aimee.mp3` (small files)
- **High Quality Spanish Female**: `brenda.mp3`, `colombiana.mp3`
- **High Quality Spanish Male**: `facu.mp3`, `lucho.mp3`
- **Long-form Content**: `facunormal.mp3`, `part_01_approx.mp3`

## Tips

1. **Sample Quality**: Use clean, clear audio samples (3-10 seconds) for best results
2. **Language Matching**: Match the reference audio language with your target language
3. **File Size**: Smaller samples (100-500 KB) work well and load faster
4. **Testing**: Start with short samples like `facundito.mp3` or `aimee.mp3` for quick tests
