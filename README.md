# Streamlit LLM Chat with RAG

This small project demonstrates a simple **Streamlit** application that wraps a language model with a
**retrieval-augmented generation (RAG)** workflow and uses Streamlit's session state for conversation
management.

## Features

- 🧠 **Chat interface** built with Streamlit
- 📚 **RAG** using a FAISS vector store built over local documents (`docs/` folder)
- 🗃️ **Session management** via `st.session_state`; maintains history across interactions
- 🔄 **Clear conversation** button to reset state

## Setup

1. **Clone or prepare workspace**
   ```bash
   cd "e:/Anand/college/sem 4/DBMS/project st"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your OpenAI API key**
   ```bash
   export OPENAI_API_KEY="your_key_here"
   # or on Windows PowerShell
   setx OPENAI_API_KEY "your_key_here"
   ```
   You can also create a `.env` file with `OPENAI_API_KEY=...`.

4. **Add source documents**
   Place one or more `.txt` files under a `docs/` directory. These will be indexed for retrieval.

5. **Run the Streamlit app**
   ```bash
   streamlit run streamlit_app.py
   ```

## How it works

1. When the app first loads, it initializes a FAISS vector store from any text files it finds.
2. User queries are sent to a LangChain `RetrievalQA` chain that:
   - retrieves the top-3 documents relevant to the query
   - passes them to an OpenAI LLM for an answer
3. Conversation history is kept in `st.session_state.history` and rendered on each rerun.
4. The **Clear conversation** button resets the history.

## Extending

- Replace `OpenAI` with any other LLM supported by LangChain
- Use other vector stores (e.g. Chroma, Pinecone) by swapping out `FAISS` with the appropriate class
- Add a file upload widget if you want users to supply documents at runtime

---

Happy building! 🚀