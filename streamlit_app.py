import streamlit as st
#configs
st.set_page_config(page_title="College RAG Project", layout="wide")

if 'user' not in st.session_state:
    st.session_state['user'] = None


#Pages
login_page = st.Page("pages/auth.py", title="Log In", icon=":material/login:")
dashboard_page = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:")
chat_page = st.Page("pages/chat.py", title="Chat", icon=":material/smart_toy:")
analytic_page = st.Page("pages/analytics.py", title="Analytics", icon=":material/thumb_up:")


if st.session_state['user'] is None:
    pg = st.navigation([login_page])
elif st.session_state['user']['user_id'] in [1,3]:
    pg = st.navigation([chat_page, dashboard_page, analytic_page])
else:
    pg = st.navigation([chat_page, dashboard_page])

pg.run()