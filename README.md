# Streamlit LLM Chat with RAG

This small project demonstrates a simple **Streamlit** application that wraps a language model with a
**retrieval-augmented generation (RAG)** workflow and uses database to the conversations for long term memory.
management.

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup Environment**
   ```.env
   GEMINI_API_KEY=your-gemini-apikey
   
   ```
3. **Run the Streamlit app**
   ```bash
   streamlit run streamlit_app.py
   ```

## Screenshots
<img width="1364" height="643" alt="image" src="https://github.com/user-attachments/assets/bb1c1262-4e4a-4e9f-8807-89b709e7c0f9" />

It can recall the previous conversations when needed.
