import streamlit as st
import os
from groq import Groq

# =====================================================
# 1. PAGE CONFIG & ULTRA PREMIUM UI
# =====================================================
st.set_page_config(page_title="BioMind AI", page_icon="🧬", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

:root {
    --primary: #00F0FF;
    --secondary: #7000FF;
    --bg-color: #050505;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 15% 50%, rgba(112, 0, 255, 0.08), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(0, 240, 255, 0.08), transparent 25%),
                #050505;
    color: #E2E8F0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 900px; padding-top: 2rem; }

/* --- SIDEBAR --- */
[data-testid="stSidebar"] {
    background: rgba(10, 10, 15, 0.95);
    border-right: 1px solid rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
}

/* --- CHAT BUBBLES --- */
[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    transition: 0.3s;
}

[data-testid="stChatMessage"]:hover {
    border-color: rgba(0, 240, 255, 0.2);
}

/* --- CHAT INPUT --- */
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 20px !important;
    padding: 10px !important;
    color: white !important;
    box-shadow: 0 0 20px rgba(0,0,0,0.5) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 15px rgba(0, 240, 255, 0.2) !important;
}

/* --- TEXT --- */
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #00F0FF 0%, #7000FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}
.hero-subtitle {
    text-align: center;
    color: #888;
    font-size: 1.1rem;
    margin-bottom: 40px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 2. SIDEBAR (API KEY CONFIG)
# =====================================================
with st.sidebar:
    st.markdown("### ⚙️ Engine Configuration")
    st.markdown("To chat with BioMind, enter your free Groq API Key below.")
    api_key_input = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    
    st.divider()
    st.markdown("""
    **⚠️ Medical Disclaimer**
    
    BioMind is an AI diagnostic assistant. It can make mistakes. Always consult a real doctor for medical emergencies.
    """)

# =====================================================
# 3. MAIN CHAT INTERFACE
# =====================================================
st.markdown('<div class="hero-title">🧬 BioMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Advanced Rare Disease Detective & Neural Diagnostician</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I am BioMind. Please describe your symptoms in detail, and I will analyze them to suggest potential conditions and next steps."}
    ]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🩺" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Describe your symptoms here (e.g., fever, rash, joint pain...)"):
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant", avatar="🩺"):
        if not api_key_input:
            st.error("⚠️ Please enter your Groq API Key in the sidebar to start the diagnosis.")
            st.stop()
            
        try:
            client = Groq(api_key=api_key_input)
            
            # System Prompt for Medical Logic
            system_prompt = """
            You are BioMind, a senior AI medical diagnostician.
            A patient comes to you with symptoms. Analyze them and provide a structured medical report.
            
            You MUST format your response exactly like this using Markdown:
            
            ### 🦠 Top Possible Conditions
            1. [Condition 1]
            2. [Condition 2]
            3. [Condition 3]
            
            ### 🧠 Medical Reasoning
            [Briefly explain why these conditions match the symptoms]
            
            ### 🚨 Urgency Level
            **[Low / Medium / High]** - [1 sentence explaining the urgency]
            
            ### 🧪 Next Steps & Tests
            *   [Test 1 to ask a doctor]
            *   [Test 2 to ask a doctor]
            
            *Disclaimer: I am an AI, not a doctor. Please consult a medical professional immediately.*
            """
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model="openai/gpt-oss-120b",
                temperature=0.3, # Lower temperature for more medical accuracy
            )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            
            # Save response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
