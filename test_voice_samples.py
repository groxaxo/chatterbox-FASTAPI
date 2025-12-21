#!/usr/bin/env python3
"""
Voice Sample Tester for Chatterbox TTS
Easily test different voice samples with the TTS system
"""

import os
import sys
import requests
from pathlib import Path

# Configuration
API_URL = "http://localhost:59363/v1/audio/speech"
VOICE_SAMPLES_DIR = Path(__file__).parent / "voice_samples"

# Predefined voice profiles
VOICE_PROFILES = {
    # Quick test voices (small files)
    "aimee": "aimee.mp3",
    "michael": "michael.mp3",
    "facundito": "facundito.mp3",
    # High quality Spanish female
    "brenda": "brenda.mp3",
    "colombiana": "colombiana.mp3",
    "vozespanola": "vozespanola.mp3",
    # High quality Spanish male
    "facu": "facu.mp3",
    "lucho": "lucho.mp3",
    # Long-form samples
    "facunormal": "facunormal.mp3",
}


def list_voices():
    """List all available voice profiles"""
    print("\n🎤 Available Voice Profiles:")
    print("=" * 50)

    for name, filename in VOICE_PROFILES.items():
        filepath = VOICE_SAMPLES_DIR / filename
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            print(f"  • {name:15} - {filename:30} ({size_kb:.1f} KB)")
        else:
            print(f"  • {name:15} - {filename:30} (NOT FOUND)")

    print("\n📁 All MP3 files in voice_samples/:")
    print("=" * 50)
    for mp3_file in sorted(VOICE_SAMPLES_DIR.glob("*.mp3")):
        size_kb = mp3_file.stat().st_size / 1024
        print(f"  • {mp3_file.name:45} ({size_kb:.1f} KB)")


def generate_with_voice(
    text, voice_name=None, voice_file=None, language="es", output_file="output.mp3"
):
    """
    Generate speech with a specific voice sample

    Args:
        text: Text to synthesize
        voice_name: Name from VOICE_PROFILES (e.g., 'aimee', 'facu')
        voice_file: Direct path to MP3 file (overrides voice_name)
        language: Language code ('es' or 'en')
        output_file: Output filename
    """
    # Determine which voice file to use
    if voice_file:
        reference_path = Path(voice_file)
    elif voice_name:
        if voice_name not in VOICE_PROFILES:
            print(f"❌ Unknown voice profile: {voice_name}")
            print(f"Available profiles: {', '.join(VOICE_PROFILES.keys())}")
            return False
        reference_path = VOICE_SAMPLES_DIR / VOICE_PROFILES[voice_name]
    else:
        print("❌ Please specify either voice_name or voice_file")
        return False

    if not reference_path.exists():
        print(f"❌ Voice file not found: {reference_path}")
        return False

    # Convert to absolute path
    reference_path = reference_path.absolute()

    print(f"\n🎙️  Generating speech...")
    print(f"   Voice: {reference_path.name}")
    print(f"   Text: {text[:50]}{'...' if len(text) > 50 else ''}")
    print(f"   Language: {language}")

    try:
        # Use OpenAI-compatible JSON API format
        payload = {
            "model": "chatterbox-multilingual",
            "input": text,
            "language": language,
            "audio_prompt": str(reference_path),
            "response_format": "mp3",
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            with open(output_file, "wb") as out:
                out.write(response.content)
            print(f"✅ Success! Audio saved to: {output_file}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API at {API_URL}")
        print("   Make sure the server is running!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("\n🎤 Chatterbox Voice Sample Tester")
        print("=" * 50)
        print("\nUsage:")
        print("  python test_voice_samples.py list")
        print(
            "  python test_voice_samples.py <voice_name> <text> [language] [output_file]"
        )
        print(
            "  python test_voice_samples.py file <path_to_mp3> <text> [language] [output_file]"
        )
        print("\nExamples:")
        print("  python test_voice_samples.py list")
        print("  python test_voice_samples.py aimee 'Hola, ¿cómo estás?'")
        print("  python test_voice_samples.py facu 'Buenos días' es output.mp3")
        print("  python test_voice_samples.py file custom.mp3 'Hello world' en")
        print()
        list_voices()
        return

    command = sys.argv[1]

    if command == "list":
        list_voices()
        return

    if command == "file":
        if len(sys.argv) < 4:
            print(
                "❌ Usage: python test_voice_samples.py file <path_to_mp3> <text> [language] [output_file]"
            )
            return

        voice_file = sys.argv[2]
        text = sys.argv[3]
        language = sys.argv[4] if len(sys.argv) > 4 else "es"
        output_file = sys.argv[5] if len(sys.argv) > 5 else "output.mp3"

        generate_with_voice(
            text, voice_file=voice_file, language=language, output_file=output_file
        )
    else:
        voice_name = command
        if len(sys.argv) < 3:
            print(
                f"❌ Usage: python test_voice_samples.py {voice_name} <text> [language] [output_file]"
            )
            return

        text = sys.argv[2]
        language = sys.argv[3] if len(sys.argv) > 3 else "es"
        output_file = sys.argv[4] if len(sys.argv) > 4 else "output.mp3"

        generate_with_voice(
            text, voice_name=voice_name, language=language, output_file=output_file
        )


if __name__ == "__main__":
    main()
