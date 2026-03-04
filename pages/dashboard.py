import streamlit as st
from helper import save_global_persona 

user = st.session_state['user']


st.sidebar.markdown("Dashboard")

st.title("Dashboard")
st.write(f"Logged in as: **{user['email']}**")
st.divider()

new_persona = st.text_area(
        "Edit Global Persona:", 
        value=user['global_persona'],
        help="This is the system message sent to the LLM."
)
    
if st.button("Save Persona"):
    save_global_persona(user['user_id'], new_persona)        
    st.session_state['user']['global_persona'] = new_persona
    st.success("Persona updated!")
    st.rerun()

if st.button("Logout"):
    st.session_state['user'] = None
    st.rerun()
