import streamlit as st

# Initialize session variable
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Page config
st.set_page_config(page_title="ISRO AI Agent", page_icon="🚀", layout="centered", initial_sidebar_state="collapsed")

# Background styling
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.ytimg.com/vi/Dcemvtppdfg/maxresdefault.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """, unsafe_allow_html=True)

# UI
st.title("🚀 ISRO AI Agent Navigation")
st.page_link("pages/1_Login.py", label="🔐 Login")
st.page_link("pages/2_Register.py", label="📝 Register")
st.page_link("pages/3_Agent.py", label="🤖 ISRO Agent", disabled=not st.session_state["authenticated"])
