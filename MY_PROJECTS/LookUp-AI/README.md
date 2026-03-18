# LookUp AI — Visual Intelligence Platform

A full-stack web application built with **Flask** (backend) and **Streamlit** (alternative UI), powered by **Google Gemini 2.5 Flash** for AI image analysis.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      LookUp AI                           │
│                                                         │
│  ┌──────────────────┐        ┌────────────────────┐    │
│  │  Flask Backend   │        │  Streamlit UI       │    │
│  │  :5000           │◄──────►│  :8501             │    │
│  │                  │        │                    │    │
│  │  /api/analyze    │        │  Camera / Upload   │    │
│  │  /api/save       │        │  AI Results View   │    │
│  │  /api/history    │        │  History Panel     │    │
│  │  /api/status     │        └────────────────────┘    │
│  │                  │        ┌────────────────────┐    │
│  │  templates/      │        │  Custom HTML UI    │    │
│  │  index.html      │        │  (browser cam)     │    │
│  └──────────────────┘        └────────────────────┘    │
│           │                                             │
│           ▼                                             │
│  ┌──────────────────┐                                   │
│  │  Google Gemini   │                                   │
│  │  2.5 Flash API   │                                   │
│  └──────────────────┘                                   │
└─────────────────────────────────────────────────────────┘
```

---

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

Get a free Gemini API key at: https://aistudio.google.com/app/apikey

---

## Running the Application

### Option A: Flask Web App (Recommended)

Runs a full-featured browser-based UI with live webcam access:

```bash
python app.py
```

Then open: **http://localhost:5000**

**Controls:**
- `S` — Capture frame
- `Y` — Analyze with AI
- `N` — Save image only
- `C` — Retake / cancel

### Option B: Streamlit UI

Requires the Flask backend to be running first.

**Terminal 1:**
```bash
python app.py
```

**Terminal 2:**
```bash
streamlit run streamlit_app.py
```

Then open: **http://localhost:8501**

---

## Features

| Feature | Flask UI | Streamlit UI |
|---------|----------|--------------|
| Live webcam capture | ✅ | ✅ (via browser) |
| Image file upload | ✅ | ✅ |
| Gemini AI analysis | ✅ | ✅ |
| Save without AI | ✅ | ✅ |
| Text-to-speech | ✅ (browser TTS) | — |
| Scan history | ✅ | ✅ |
| Keyboard shortcuts | ✅ | — |
| Dark UI with HUD | ✅ | ✅ |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web app |
| `/api/analyze` | POST | Analyze image with Gemini AI |
| `/api/save` | POST | Save image without AI |
| `/api/history` | GET | Get scan history (last 20) |
| `/api/status` | GET | Server health + config check |
| `/captures/<file>` | GET | Serve saved capture files |

### Example API Usage

```python
import requests, base64
from PIL import Image
from io import BytesIO

# Load image
img = Image.open("photo.jpg")
buf = BytesIO()
img.save(buf, format="JPEG")
b64 = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

# Analyze
response = requests.post("http://localhost:5000/api/analyze", json={"image": b64})
print(response.json()["description"])
```

---

## Project Structure

```
lookup_ai/
├── app.py              # Flask backend + API routes
├── streamlit_app.py    # Streamlit UI (connects to Flask)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .env                # Your API keys (gitignored)
├── history.txt         # Scan log (auto-created)
├── captures/           # Saved images (auto-created)
└── templates/
    └── index.html      # Flask HTML frontend
```

---

## Troubleshooting

**Camera not working in Flask UI?**
→ Use HTTPS or localhost (browsers restrict camera on HTTP)
→ Switch to Upload mode as fallback

**Gemini API error?**
→ Check your API key in `.env`
→ Ensure `GEMINI_API_KEY` is set correctly

**Streamlit can't reach Flask?**
→ Make sure Flask is running on port 5000 before starting Streamlit
→ Check `FLASK_URL` in `streamlit_app.py`
