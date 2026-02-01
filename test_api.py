import requests
import base64
import os
def test_api():
    """Test the Voice Detection API"""
    print("="*60)
    print("🧪 TESTING VOICE DETECTION API")
    print("="*60)
    print()
    base_url = "http://localhost:5000"
    api_key = "sk_test_123456789"
    # Test 1: Health Check
    print("📋 Test 1: Health Check")
    response = requests.get(f"{base_url}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print()
    # Test 2: Voice Detection (if sample file exists)
    if os.path.exists('sample.mp3'):
        print("📋 Test 2: Voice Detection with Sample Audio")
        with open('sample.mp3', 'rb') as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        headers = {'x-api-key': api_key}
        data = {
            'language': 'English',
            'audioFormat': 'mp3',
            'audioBase64': audio_base64
        }
        response = requests.post(
            f"{base_url}/api/voice-detection",
            headers=headers,
            json=data
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Classification: {result.get('classification')}")
            print(f"   Confidence: {result.get('confidenceScore')}")
            print(f"   Explanation: {result.get('explanation')}")
        else:
            print(f"   Error: {response.json()}")
    else:
        print("⚠️  No sample.mp3 file found. Place a sample MP3 in the project folder.")
    print()
    print("="*60)
if __name__ == "__main__":
    test_api()