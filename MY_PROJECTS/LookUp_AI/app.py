import cv2
import os
import textwrap
import pyttsx3
from datetime import datetime
from PIL import Image
from google import genai
from dotenv import load_dotenv

# --- CONFIGURATION & SECURITY ---
load_dotenv()  # Loads variables from .env file
API_KEY = os.getenv("GEMINI_API_KEY")
SAVE_DIR = "captures"
HISTORY_FILE = "history.txt"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Initialize Gemini Client
client = genai.Client(api_key=API_KEY)

# --- UI & UTILITY FUNCTIONS ---

def draw_ui(img, text, status, sub_text=""):
    """Renders the HUD/Overlay on the image."""
    h, w, _ = img.shape
    overlay = img.copy()
    # Darken bottom area for text readability
    cv2.rectangle(overlay, (0, h - 250), (w, h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)
    
    # Status Indicators
    color = (0, 255, 0) if "READY" in status else (0, 165, 255)
    cv2.putText(img, f"STATUS: {status}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    if sub_text:
        cv2.putText(img, sub_text, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Text Wrapping for AI Descriptions
    wrapped_lines = textwrap.wrap(text, width=70) 
    y_entry = h - 220
    for line in wrapped_lines[:8]:
        cv2.putText(img, line, (20, y_entry), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        y_entry += 25

def speak(text):
    """Text-to-Speech engine."""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        del engine
    except Exception as e:
        print(f"TTS Error: {e}")

def save_to_history(description):
    """Logs AI descriptions to a text file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n{description}\n" + "-"*30 + "\n")
    except Exception as e:
        print(f"❌ History File Error: {e}")

def get_ai_description(pil_img):
    """Sends image to Gemini API."""
    prompt = (
        "Identify the main subject. IF it is a renowned/famous person, "
        "provide a detailed biography of at least 100 words. "
        "OTHERWISE, provide a brief 2-sentence description. No markdown."
    )
    # Using gemini-2.5-flash for high speed/low latency
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=[prompt, pil_img]
    )
    return response.text

# --- CORE LOGIC ---

def handle_user_choice(frame):
    """Freezes the frame and waits for user interaction."""
    freeze_frame = frame.copy()
    
    while True:
        choice_img = freeze_frame.copy()
        draw_ui(choice_img, "IMAGE CAPTURED", "AWAITING CHOICE", 
                sub_text="[Y] Get AI Info | [N] Save Image Only | [C] Cancel")
        cv2.imshow("LookUp_AI", choice_img)
        
        c_key = cv2.waitKey(0) & 0xFF 
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if c_key == ord('y'):
            # Show Analyzing State
            loading_img = freeze_frame.copy()
            draw_ui(loading_img, "Consulting AI...", "ANALYZING...")
            cv2.imshow("LookUp_AI", loading_img)
            cv2.waitKey(1)

            # Convert BGR (OpenCV) to RGB (PIL)
            rgb_frame = cv2.cvtColor(freeze_frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)
            
            try:
                description = get_ai_description(pil_img)
                
                # Update UI and Save
                final_frame = freeze_frame.copy()
                draw_ui(final_frame, description, "AI SPEAKING...")
                cv2.imshow("LookUp_AI", final_frame)
                cv2.waitKey(100)
                
                cv2.imwrite(os.path.join(SAVE_DIR, f"ai_scan_{ts}.jpg"), final_frame)
                save_to_history(description)
                speak(description)
                return description
            except Exception as e:
                return f"Error: {e}"

        elif c_key == ord('n'):
            cv2.imwrite(os.path.join(SAVE_DIR, f"raw_save_{ts}.jpg"), freeze_frame)
            return "Image saved directly (No AI)."

        elif c_key == ord('c'):
            return "Action cancelled."

# --- MAIN LOOP ---

cap = cv2.VideoCapture(0)
display_text = "Press 'S' to Capture"
status_msg = "READY"

print("LookUp_AI is running. Press 'S' to capture, 'Q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret: break

    display_frame = frame.copy()
    draw_ui(display_frame, display_text, status_msg)
    cv2.imshow("LookUp_AI", display_frame)
    
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        display_text = handle_user_choice(frame)
        status_msg = "READY"
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()