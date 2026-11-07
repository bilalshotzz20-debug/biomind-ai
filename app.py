import streamlit as st
import os
from groq import Groq
import time

# =====================================================
# 1. PAGE CONFIG & INITIALIZATION
# =====================================================
st.set_page_config(page_title="BioMind AI", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed")

# Initialize Theme State
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to BioMind. I am your AI medical assistant. Please describe your symptoms to begin the analysis."}
    ]

# =====================================================
# 2. DYNAMIC CSS (LIGHT & DARK MODES)
# =====================================================
# Colors based on screenshots (Vibrant Purple/Cyan for dark, Soft Pastel/White for light)
if st.session_state.theme == "dark":
    bg_color = "#050508"
    text_color = "#F8FAFC"
    muted_color = "#94A3B8"
    card_bg = "rgba(20, 20, 25, 0.6)"
    card_border = "rgba(255, 255, 255, 0.08)"
    chat_user_bg = "rgba(112, 0, 255, 0.2)"
    chat_ai_bg = "rgba(0, 240, 255, 0.05)"
    input_bg = "rgba(15, 15, 20, 0.9)"
    glow = "rgba(0, 240, 255, 0.2)"
else:
    bg_color = "#F8FAFC"
    text_color = "#1E293B"
    muted_color = "#64748B"
    card_bg = "rgba(255, 255, 255, 0.8)"
    card_border = "rgba(0, 0, 0, 0.05)"
    chat_user_bg = "rgba(139, 92, 246, 0.15)"
    chat_ai_bg = "rgba(14, 165, 233, 0.1)"
    input_bg = "rgba(255, 255, 255, 0.9)"
    glow = "rgba(139, 92, 246, 0.15)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

/* --- GLOBAL --- */
html, body, [class*="css"] {{
    font-family: 'Outfit', sans-serif !important;
}}
.stApp {{
    background-color: {bg_color};
    color: {text_color};
    transition: background-color 0.5s ease, color 0.5s ease;
    overflow-x: hidden;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ max-width: 1100px; padding-top: 2rem; padding-bottom: 5rem; }}

/* --- ANIMATED BACKGROUND BLOBS (Like Canva/Grow) --- */
.blob {{
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    z-index: -1;
    animation: float 10s infinite ease-in-out alternate;
}}
.blob1 {{
    top: -10%; left: -10%; width: 400px; height: 400px;
    background: rgba(112, 0, 255, 0.15);
}}
.blob2 {{
    bottom: -10%; right: -10%; width: 500px; height: 500px;
    background: rgba(0, 240, 255, 0.1);
    animation-delay: -5s;
}}
@keyframes float {{
    0% {{ transform: translate(0, 0) scale(1); }}
    100% {{ transform: translate(30px, 50px) scale(1.1); }}
}}

/* --- ANIMATED TOGGLE BUTTON --- */
div[data-testid="stToggle"] {{
    background: {card_bg};
    padding: 10px 20px;
    border-radius: 50px;
    border: 1px solid {card_border};
    backdrop-filter: blur(10px);
    width: fit-content;
    margin-left: auto;
}}
div[data-testid="stToggle"] label p {{
    font-weight: 600 !important;
    color: {text_color} !important;
}}

/* --- CHAT MESSAGES (GLASSMORPHISM) --- */
[data-testid="stChatMessage"] {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 20px;
    padding: 24px;
    backdrop-filter: blur(20px);
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: slideUp 0.4s ease-out;
}}
[data-testid="stChatMessage"]:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 40px {glow};
}}
@keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* User and AI specific styling */
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {{
    background: {chat_user_bg};
}}
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) {{
    background: {chat_ai_bg};
}}

/* --- CHAT INPUT (CAPSULE) --- */
[data-testid="stChatInput"] {{
    background: {input_bg} !important;
    border: 1px solid {card_border} !important;
    border-radius: 50px !important;
    padding: 10px 20px !important;
    backdrop-filter: blur(20px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.3s ease;
}}
[data-testid="stChatInput"]:focus-within {{
    border-color: #8B5CF6 !important;
    box-shadow: 0 0 20px {glow} !important;
}}

/* --- HERO TYPOGRAPHY --- */
.hero {{
    text-align: center;
    margin-bottom: 40px;
    animation: fadeIn 1s ease-out;
}}
.hero h1 {{
    font-size: 3.5rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    background: linear-gradient(135deg, #8B5CF6 0%, #06B6D4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}}
.hero p {{
    font-size: 1.1rem;
    color: {muted_color};
}}
@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}
</style>

<!-- Background Blobs -->
<div class="blob blob1"></div>
<div class="blob blob2"></div>
""", unsafe_allow_html=True)

# =====================================================
# 3. TOP BAR (Theme Toggle)
# =====================================================
col1, col2 = st.columns([3, 1])
with col2:
    # Animated Toggle Switch
    is_dark = st.toggle("🌙 Dark Mode", value=(st.session_state.theme == "dark"))
    if is_dark and st.session_state.theme == "light":
        st.session_state.theme = "dark"
        st.rerun()
    elif not is_dark and st.session_state.theme == "dark":
        st.session_state.theme = "light"
        st.rerun()

# =====================================================
# 4. HERO SECTION
# =====================================================
st.markdown("""
<div class="hero">
    <h1>BioMind AI</h1>
    <p>Advanced Medical Diagnostics & Disease Detective Engine</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# 5. CHAT INTERFACE
# =====================================================
for message in st.session_state.messages:
    avatar = "🧬" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# API Key Check (Hidden in sidebar for clean UI)
with st.sidebar:
    st.markdown("### ⚙️ System Config")
    # Put your actual key here or ask in sidebar
    api_key_input = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    st.markdown("*Enter your key to activate the AI engine.*")

# Input logic
if prompt := st.chat_input("Describe your symptoms here..."):
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant", avatar="🧬"):
        if not api_key_input:
            st.error("⚠️ Please enter your Groq API Key in the sidebar.")
            st.stop()
            
        with st.spinner("Analyzing medical database..."):
            try:
                client = Groq(api_key=api_key_input)
                
                system_prompt = """
                You are BioMind, an elite AI medical diagnostician.
                Analyze the patient's symptoms and provide a structured, professional medical report.
                
                YOU MUST FORMAT YOUR RESPONSE EXACTLY LIKE THIS USING MARKDOWN:

                ### 🦠 Top Possible Conditions
                **1. [Condition Name]**
                *Why it fits:* [1 sentence explanation]

                **2. [Condition Name]**
                *Why it fits:* [1 sentence explanation]

                **3. [Condition Name]**
                *Why it fits:* [1 sentence explanation]

                ### 🚨 Urgency Level
                **[Low / Medium / High]**
                [1 sentence explaining the urgency]

                ### 🧪 Recommended Next Steps
                *   **[Test Name]:** [Why this test is needed]
                *   **[Action]:** [E.g., Consult a specialist]

                ---
                *⚕️ Disclaimer: I am an AI assistant. This is not a substitute for professional medical diagnosis. Please consult a doctor immediately.*
                """
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    model="openai/gpt-oss-120b",
                    temperature=0.2, 
                )
                
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")
