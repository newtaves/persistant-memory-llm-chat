import streamlit as st
from helper import register_user, authenticate_user

st.title("College Project Access")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            result = authenticate_user(email, password)

            if isinstance(result, str):
                st.error(result)
            else:
                st.session_state['user'] = result
                st.rerun()

with tab2:
    with st.form("register_form"):
        reg_email = st.text_input("New Email")
        reg_password = st.text_input("New Password", type="password")
        if st.form_submit_button("Create Account"):
            register_user(reg_email, reg_password)
            st.success("Registration successful! Switch to Login tab.")