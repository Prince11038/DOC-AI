import streamlit as st
import pandas as pd
import os

# File to store user data
user_data_file = 'user_data.csv'

# Check if file exists, if not create it with the appropriate columns
if not os.path.exists(user_data_file):
    df = pd.DataFrame(columns=['Name', 'Age', 'Mobile', 'Email'])
    df.to_csv(user_data_file, index=False)

# Function to load user data
def load_user_data():
    return pd.read_csv(user_data_file)

# Function to save user data
def save_user_data(name, age, mobile, email):
    df = load_user_data()
    new_entry = {'Name': name, 'Age': age, 'Mobile': mobile, 'Email': email}
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(user_data_file, index=False)

# Function to check if the user already exists
def user_exists(email):
    df = load_user_data()
    return any(df['Email'] == email)

# Main Application
def main():
    st.title("Login and Signup Page")

    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Signup":
        st.subheader("Create New Account")

        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        mobile = st.text_input("Mobile")
        email = st.text_input("Email")
        if st.button("Signup"):
            if user_exists(email):
                st.warning("User already exists! Please login.")
            else:
                save_user_data(name, age, mobile, email)
                st.success("You have successfully signed up!")
                st.info("Go to the login menu to login.")

    elif choice == "Login":
        st.subheader("Login to your Account")
        email = st.text_input("Email")
        if st.button("Login"):
            if user_exists(email):
                st.success("Welcome back!")
            else:
                st.warning("User not found! Please signup.")

if __name__ == '__main__':
    main()
