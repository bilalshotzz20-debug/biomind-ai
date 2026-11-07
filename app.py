import streamlit as st
import os
from groq import Groq

# =====================================================
# 1. PAGE CONFIG & INITIALIZATION
# =====================================================
st.set_page_config(page_title="BioMind AI", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed")

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to BioMind. I am your AI medical assistant. Please describe your symptoms to begin the analysis."}
    ]

# =====================================================
# 2. FETCH API KEY (SECRETS OR SIDEBAR)
# =====================================================
try:
    SECRET_KEY = st.secrets["GROQ_API_KEY"]
except:
    SECRET_KEY = None

# =====================================================
# 3. DYNAMIC CSS (LIGHT & DARK MODES)
# =====================================================
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
    blob1 = "rgba(112, 0, 255, 0.15)"
    blob2 = "rgba(0, 240, 255, 0.1)"
else:
    bg_color = "#F8FAFC"
    text_color = "#0F172A" 
    muted_color = "#64748B"
    card_bg = "rgba(255, 255, 255, 0.9)"
    card_border = "rgba(0, 0, 0, 0.08)"
    chat_user_bg = "#E0E7FF" 
    chat_ai_bg = "#FFFFFF" 
    input_bg = "#FFFFFF" # Light mode input background
    glow = "rgba(139, 92, 246, 0.15)"
    blob1 = "rgba(139, 92, 246, 0.08)"
    blob2 = "rgba(6, 182, 212, 0.08)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
html, body, [class*="css"] {{ font-family: 'Outfit', sans-serif !important; }}
.stApp, .stMarkdown, p, span, li, h1, h2, h3, h4, h5, h6 {{ color: {text_color} !important; }}
.stApp {{ background-color: {bg_color}; transition: background-color 0.5s ease; overflow-x: hidden; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ max-width: 1100px; padding-top: 2rem; padding-bottom: 5rem; }}
[data-testid="stSidebar"] {{ background-color: {bg_color} !important; border-right: 1px solid {card_border}; }}
[data-testid="stSidebar"] * {{ color: {text_color} !important; }}

/* Background Blobs */
.blob {{ position: fixed; border-radius: 50%; filter: blur(80px); z-index: -1; animation: float 10s infinite ease-in-out alternate; }}
.blob1 {{ top: -10%; left: -10%; width: 400px; height: 400px; background: {blob1}; }}
.blob2 {{ bottom: -10%; right: -10%; width: 500px; height: 500px; background: {blob2}; animation-delay: -5s; }}
@keyframes float {{ 0% {{ transform: translate(0, 0) scale(1); }} 100% {{ transform: translate(30px, 50px) scale(1.1); }} }}

/* Toggle Button */
div[data-testid="stToggle"] {{ background: {card_bg}; padding: 10px 20px; border-radius: 50px; border: 1px solid {card_border}; backdrop-filter: blur(10px); width: fit-content; margin-left: auto; }}

/* Chat Messages */
[data-testid="stChatMessage"] {{ background: {card_bg}; border: 1px solid {card_border}; border-radius: 20px; padding: 24px; backdrop-filter: blur(20px); margin-bottom: 1.5rem; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05); transition: transform 0.3s ease, box-shadow 0.3s ease; animation: slideUp 0.4s ease-out; }}
[data-testid="stChatMessage"]:hover {{ transform: translateY(-3px); box-shadow: 0 12px 40px {glow}; }}
@keyframes slideUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {{ background: {chat_user_bg} !important; }}
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) {{ background: {chat_ai_bg} !important; }}

/* =========================================
   CHAT INPUT FIX (THE MAGIC HAPPENS HERE)
   ========================================= */
/* Remove default white background of the outer wrapper */
[data-testid="stChatInput"] {{ 
    background: transparent !important; 
    border: none !important;
}}

/* Style the actual input container */
[data-testid="stChatInput"] > div {{ 
    background: {input_bg} !important; 
    border: 1px solid {card_border} !important; 
    border-radius: 50px !important; 
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.3s ease;
}}

/* Style the text and placeholder */
[data-testid="stChatInput"] textarea {{ 
    color: {text_color} !important; 
    caret-color: {text_color} !important;
}}
[data-testid="stChatInput"] textarea::placeholder {{ 
    color: {muted_color} !important; 
    opacity: 1 !important;
}}

/* Style the send button */
[data-testid="stChatInput"] button {{ 
    color: {text_color} !important; 
}}
[data-testid="stChatInput"] button:hover {{ 
    background-color: {card_border} !important; 
}}

[data-testid="stChatInput"]:focus-within > div {{ 
    border-color: #8B5CF6 !important; 
    box-shadow: 0 0 20px {glow} !important; 
}}

/* Hero */
.hero {{ text-align: center; margin-bottom: 40px; animation: fadeIn 1s ease-out; }}
.hero h1 {{ font-size: 3.5rem; font-weight: 800; letter-spacing: -1.5px; background: linear-gradient(135deg, #8B5CF6 0%, #06B6D4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }}
.hero p {{ font-size: 1.1rem; color: {muted_color} !important; }}
@keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
</style>

<div class="blob blob1"></div>
<div class="blob blob2"></div>
""", unsafe_allow_html=True)

# =====================================================
# 4. TOP BAR (Theme Toggle)
# =====================================================
col1, col2 = st.columns([3, 1])
with col2:
    is_dark = st.toggle("🌙 Dark Mode", value=(st.session_state.theme == "dark"))
    if is_dark and st.session_state.theme == "light":
        st.session_state.theme = "dark"
        st.rerun()
    elif not is_dark and st.session_state.theme == "dark":
        st.session_state.theme = "light"
        st.rerun()

# =====================================================
# 5. HERO SECTION
# =====================================================
st.markdown("""
<div class="hero">
    <h1>BioMind AI</h1>
    <p>Advanced Medical Diagnostics & Disease Detective Engine</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# 6. CHAT INTERFACE
# =====================================================
for message in st.session_state.messages:
    avatar = "🧬" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# =====================================================
# 7. SIDEBAR & KEY LOGIC
# =====================================================
api_key_input = ""
with st.sidebar:
    st.markdown("### ⚙️ System Config")
    if SECRET_KEY:
        st.success("✅ API Key loaded securely from Streamlit Secrets.")
        api_key_input = SECRET_KEY
    else:
        st.warning("⚠️ API Key not found in Secrets. Please enter manually.")
        api_key_input = st.text_input("Groq API Key", type="password", placeholder="gsk_...")

# Input logic
if prompt := st.chat_input("Describe your symptoms here (e.g., fever, sore throat...)"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🧬"):
        if not api_key_input:
            st.error("⚠️ API Key missing. Please check Streamlit Secrets or enter it in the sidebar.")
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
