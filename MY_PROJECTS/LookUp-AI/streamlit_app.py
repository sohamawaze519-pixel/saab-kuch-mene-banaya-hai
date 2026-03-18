"""
LookUp AI — Streamlit Companion App
An alternative UI using Streamlit that connects to the Flask backend.
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import requests
import base64
import json
from datetime import datetime
from PIL import Image
from io import BytesIO

# --- CONFIG ---
FLASK_URL = "http://localhost:5000"

st.set_page_config(
    page_title="LookUp AI",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Mono', monospace;
    background-color: #08090c;
    color: #e8eaf0;
}

.stApp { background-color: #08090c; }

.main-header {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: #e8eaf0;
    margin-bottom: 0;
    letter-spacing: -1px;
}

.main-header span { color: #00e5ff; }

.subtitle {
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    color: #6b7280;
    margin-bottom: 2rem;
    text-transform: uppercase;
}

.result-card {
    background: #0f1117;
    border: 1px solid #1e2130;
    border-radius: 6px;
    padding: 20px;
    margin: 12px 0;
    font-size: 0.85rem;
    line-height: 1.7;
    color: #e8eaf0;
}

.result-card.ai { border-left: 3px solid #00e5ff; }
.result-card.saved { border-left: 3px solid #10b981; }
.result-card.error { border-left: 3px solid #ef4444; }

.timestamp {
    font-size: 0.7rem;
    color: #00e5ff;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
}

.history-item {
    background: #0f1117;
    border: 1px solid #1e2130;
    border-radius: 4px;
    padding: 12px;
    margin: 8px 0;
    font-size: 0.75rem;
    line-height: 1.5;
    color: #9ca3af;
    cursor: pointer;
}

.status-bar {
    background: #0f1117;
    border: 1px solid #1e2130;
    border-radius: 4px;
    padding: 10px 16px;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    color: #6b7280;
    display: flex;
    gap: 20px;
    margin-bottom: 16px;
}

.kbd {
    display: inline-block;
    background: #161820;
    border: 1px solid #374151;
    border-radius: 3px;
    padding: 1px 6px;
    font-size: 0.7rem;
    color: #9ca3af;
}

div[data-testid="stButton"] button {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# --- HELPERS ---
def pil_to_base64(pil_img):
    buffer = BytesIO()
    pil_img.save(buffer, format="JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode()

def call_backend_analyze(image_b64: str):
    try:
        res = requests.post(
            f"{FLASK_URL}/api/analyze",
            json={"image": image_b64},
            timeout=60
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def call_backend_save(image_b64: str):
    try:
        res = requests.post(
            f"{FLASK_URL}/api/save",
            json={"image": image_b64},
            timeout=15
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def get_history():
    try:
        res = requests.get(f"{FLASK_URL}/api/history", timeout=10)
        return res.json().get("history", [])
    except:
        return []

def get_status():
    try:
        res = requests.get(f"{FLASK_URL}/api/status", timeout=5)
        return res.json()
    except:
        return {"status": "offline", "gemini_configured": False, "captures_count": 0}

# --- STATE ---
if "result" not in st.session_state:
    st.session_state.result = None
if "captured_image" not in st.session_state:
    st.session_state.captured_image = None

# --- HEADER ---
st.markdown('<div class="main-header">Lookup<span>AI</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Visual Intelligence Platform · Flask + Streamlit</div>', unsafe_allow_html=True)

# Status bar
status = get_status()
gemini_ok = "✓ GEMINI READY" if status.get("gemini_configured") else "✗ NO API KEY"
flask_ok = "✓ FLASK ONLINE" if status.get("status") == "running" else "✗ FLASK OFFLINE"
st.markdown(f"""
<div class="status-bar">
  <span>{flask_ok}</span>
  <span>{gemini_ok}</span>
  <span>{status.get("captures_count", 0)} CAPTURES</span>
  <span style="margin-left:auto; color:#374151">{datetime.now().strftime("%H:%M:%S")}</span>
</div>
""", unsafe_allow_html=True)

# --- LAYOUT ---
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    st.markdown("#### 📷 Image Input")

    input_mode = st.radio(
        "Input Mode", ["📷 Webcam Snapshot", "📁 Upload Image"],
        horizontal=True, label_visibility="collapsed"
    )

    if "Upload" in input_mode:
        uploaded = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed"
        )
        if uploaded:
            pil_img = Image.open(uploaded).convert("RGB")
            st.session_state.captured_image = pil_img
            st.image(pil_img, use_column_width=True, caption="Uploaded Image")
    else:
        snap = st.camera_input("Take a snapshot", label_visibility="collapsed")
        if snap:
            pil_img = Image.open(snap).convert("RGB")
            st.session_state.captured_image = pil_img

    if st.session_state.captured_image:
        st.markdown("---")
        st.markdown("**Actions:**")
        btn_col1, btn_col2, btn_col3 = st.columns(3)

        with btn_col1:
            if st.button("🤖 Analyze with AI", use_container_width=True, type="primary"):
                with st.spinner("Consulting Gemini AI..."):
                    b64 = pil_to_base64(st.session_state.captured_image)
                    result = call_backend_analyze(b64)
                    st.session_state.result = result

        with btn_col2:
            if st.button("💾 Save Image Only", use_container_width=True):
                with st.spinner("Saving..."):
                    b64 = pil_to_base64(st.session_state.captured_image)
                    result = call_backend_save(b64)
                    if result.get("success"):
                        st.success(f"Saved: {result.get('image_file', '')}")
                    else:
                        st.error(result.get("error", "Save failed"))

        with btn_col3:
            if st.button("🔄 Clear", use_container_width=True):
                st.session_state.captured_image = None
                st.session_state.result = None
                st.rerun()

with col_right:
    st.markdown("#### 🧠 AI Analysis")

    # Show result
    if st.session_state.result:
        res = st.session_state.result
        if res.get("success"):
            st.markdown(f'<div class="timestamp">▸ {res.get("timestamp", "")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-card ai">{res.get("description", "")}</div>', unsafe_allow_html=True)
            if res.get("image_file"):
                st.markdown(f'<small style="color:#6b7280">Saved as: {res["image_file"]}</small>', unsafe_allow_html=True)
        elif res.get("error"):
            st.markdown(f'<div class="result-card error">Error: {res["error"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-card" style="color:#374151; text-align:center; padding: 40px 20px;">
            <div style="font-size:2rem; margin-bottom:12px;">👁</div>
            AWAITING IMAGE
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📋 Scan History")

    history = get_history()
    if history:
        for item in history[:8]:
            with st.expander(item.get("header", "Unknown"), expanded=False):
                st.markdown(f'<div style="font-size:0.8rem; color:#9ca3af; line-height:1.6">{item.get("description", "")}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#374151; font-size:0.75rem; padding:12px; letter-spacing:0.1em">NO HISTORY YET</div>', unsafe_allow_html=True)

    if st.button("↺ Refresh History", use_container_width=True):
        st.rerun()

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="font-size:0.7rem; color:#374151; letter-spacing:0.1em; text-align:center; padding:8px 0;">
  LOOKUP AI · FLASK BACKEND ON :5000 · STREAMLIT UI ON :8501 · POWERED BY GEMINI 2.5 FLASH
</div>
""", unsafe_allow_html=True)
