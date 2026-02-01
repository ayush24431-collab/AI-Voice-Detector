from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os
import uuid
import time
from detector import detector

app = Flask(__name__)
CORS(app)

VALID_API_KEYS = {"sk_test_123456789"}

def validate_api_key(request):
    api_key = request.headers.get('x-api-key')
    return api_key in VALID_API_KEYS

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "Voice Detection API is running",
        "detector_version": getattr(detector, 'version', 'unknown')
    }), 200

@app.route('/api/voice-detection', methods=['POST'])
def detect_voice():
    start_time = time.time()
    
    if not validate_api_key(request):
        return jsonify({"status": "error", "message": "Invalid API key or malformed request"}), 401
    
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No JSON data provided")
    except:
        return jsonify({"status": "error", "message": "Invalid JSON format"}), 400
    
    if 'audioBase64' not in data or 'language' not in data:
        return jsonify({"status": "error", "message": "Missing required fields: audioBase64 and/or language"}), 400
    
    audio_base64 = data['audioBase64']
    language = data['language']
    
    valid_languages = ['Tamil', 'English', 'Hindi', 'Malayalam', 'Telugu']
    if language not in valid_languages:
        return jsonify({"status": "error", "message": f"Invalid language. Supported: {', '.join(valid_languages)}"}), 400
    
    temp_filename = None
    try:
        audio_bytes = base64.b64decode(audio_base64)
        
        if len(audio_bytes) > 10 * 1024 * 1024:
            return jsonify({"status": "error", "message": "Audio file too large (max 10MB)"}), 400
        
        temp_filename = f"temp_{uuid.uuid4()}.mp3"
        with open(temp_filename, 'wb') as f:
            f.write(audio_bytes)
        
        result = detector.analyze(temp_filename, language)
        result['processingTime'] = round(time.time() - start_time, 3)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Processing error: {str(e)}"}), 500
    
    finally:
        if temp_filename and os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except:
                pass

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    print("="*60)
    print("🚀 AI Voice Detection API Starting...")
    print("="*60)
    print("📍 URL: http://localhost:5000")
    print("🔑 API Key: sk_test_123456789")
    print(f"🔧 Detector Version: {getattr(detector, 'version', 'unknown')}")
    print("="*60)
    print("✅ Ready to accept requests!")
    print()    
    app.run(debug=False, host='0.0.0.0', port=PORT)
