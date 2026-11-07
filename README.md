# 🧬 BioMind AI: Advanced Rare Disease Detective

An end-to-end Generative AI web application designed to assist in the early detection of rare diseases and complex medical conditions. Built to act as an intelligent diagnostic assistant for patients and healthcare professionals globally.

🔗 **Live Demo:** [Add your Streamlit Link Here]

## 🌍 The Global Problem
Worldwide, over 300 million people suffer from rare diseases. Because these conditions are uncommon, they are frequently misdiagnosed or take years to identify. Patients often visit multiple specialists, spending thousands of dollars while their health deteriorates. Access to specialized medical knowledge is highly unequal globally.

## 💡 The Solution
**BioMind AI** bridges this gap. It uses advanced Large Language Models (LLMs) to analyze a patient's reported symptoms and cross-references them with vast medical knowledge in real-time. It acts as a "second opinion" tool that suggests potential rare conditions, explains the reasoning, and recommends specific medical tests.

## 🚀 Key Features
*   **Intelligent Symptom Analysis:** Converts unstructured text (symptoms) into structured medical hypotheses.
*   **Actionable Insights:** Provides the top 3 possible conditions, urgency levels, and next steps (tests to request from a doctor).
*   **Ultra-Fast Inference:** Powered by Groq's LPU inference engine, generating complex medical reports in under 2 seconds.
*   **Premium Glassmorphism UI:** A sleek, dark-mode medical dashboard built with Streamlit.
*   **Secure Architecture:** Users input their own API keys via a secure sidebar, ensuring privacy and zero backend costs.

## 🛠️ Tech Stack
*   **Frontend:** Streamlit (Custom CSS for Glassmorphism UI)
*   **AI Engine:** Groq API (Running `openai/gpt-oss-120b` / Llama 3 models)
*   **Language:** Python
*   **Libraries:** `groq`, `streamlit`

## 💻 How to Run This Project Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/biomind-ai.git
