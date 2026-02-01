
# AI Voice Detection API
Detects AI-generated vs Human voices across 5 languages.
## Languages Supported
- Tamil
- English  
- Hindi
- Malayalam
- Telugu
## Setup
1. Create virtual environment:
```bash
   python -m venv venv
```
2. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Run the API:
```bash
   python app.py
```
5. Test the API:
```bash
   python test_api.py
```
## API Usage
**Endpoint:** `POST /api/voice-detection`
**Headers:**
# ai-voice-detection
AI-based system to detect real vs fake(AI-generated) voice samples.
