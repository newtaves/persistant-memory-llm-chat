import streamlit as st

#configs
st.set_page_config(page_title="College RAG Project", layout="wide")

if 'user' not in st.session_state:
    st.session_state['user'] = None


#Pages
login_page = st.Page("pages/auth.py", title="Log In", icon=":material/login:")
dashboard_page = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:")


if st.session_state['user'] is None:
    pg = st.navigation([login_page])
else:
    pg = st.navigation([dashboard_page])

pg.run()