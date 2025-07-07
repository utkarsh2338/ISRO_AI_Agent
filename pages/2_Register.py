import streamlit as st
import pandas as pd
import os
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



st.title("📝 Register")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    user_path = "users/users.csv"
    if os.path.exists(user_path):
        return pd.read_csv(user_path)
    return pd.DataFrame(columns=["email", "password"])

def save_user(email, password):
    os.makedirs("users", exist_ok=True)
    users = load_users()
    new_user = pd.DataFrame([{"email": email, "password": hash_password(password)}])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv("users/users.csv", index=False)

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):
    users = load_users()
    if email in users["email"].values:
        st.warning("User already exists")
    else:
        save_user(email, password)
        st.success("Registration successful!")