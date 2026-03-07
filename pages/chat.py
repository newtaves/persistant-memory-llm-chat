import streamlit as st
from dotenv import load_dotenv

from helper import (
    create_conversation,
    list_conversations,
    load_session,
    save_message_n_message_embeddings,
    retrieve_context
)

from helper import get_gemini_response, create_session_name

load_dotenv()


# ---------------- SESSION STATE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "first_response" not in st.session_state:
    st.session_state.first_response = True


# ---------------- SIDEBAR ---------------- #

st.sidebar.title("Conversations")


# New chat button
if st.sidebar.button("➕ New Chat"):

    st.session_state.messages = []
    st.session_state.conversation_id = None
    st.session_state.first_response = True

    st.rerun()


# Load user conversations
conversations = list_conversations(st.session_state.user["user_id"])


for conv in conversations:

    title = conv["title"] or "Untitled"

    if st.sidebar.button(title, key=conv["conversation_id"]):

        st.session_state.conversation_id = conv["conversation_id"]

        rows = load_session(conv["conversation_id"])

        st.session_state.messages = [
            {"role": r["role"], "content": r["content"]} for r in rows
        ]

        st.session_state.first_response = False

        st.rerun()


# ---------------- DISPLAY CHAT ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- USER INPUT ---------------- #

if prompt := st.chat_input("Ask something..."):

    # show user message
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })


    # ---------- RAG CONTEXT ---------- #

    context_list = retrieve_context(prompt, top_k=5)

    context_text = "\n".join(context_list)

    history = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in st.session_state.messages[-6:]
    )

    system_instructions = f""" 
        You are a helpful assitant. Answer the questions of the user.
        While answering use your long term memory when needed.
        Here is your long term memory:
        {context_text}
    """

    prompt = f"""conversation History:
        {history}

        User Question:
        {prompt}
    """
    # ---------- LLM RESPONSE ---------- #

    response = get_gemini_response(prompt, system_instructions)["response"]


    # ---------- FIRST MESSAGE LOGIC ---------- #

    if st.session_state.first_response:

        title_prompt = f"""
        role:user
        content:{prompt}

        role:assistant
        content:{response}
        """

        title = create_session_name(title_prompt).get("response", "Untitled")

        conversation_id = create_conversation(
            st.session_state.user["user_id"],
            title[:40]
        )

        st.session_state.conversation_id = conversation_id

        save_message_n_message_embeddings(
            conversation_id,
            "user",
            prompt
        )

        save_message_n_message_embeddings(
            conversation_id,
            "assistant",
            response
        )

        st.session_state.first_response = False

    else:

        save_message_n_message_embeddings(
            st.session_state.conversation_id,
            "user",
            prompt
        )

        save_message_n_message_embeddings(
            st.session_state.conversation_id,
            "assistant",
            response
        )


    # ---------- DISPLAY RESPONSE ---------- #

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })