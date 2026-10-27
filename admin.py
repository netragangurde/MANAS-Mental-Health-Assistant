import streamlit as st
from streamlit import session_state
import json
import os
import numpy as np
from dotenv import load_dotenv
from PIL import Image
from openai import OpenAI

load_dotenv()

session_state = st.session_state
if "user_index" not in st.session_state:
    st.session_state["user_index"] = 0
    
def check_login(username, password, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
        for admin in data["admins"]:
            if admin["email"] == username and admin["password"] == password:
                session_state["logged_in"] = True
                session_state["user_info"] = admin
                st.success("Login successful!")
                return admin
        return None
    except Exception as e:
        st.error(f"Error checking login: {e}")
        return None


def signup(json_file_path="data.json"):
    st.title("Admin Signup Page")
    with st.form("signup_form"):
        st.write("Fill in the details below to create an admin account:")
        name = st.text_input("Name:")
        email = st.text_input("Email:")
        age = st.number_input("Age:", min_value=0, max_value=120)
        sex = st.radio("Sex:", ("Male", "Female", "Other"))
        password = st.text_input("Password:", type="password")
        confirm_password = st.text_input("Confirm Password:", type="password")
        
        if st.form_submit_button("Signup"):
            if password == confirm_password:
                admin = create_admin_account(name, email, age, sex, password, json_file_path)
                session_state["logged_in"] = True
                session_state["admin_info"] = admin
            else:
                st.error("Passwords do not match. Please try again.")


def login(json_file_path="data.json"):
    st.title("Admin Login Page")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    login_button = st.button("Login")

    if login_button:
        admin = check_login(username, password, json_file_path)
        if admin is not None:
            session_state["logged_in"] = True
            session_state["admin_info"] = admin
        else:
            st.error("Invalid credentials. Please try again.")


def create_admin_account(
    name,
    email,
    age,
    sex,
    password,
    json_file_path="data.json",
):
    try:
        # Check if the JSON file exists or is empty
        if not os.path.exists(json_file_path) or os.stat(json_file_path).st_size == 0:
            # Initialize data structure with empty lists for users and admins
            data = {"users": [], "admins": []}
        else:
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)
            
            # Check if "admins" key is missing, add it if necessary
            if "admins" not in data:
                data["admins"] = []

        admin_info = {
            "name": name,
            "email": email,
            "age": age,
            "sex": sex,
            "password": password,
        }
        data["admins"].append(admin_info)

        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        st.success("Admin account created successfully! You can now login.")
        return admin_info
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        st.error(f"Error creating admin account: {e}")
        return None

    
def render_admin_dashboard(admin_info):
    try:
        st.title(f"Welcome to the Admin Dashboard, {admin_info['name']}!")
        st.subheader("Admin Information:")
        st.write(f"Name: {admin_info['name']}")
        st.write(f"Sex: {admin_info['sex']}")
        st.write(f"Age: {admin_info['age']}")
        # Add other admin-specific information as needed
    except Exception as e:
        st.error(f"Error rendering admin dashboard: {e}")


def initialize_database(json_file_path="data.json"):
    try:
        # Check if JSON file exists
        if not os.path.exists(json_file_path):
            # Create an empty JSON structure with "users" and "admins" keys
            data = {"users": [], "admins": []}
            with open(json_file_path, "w") as json_file:
                json.dump(data, json_file)
        else:
            # Load existing data and check if "admins" key is missing
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)
                if "admins" not in data:
                    data["admins"] = []
                    with open(json_file_path, "w") as json_file:
                        json.dump(data, json_file, indent=4)

    except Exception as e:
        print(f"Error initializing database: {e}")


