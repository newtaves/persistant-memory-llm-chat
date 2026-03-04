import streamlit as st

user = st.session_state['user']

# Sidebar for logout and info
with st.sidebar:
    st.write(f"Logged in as: **{user['email']}**")
    if st.button("Logout"):
        st.session_state['user'] = None
        st.rerun()

st.title("Dashboard")
st.info(f"Active Persona: {user['global_persona']}")

# Your RAG Logic goes here
st.write("---")
st.subheader("Chat Interface")
# st.chat_input("Ask something...")