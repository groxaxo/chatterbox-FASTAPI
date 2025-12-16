"""
Quick Start Example for Chatterbox FastAPI

This example demonstrates the basic usage of the Chatterbox FastAPI server.
"""

import requests
from openai import OpenAI

def example_openai_client():
    """Example using OpenAI Python client"""
    print("\n" + "="*60)
    print("Example 1: Using OpenAI Python Client")
    print("="*60)
    
    # Initialize OpenAI client pointing to local server
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed"  # API key not required for local server
    )
    
    # Generate English speech
    print("\nGenerating English speech...")
    response = client.audio.speech.create(
        model="chatterbox-multilingual",
        voice="default",
        input="Hello! Welcome to Chatterbox FastAPI with multilingual support.",
    )
    response.stream_to_file("example_english.mp3")
    print("✓ Saved to example_english.mp3")
    
    # Generate Spanish speech
    print("\nGenerating Spanish speech...")
    response = client.audio.speech.create(
        model="chatterbox-multilingual",
        voice="default",
        input="¡Hola! Bienvenido a Chatterbox FastAPI con soporte multilingüe.",
        language="es"
    )
    response.stream_to_file("example_spanish.mp3")
    print("✓ Saved to example_spanish.mp3")


def example_requests_library():
    """Example using requests library"""
    print("\n" + "="*60)
    print("Example 2: Using Requests Library")
    print("="*60)
    
    # Generate French speech
    print("\nGenerating French speech...")
    response = requests.post(
        "http://localhost:8000/v1/audio/speech",
        json={
            "model": "chatterbox-multilingual",
            "input": "Bonjour! Bienvenue dans Chatterbox FastAPI.",
            "voice": "default",
            "language": "fr",
            "response_format": "mp3"
        }
    )
    
    if response.status_code == 200:
        with open("example_french.mp3", "wb") as f:
            f.write(response.content)
        print("✓ Saved to example_french.mp3")
    else:
        print(f"✗ Error: {response.status_code}")


def example_different_formats():
    """Example with different audio formats"""
    print("\n" + "="*60)
    print("Example 3: Different Audio Formats")
    print("="*60)
    
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")
    
    text = "Testing different audio formats."
    
    # MP3 format
    print("\nGenerating MP3...")
    response = client.audio.speech.create(
        model="chatterbox-multilingual",
        voice="default",
        input=text,
        response_format="mp3"
    )
    response.stream_to_file("example_format.mp3")
    print("✓ Saved to example_format.mp3")
    
    # WAV format
    print("\nGenerating WAV...")
    response = client.audio.speech.create(
        model="chatterbox-multilingual",
        voice="default",
        input=text,
        response_format="wav"
    )
    response.stream_to_file("example_format.wav")
    print("✓ Saved to example_format.wav")


def example_multilingual():
    """Example with multiple languages"""
    print("\n" + "="*60)
    print("Example 4: Multiple Languages")
    print("="*60)
    
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")
    
    languages = [
        ("en", "Hello from Chatterbox!", "example_lang_en.mp3"),
        ("de", "Hallo von Chatterbox!", "example_lang_de.mp3"),
        ("ja", "チャターボックスからこんにちは！", "example_lang_ja.mp3"),
        ("zh", "你好，来自 Chatterbox！", "example_lang_zh.mp3"),
    ]
    
    for lang_code, text, filename in languages:
        print(f"\nGenerating {lang_code.upper()}...")
        response = client.audio.speech.create(
            model="chatterbox-multilingual",
            voice="default",
            input=text,
            language=lang_code
        )
        response.stream_to_file(filename)
        print(f"✓ Saved to {filename}")


def list_available_voices():
    """List available voices"""
    print("\n" + "="*60)
    print("Example 5: List Available Voices")
    print("="*60)
    
    response = requests.get("http://localhost:8000/v1/audio/voices")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nFound {len(data['voices'])} voice(s):")
        for voice in data['voices']:
            print(f"\n  Voice: {voice['name']}")
            print(f"  ID: {voice['id']}")
            print(f"  Languages: {len(voice['languages'])} supported")
            print(f"  Codes: {', '.join(voice['languages'][:10])}...")
    else:
        print(f"✗ Error: {response.status_code}")


def check_server_health():
    """Check server health"""
    print("\n" + "="*60)
    print("Checking Server Health")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✓ Server is healthy!")
            print(f"  Model: {data['model']}")
            print(f"  Device: {data['device']}")
            return True
        else:
            print(f"\n✗ Server returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n✗ Cannot connect to server!")
        print("\nPlease start the server first:")
        print("  python -m api.main")
        print("  or")
        print("  ./start_server.sh")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def main():
    """Run all examples"""
    print("="*60)
    print("Chatterbox FastAPI - Quick Start Examples")
    print("="*60)
    
    # Check if server is running
    if not check_server_health():
        return
    
    try:
        # Run examples
        example_openai_client()
        example_requests_library()
        example_different_formats()
        example_multilingual()
        list_available_voices()
        
        print("\n" + "="*60)
        print("✓ All examples completed successfully!")
        print("="*60)
        print("\nGenerated files:")
        print("  - example_english.mp3")
        print("  - example_spanish.mp3")
        print("  - example_french.mp3")
        print("  - example_format.mp3")
        print("  - example_format.wav")
        print("  - example_lang_*.mp3 (multiple languages)")
        
    except Exception as e:
        print(f"\n✗ Error running examples: {e}")


if __name__ == "__main__":
    main()
