import streamlit as st
import os


def main():
    st.title("Welcome to the Mental Health Portal")
    st.write("Login as a patient or an admin")
    user = st.radio("User", ("Patient", "Admin"))
    if st.button("Login"):
        if user == "Patient":
            os.system("streamlit run patient.py")
        else:
            os.system("streamlit run admin.py")

if __name__ == "__main__":
    main()