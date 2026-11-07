import streamlit as st
import os
from groq import Groq

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="BioMind AI | Medical Diagnostician", page_icon="🧬", layout="wide")

# --- CUSTOM CSS FOR PREMIUM MEDICAL LOOK ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: radial-gradient(circle at top right, #0F172A 0%, #020617 100%);
        color: #E2E8F0;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #94A3B8;
        margin-top: 5px;
        margin-bottom: 30px;
        font-weight: 300;
    }
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .stTextArea textarea {
        background-color: rgba(0,0,0,0.2) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        color: white !important;
        font-size: 16px !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #0EA5E9 0%, #6366F1 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        border-radius: 8px;
        padding: 12px 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR FOR API KEY ---
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.info("To use this AI, you need a free Groq API Key.")
    api_key_input = st.text_input("Enter your Groq API Key:", type="password", help="Get your free key at console.groq.com")
    
    st.divider()
    st.markdown("""
    **Disclaimer:** 
    BioMind is an AI assistant, not a real doctor. Always consult a medical professional for actual diagnosis.
    """)

# --- HEADER ---
st.markdown('<div class="hero-title">🧬 BioMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Advanced Rare Disease Detective & Medical Diagnostician</div>', unsafe_allow_html=True)

# --- MAIN UI ---
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Patient Symptoms")
    st.markdown("Describe the symptoms in detail (e.g., duration, severity, location).")
    
    symptoms = st.text_area(
        "Enter symptoms here:", 
        height=200, 
        placeholder="Example: Patient has a high fever of 102F for 3 days, severe joint pain, and small red spots on the arms..."
    )
    
    analyze_btn = st.button("🔍 Analyze Symptoms")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
    st.markdown("### 🧠 AI Diagnostic Report")
    
    if analyze_btn:
        if not api_key_input:
            st.error("⚠️ Please enter your Groq API Key in the sidebar first.")
        elif not symptoms:
            st.warning("⚠️ Please enter some symptoms to analyze.")
        else:
            with st.spinner("Analyzing medical database and generating report..."):
                try:
                    # Initialize Groq client
                    client = Groq(api_key=api_key_input)
                    
                    prompt = f"""
                    You are BioMind, a senior AI medical diagnostician.
                    A patient comes to you with the following symptoms: {symptoms}
                    
                    Based on your medical knowledge, analyze these symptoms. 
                    Provide your answer in this exact format:
                    1. Top 3 Possible Conditions (List them)
                    2. Why these conditions fit (Brief explanation)
                    3. Urgency Level (Low / Medium / High)
                    4. Next Steps (What tests the patient should ask a doctor for)
                    
                    Important: Add a disclaimer that you are an AI and not a real doctor.
                    """
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="openai/gpt-oss-120b",
                    )
                    
                    report = chat_completion.choices[0].message.content
                    
                    st.success("Analysis Complete!")
                    st.markdown(report)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 50px 20px; color: #64748B;">
            <h1 style="font-size: 50px;">🩺</h1>
            <p>Enter symptoms on the left and click Analyze to see the AI report.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)