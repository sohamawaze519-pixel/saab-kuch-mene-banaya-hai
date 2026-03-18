import os
import base64
import textwrap
import uuid
from datetime import datetime
from io import BytesIO

from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
SAVE_DIR = "captures"
HISTORY_FILE = "history.txt"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

app = Flask(__name__)

# --- GEMINI AI ---
def get_ai_description(pil_img):
    """Sends image to Gemini API and returns description."""
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)
        prompt = (
            "Identify the main subject. IF it is a renowned/famous person, "
            "provide a detailed biography of at least 100 words. "
            "OTHERWISE, provide a brief 2-sentence description. No markdown."
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, pil_img]
        )
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

def save_to_history(description, image_filename=""):
    """Logs AI descriptions to a text file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {image_filename}\n{description}\n" + "-"*40 + "\n")
    except Exception as e:
        print(f"History File Error: {e}")

def pil_to_base64(pil_img):
    """Convert PIL image to base64 string."""
    buffer = BytesIO()
    pil_img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

# --- ROUTES ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/captures/<path:filename>")
def serve_capture(filename):
    return send_from_directory(SAVE_DIR, filename)

@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Analyze image with Gemini AI."""
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    try:
        # Decode base64 image
        img_data = data["image"]
        if "," in img_data:
            img_data = img_data.split(",")[1]
        img_bytes = base64.b64decode(img_data)
        pil_img = Image.open(BytesIO(img_bytes)).convert("RGB")

        # Get AI description
        description = get_ai_description(pil_img)

        # Save image
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:6]
        filename = f"ai_scan_{ts}_{unique_id}.jpg"
        filepath = os.path.join(SAVE_DIR, filename)
        pil_img.save(filepath, quality=90)

        # Save to history
        save_to_history(description, filename)

        return jsonify({
            "success": True,
            "description": description,
            "image_file": filename,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/save", methods=["POST"])
def save_image():
    """Save image without AI analysis."""
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    try:
        img_data = data["image"]
        if "," in img_data:
            img_data = img_data.split(",")[1]
        img_bytes = base64.b64decode(img_data)
        pil_img = Image.open(BytesIO(img_bytes)).convert("RGB")

        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:6]
        filename = f"raw_save_{ts}_{unique_id}.jpg"
        filepath = os.path.join(SAVE_DIR, filename)
        pil_img.save(filepath, quality=90)

        return jsonify({
            "success": True,
            "message": "Image saved successfully (no AI analysis).",
            "image_file": filename,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/history", methods=["GET"])
def get_history():
    """Return scan history."""
    try:
        if not os.path.exists(HISTORY_FILE):
            return jsonify({"history": []})

        entries = []
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        blocks = content.strip().split("-"*40)
        for block in reversed(blocks):
            block = block.strip()
            if not block:
                continue
            lines = block.strip().split("\n")
            if lines:
                header = lines[0]
                description = "\n".join(lines[1:]).strip()
                entries.append({
                    "header": header,
                    "description": description
                })

        return jsonify({"history": entries[:20]})  # last 20
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/status", methods=["GET"])
def status():
    """Health check and config status."""
    return jsonify({
        "status": "running",
        "gemini_configured": bool(API_KEY),
        "captures_count": len([f for f in os.listdir(SAVE_DIR) if f.endswith(".jpg")]) if os.path.exists(SAVE_DIR) else 0
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
