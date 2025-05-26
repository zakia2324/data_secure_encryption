import streamlit as st
from cryptography.fernet import Fernet
import time

# Global in-memory storage (dictionary)
user_data = {}
failed_attempts = {}

# Generate a key (should be stored securely in a real application)
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

def encrypt_data(passkey, data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(passkey, encrypted_data):
    return cipher.decrypt(encrypted_data.encode()).decode()

# Streamlit UI
st.title("Secure Data Storage & Retrieval")

# Select operation
choice = st.selectbox("Choose an operation:", ["Store Data", "Retrieve Data"])

# Store Data
if choice == "Store Data":
    username = st.text_input("Enter Username:")
    passkey = st.text_input("Enter Unique Passkey:", type="password")
    data = st.text_area("Enter Data to Store:")

    if st.button("Store"):
        if username and passkey and data:
            encrypted_data = encrypt_data(passkey, data)
            user_data[username] = encrypted_data
            failed_attempts[username] = 0  # Reset failed attempts
            st.success("Data stored securely!")
        else:
            st.error("All fields are required.")

# Retrieve Data
if choice == "Retrieve Data":
    username = st.text_input("Enter Username:")
    passkey = st.text_input("Enter Unique Passkey:", type="password")

    if st.button("Retrieve"):
        if username in user_data:
            if failed_attempts.get(username, 0) >= 3:
                st.error("Too many failed attempts! Please reauthorize.")
                time.sleep(2)
                st.rerun()
            try:
                decrypted_data = decrypt_data(passkey, user_data[username])
                st.success("Decrypted Data:")
                st.text_area("Your Data:", decrypted_data, disabled=True)
                failed_attempts[username] = 0  # Reset failed attempts
            except:
                failed_attempts[username] = failed_attempts.get(username, 0) + 1
                st.error(f"Incorrect passkey! Attempts remaining: {3 - failed_attempts[username]}")
        else:
            st.error("User not found.")
            