def main(json_file_path="data.json", therapists="therapists.json"):
    st.sidebar.title("MANAS - Mental Health Assistant")
    page = st.sidebar.radio(
        "Go to",
        (
            "Signup/Login",
            "Dashboard",
            "View patient details",  ## list
            "View groups",  ## details of other people with same therapist
        ),
        key="MANAS - Mental Health Assistant",
    )

    if page == "Signup/Login":
        st.title("Signup/Login Page")
        login_or_signup = st.radio(
            "Select an option", ("Login", "Signup"), key="login_signup"
        )
        if login_or_signup == "Login":
            login(json_file_path)
        else:
            signup(json_file_path)

    elif page == "Dashboard":
        admin_info = session_state.get("admin_info")

        if session_state.get("logged_in") and admin_info:
            render_admin_dashboard(admin_info)
        else:
            st.warning("Please login/signup to view the dashboard.")        
            
    elif page == "View patient details":
        groups = ["Group 1", "Group 2", "Group 3", "Group 4", "Group 5"]
        if session_state.get("logged_in"):
            st.title("View patient details")
            st.write("View details of all patients and add them to groups")

            # Add radio buttons for viewing options
            view_option = st.radio("View patients:", ("All patients", "Patients not assigned to any group"))

            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)
                for user in data["users"]:
                    # Check if the user is not assigned to any group
                    if view_option == "Patients not assigned to any group" and user["group"] is None:
                        st.subheader(f"Name: {user['name']}")
                        st.markdown("**Email:** " + user["email"])
                        st.markdown("**Age:** " + str(user["age"]))
                        if user["mental_health_traits"] is not None:
                            traits = sorted(
                                user["mental_health_traits"].items(), key=lambda x: x[1], reverse=True
                            )
                            top_traits = [trait for trait in traits if trait is not None and trait[1] > 0]
                            st.markdown("**Top traits:** " + ", ".join([trait[0] for trait in top_traits]))
                        st.markdown("**Personality type:** " + user["personality_type"])
                        if user["therapist"] is not None:
                            st.markdown("**Therapist:** " + user["therapist"]["name"])
                        else:
                            st.markdown("**Therapist:** Not assigned")
                        st.markdown("**Is interested in joining a group:** " + user["interested_in_groups"])
                        
                        # Add checkboxes to add users to groups and remove them from the list
                        try:
                            selected_group = st.selectbox(f"Select group for {user['name']}", groups)
                        except Exception as e:
                            selected_group = st.selectbox(f"Select group for {user['name']} with email {user['email']}", groups)
                        try:
                            if st.button(f"Add {user['name']} to {selected_group} group"):
                                # Update user's group in the data
                                user["group"] = selected_group
                                # Write updated data back to JSON file
                                with open(json_file_path, "w") as json_file:
                                    json.dump(data, json_file, indent=4)
                                    st.success("User added to group successfully.")
                                    st.rerun()
                        except Exception as e:
                            if st.button(f"Add {user['name']} with email {user['email']} to {selected_group} group"):
                                # Update user's group in the data
                                user["group"] = selected_group
                                # Write updated data back to JSON file
                                with open(json_file_path, "w") as json_file:
                                    json.dump(data, json_file, indent=4)
                                    st.success("User added to group successfully.")
                                    st.rerun()
                    elif view_option == "All patients":
                        # Display details of all patients
                        st.subheader(f"Name: {user['name']}")
                        st.markdown("**Email:** " + user["email"])
                        st.markdown("**Age:** " + str(user["age"]))
                        if user["mental_health_traits"] is not None:
                            traits = sorted(
                                user["mental_health_traits"].items(), key=lambda x: x[1], reverse=True
                            )
                            top_traits = [trait for trait in traits if trait is not None and trait[1] > 0]
                            st.markdown("**Top traits:** " + ", ".join([trait[0] for trait in top_traits]))
                        st.markdown("**Personality type:** " + user["personality_type"])
                        if user["therapist"] is not None:
                            st.markdown("**Therapist:** " + user["therapist"]["name"])
                        else:
                            st.markdown("**Therapist:** Not assigned")
                        st.markdown("**Is interested in joining a group:** " + str(user.get("interested_in_group", False)))
                        if "group" not in user:
                            user["group"] = None
                        group = "Not assigned" if  user["group"] is None else user["group"]
                        st.write("\n")
            if st.button("Reset groups"):
                for user in data["users"]:
                    # if user["group"] key does not exist, set it to None
                    if "group" not in user or user["group"] is not None:
                        user["group"] = None
                with open(json_file_path, "w") as json_file:
                    json.dump(data, json_file, indent=4)
                st.success("Groups reset successfully.")
                st.rerun()
                    
        else:
            st.warning("Please login/signup to find a therapist.")


    elif page == "View groups":
        if session_state.get("logged_in"):
            st.title("View groups")
            st.write("View details of all groups and the patients in each group")
            groups = ["Group 1", "Group 2", "Group 3", "Group 4", "Group 5"]

            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)
                if os.stat(json_file_path).st_size == 0 or not os.path.exists(json_file_path) or not json_file_path or "users" not in data or not data["users"]:
                    st.warning("No users found.")
                    return
                for group in groups:
                    st.subheader(f"Group: {group}")
                    group_empty = True  # Flag to track if the group is empty
                    for user in data["users"]:
                        if user.get("group") == group:
                            group_empty = False  # Group is not empty
                            st.markdown(f"**Name:** {user['name']}")
                            st.markdown(f"**Email:** {user['email']}")
                            st.markdown(f"**Age:** {user['age']}")
                            if user["mental_health_traits"] is not None:
                                traits = sorted(
                                    user["mental_health_traits"].items(), key=lambda x: x[1], reverse=True
                                )
                                top_traits = [trait for trait in traits if trait is not None and trait[1] > 0]
                                st.markdown("**Top traits:** " + ", ".join([trait[0] for trait in top_traits]))
                            st.markdown(f"**Top traits:** {', '.join([trait[0] for trait in top_traits])}")
                            st.markdown(f"**Personality type:** {user['personality_type']}")
                            if user["therapist"] is not None:
                                st.markdown("**Therapist:** " + user["therapist"]["name"])
                            else:
                                st.markdown("**Therapist:** Not assigned")

                            try:
                                if st.button(f"Delete {user['name']} from {group} group"):
                                    user["group"] = None
                                    st.success(f"{user['name']} deleted from group.")
                                    # Write updated data back to JSON file
                                    with open(json_file_path, "w") as json_file:
                                        json.dump(data, json_file, indent=4)
                                    break  # Stop iterating over users
                            except Exception as e:
                                if st.button(f"Delete {user['name']} with email {user['email']} from {group} group"):
                                    user["group"] = None
                                    st.success(f"{user['name']} deleted from group.")
                                    # Write updated data back to JSON file
                                    with open(json_file_path, "w") as json_file:
                                        json.dump(data, json_file, indent=4)
                                    break

                            st.write("\n")
                    if group_empty:
                        st.warning(f"No users assigned to {group} group.")
                    st.markdown("---")
        else:
            st.warning("Please login/signup to view your therapists.")


if __name__ == "__main__":
    initialize_database()
    main()
