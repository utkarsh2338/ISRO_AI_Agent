import streamlit.components.v1 as components
import os
import streamlit as st
import pandas as pd
import hashlib


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


st.title("🔐 Login")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    user_path = "users/users.csv"
    if os.path.exists(user_path):
        return pd.read_csv(user_path)
    return pd.DataFrame(columns=["email", "password"])

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    users = load_users()
    if email in users["email"].values and hash_password(password) in users[users["email"] == email]["password"].values:
        st.session_state["authenticated"] = True
        st.session_state["user_email"] = email
        st.success("Login successful!")
        
    else:
        st.error("Invalid credentials")