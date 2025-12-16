"""
Example script to test the Chatterbox FastAPI server

This script demonstrates how to use the OpenAI-compatible API endpoints.
"""
from openai import OpenAI

def test_basic_tts():
    """Test basic text-to-speech"""
    print("Testing basic TTS...")
    
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed"
    )
    
    response = client.audio.speech.create(
        model="chatterbox-multilingual",
        voice="default",
        input="Hello! This is a test of the Chatterbox FastAPI server."
    )
    
    response.stream_to_file("test_basic.mp3")
    print("✓ Basic TTS test completed - saved to test_basic.mp3")


def test_multilingual():
    """Test multilingual support"""
    print("\nTesting multilingual support...")
    
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed"
    )
    
    tests = [
        ("en", "Hello, how are you today?", "test_english.mp3"),
        ("es", "Hola, ¿cómo estás hoy?", "test_spanish.mp3"),
        ("fr", "Bonjour, comment allez-vous aujourd'hui?", "test_french.mp3"),
        ("de", "Hallo, wie geht es dir heute?", "test_german.mp3"),
        ("ja", "こんにちは、今日はお元気ですか？", "test_japanese.mp3"),
        ("zh", "你好，你今天好吗？", "test_chinese.mp3"),
    ]
    
    for lang, text, filename in tests:
        response = client.audio.speech.create(
            model="chatterbox-multilingual",
            voice="default",
            input=text,
            language=lang
        )
        response.stream_to_file(filename)
        print(f"✓ {lang.upper()}: {filename}")


def test_different_formats():
    """Test different audio formats"""
    print("\nTesting different audio formats...")
    
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed"
    )
    
    text = "Testing different audio formats."
    formats = ["mp3", "wav", "flac", "opus"]
    
    for fmt in formats:
        response = client.audio.speech.create(
            model="chatterbox-multilingual",
            voice="default",
            input=text,
            response_format=fmt
        )
        filename = f"test_format.{fmt}"
        response.stream_to_file(filename)
        print(f"✓ {fmt.upper()}: {filename}")


def test_api_with_requests():
    """Test API using requests library"""
    print("\nTesting with requests library...")
    
    import requests
    
    response = requests.post(
        "http://localhost:8000/v1/audio/speech",
        json={
            "model": "chatterbox-multilingual",
            "input": "Testing with requests library.",
            "voice": "default",
            "language": "en",
            "response_format": "mp3"
        }
    )
    
    if response.status_code == 200:
        with open("test_requests.mp3", "wb") as f:
            f.write(response.content)
        print("✓ Requests test completed - saved to test_requests.mp3")
    else:
        print(f"✗ Request failed: {response.status_code}")


def list_voices():
    """List available voices"""
    print("\nListing available voices...")
    
    import requests
    
    response = requests.get("http://localhost:8000/v1/audio/voices")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {len(data['voices'])} voice(s)")
        for voice in data['voices']:
            print(f"  - {voice['name']} (ID: {voice['id']})")
            print(f"    Languages: {len(voice['languages'])} supported")
    else:
        print(f"✗ Request failed: {response.status_code}")


def check_health():
    """Check server health"""
    print("\nChecking server health...")
    
    import requests
    
    response = requests.get("http://localhost:8000/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Server is healthy")
        print(f"  - Model: {data['model']}")
        print(f"  - Device: {data['device']}")
    else:
        print(f"✗ Health check failed: {response.status_code}")


if __name__ == "__main__":
    print("=" * 60)
    print("Chatterbox FastAPI Test Suite")
    print("=" * 60)
    
    try:
        check_health()
        list_voices()
        test_basic_tts()
        test_api_with_requests()
        test_different_formats()
        test_multilingual()
        
        print("\n" + "=" * 60)
        print("✓ All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        print("\nMake sure the server is running:")
        print("  python -m api.main")
