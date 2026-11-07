import streamlit as st
import os
from groq import Groq

# =====================================================
# 1. PAGE CONFIG
# =====================================================
st.set_page_config(page_title="BioMind AI | Command Center", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

# =====================================================
# 2. ULTRA MODERN UI (CSS)
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #050508;
    --surface: rgba(20, 20, 25, 0.6);
    --primary: #00F0FF;
    --secondary: #7000FF;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
    --border: rgba(255, 255, 255, 0.08);
}

/* Global App & Background */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
}
.stApp {
    background-color: var(--bg);
    background-image: 
        radial-gradient(circle at 10% 20%, rgba(0, 240, 255, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(112, 0, 255, 0.08) 0%, transparent 40%);
    color: var(--text-main);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 1000px; padding-top: 2rem; padding-bottom: 5rem; }

/* Custom Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: rgba(10, 10, 15, 0.95);
    border-right: 1px solid var(--border);
    backdrop-filter: blur(20px);
}
.sidebar-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: white;
    margin-bottom: 5px;
}
.sidebar-sub {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-bottom: 25px;
}
.status-dot {
    height: 8px;
    width: 8px;
    background-color: #10B981;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 10px #10B981;
    margin-right: 8px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
    70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* Chat Container */
[data-testid="stChatMessage"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 20px 24px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
[data-testid="stChatMessage"]:hover {
    border-color: rgba(0, 240, 255, 0.3);
    transform: translateY(-2px);
}

/* Chat Input (Capsule Style) */
[data-testid="stChatInput"] {
    background: rgba(15, 15, 20, 0.9) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 50px !important;
    padding: 8px 16px !important;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    transition: 0.3s;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.2) !important;
}

/* Hero Header */
.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(120deg, #00F0FF 0%, #7000FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
    letter-spacing: -1px;
}
.hero-subtitle {
    font-size: 1rem;
    color: var(--text-muted);
    margin-bottom: 30px;
    font-weight: 400;
    letter-spacing: 0.5px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. SIDEBAR (Controls & Status)
# =====================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ System Config</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Secure API Authentication</div>', unsafe_allow_html=True)
    
    api_key_input = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    
    st.divider()
    
    st.markdown(f'<div style="font-size: 0.8rem; color: var(--text-muted);"><span class="status-dot"></span> Neural Engine Online</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 8px;">Model: <b>Llama-3-70B</b></div>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown("""
    <div style="background: rgba(255, 50, 50, 0.1); border-left: 3px solid #FF3232; padding: 10px; border-radius: 4px;">
        <div style="font-size: 0.75rem; color: #FFA0A0;">
            <b>Disclaimer:</b> BioMind is an AI. It cannot replace professional medical advice.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 4. MAIN INTERFACE
# =====================================================
st.markdown('<div class="hero-title">BioMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Advanced Medical Diagnostics & Disease Detective</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to BioMind. I am your AI medical assistant. Please describe your symptoms, their duration, and any relevant details."}
    ]

# Display chat messages
for message in st.session_state.messages:
    avatar = "🧬" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Describe your symptoms (e.g., persistent cough, fever...)"):
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant", avatar="🧬"):
        if not api_key_input:
            st.error("⚠️ API Key missing. Please enter your Groq API Key in the sidebar.")
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
