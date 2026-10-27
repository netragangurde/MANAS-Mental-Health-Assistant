import streamlit as st
from streamlit import session_state
import json
import os
import numpy as np
from dotenv import load_dotenv
from PIL import Image
from openai import OpenAI
import smtplib, ssl
import smtplib

load_dotenv()


def get_text_client_and_model():
    """Return an OpenAI-compatible client and model for the selected cloud provider.

    Set LLM_PROVIDER=gemini to use Gemini, or LLM_PROVIDER=openai to use OpenAI.
    This helper is for the legacy assessment prompts; chat UI has its own Ollama path.
    """
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key or api_key == "paste_your_new_gemini_key_here":
            raise RuntimeError("GEMINI_API_KEY is missing from .env.")
        model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()
        client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            timeout=45.0,
            max_retries=0,
        )
        return client, model

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing from .env.")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
        client = OpenAI(api_key=api_key, timeout=45.0, max_retries=0)
        return client, model

    raise RuntimeError(
        f"Provider '{provider}' is not supported by these assessment functions. "
        "Use LLM_PROVIDER=gemini or LLM_PROVIDER=openai."
    )


def ai_therapist(name, personality_type, previous_question=None, previous_answer=None):
    try:
        client, model = get_text_client_and_model()

        personality_messages = {
            "INTJ - Architect": "I'm here to provide you with logical and strategic guidance.",
            "INTP - Logician": "I'm here to help you analyze and understand complex ideas.",
            "ENTJ - Commander": "I'm here to help you take charge and achieve your goals.",
            "ENTP - Debater": "I'm here to engage in stimulating discussions and explore possibilities with you.",
            "INFJ - Advocate": "I'm here to support your values and help you make a positive impact.",
            "INFP - Mediator": "I'm here to understand your unique perspective and help you find harmony.",
            "ENFJ - Protagonist": "I'm here to inspire and empower you to reach your full potential.",
            "ENFP - Campaigner": "I'm here to ignite your imagination and help you pursue your dreams.",
            "ISTJ - Logistician": "I'm here to provide you with practical solutions and reliable support.",
            "ISFJ - Defender": "I'm here to protect and care for you, ensuring your well-being.",
            "ESTJ - Executive": "I'm here to organize and optimize your life for success.",
            "ESFJ - Consul": "I'm here to create a warm and supportive environment for you.",
            "ISTP - Virtuoso": "I'm here to help you navigate the world with practical skill and expertise.",
            "ISFP - Adventurer": "I'm here to explore the beauty and creativity of life with you.",
            "ESTP - Entrepreneur": "I'm here to take risks and seize opportunities with you.",
            "ESFP - Entertainer": "I'm here to bring joy and excitement into your life.",
        }

        personality_message = personality_messages.get(personality_type, "")
        if previous_question is None or previous_answer is None:
            prompt = f"""
            As an AI mental health therapist, I aim to provide you with a safe space to express yourself and explore your thoughts and feelings. I understand that seeking help can be challenging, but please know that {personality_message}

            Let's start by taking a deep breath together. Inhale slowly... and exhale gently. Remember, it's okay to feel whatever you're feeling right now. Your emotions are valid, and you deserve compassion and understanding.

            As we embark on this journey together, I want you to know that I'm not here to judge you. 

            So, tell me, what's on your mind today? Is there anything specific that's been weighing on you lately? Feel free to share as much or as little as you're comfortable with. I'm here to support you, no matter what.

            And remember, you're not alone in this. We're in this together, and together, we can navigate through whatever challenges you may be facing. Take your time, and whenever you're ready, I'm here to listen.
            """
        else:
            prompt = f"""
            {previous_question}
            Patient: {previous_answer}
            """

        messages = [{"role": "system", "content": prompt}]
        response = client.chat.completions.create(
            messages=messages,
            model=model,
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def identify_traits(
    name, personality_type, previous_question=None, previous_answer=None
):
    try:
        client, model = get_text_client_and_model()

        # List of mental health traits to identify
        mental_health_traits = [
            "Anxiety",
            "Depression",
            "Suicidal ideation",
            "Insomnia",
            "PTSD",
            "OCD",
            "Bipolar disorder",
            "Eating disorders",
            "ADHD",
            "Substance abuse/addiction",
        ]

        # Construct the prompt
        prompt = f"As a mental health AI, I aim to identify any mental health traits you might be experiencing. Based on your response, I'll try to detect traits like {', '.join(mental_health_traits)}. Please share your thoughts or feelings, and I'll analyze them to identify any relevant traits.\nPatient: {previous_answer}"

        messages = [{"role": "system", "content": prompt}]

        # Request completion from OpenAI
        response = client.chat.completions.create(
            messages=messages,
            model=model,
        )

        # Extract detected traits from the response
        detected_traits = []
        for trait in mental_health_traits:
            if trait.lower() in response.choices[0].message.content.lower():
                detected_traits.append(trait)

        return detected_traits

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def ai_therapist_with_traits(name, personality_type, previous_question=None, previous_answer=None):
    try:
        client, model = get_text_client_and_model()
        mental_health_traits = [
            "Anxiety",
            "Depression",
            "Suicidal ideation",
            "Insomnia",
            "PTSD",
            "OCD",
            "Bipolar disorder",
            "Eating disorders",
            "ADHD",
            "Substance abuse/addiction",
        ]
        personality_messages = {
            "INTJ - Architect": "I'm here to provide you with logical and strategic guidance.",
            "INTP - Logician": "I'm here to help you analyze and understand complex ideas.",
            "ENTJ - Commander": "I'm here to help you take charge and achieve your goals.",
            "ENTP - Debater": "I'm here to engage in stimulating discussions and explore possibilities with you.",
            "INFJ - Advocate": "I'm here to support your values and help you make a positive impact.",
            "INFP - Mediator": "I'm here to understand your unique perspective and help you find harmony.",
            "ENFJ - Protagonist": "I'm here to inspire and empower you to reach your full potential.",
            "ENFP - Campaigner": "I'm here to ignite your imagination and help you pursue your dreams.",
            "ISTJ - Logistician": "I'm here to provide you with practical solutions and reliable support.",
            "ISFJ - Defender": "I'm here to protect and care for you, ensuring your well-being.",
            "ESTJ - Executive": "I'm here to organize and optimize your life for success.",
            "ESFJ - Consul": "I'm here to create a warm and supportive environment for you.",
            "ISTP - Virtuoso": "I'm here to help you navigate the world with practical skill and expertise.",
            "ISFP - Adventurer": "I'm here to explore the beauty and creativity of life with you.",
            "ESTP - Entrepreneur": "I'm here to take risks and seize opportunities with you.",
            "ESFP - Entertainer": "I'm here to bring joy and excitement into your life.",
        }

        personality_message = personality_messages.get(personality_type, "")
        
        # Instructions for detecting mental health traits
        trait_detection_prompt = """
        Additionally, while we converse, I will also be analyzing our discussion to identify any mental health traits you might be experiencing. 
        This includes traits such as Anxiety, Depression, Suicidal ideation, Insomnia, PTSD, OCD, Bipolar disorder, Eating disorders, ADHD, and Substance abuse/addiction.
        """

        prompt = f"""
        As an AI mental health therapist, I aim to provide you with a safe space to express yourself and explore your thoughts and feelings. I understand that seeking help can be challenging, but please know that {personality_message}

        Let's start by taking a deep breath together. Inhale slowly... and exhale gently. Remember, it's okay to feel whatever you're feeling right now. Your emotions are valid, and you deserve compassion and understanding.

        As we embark on this journey together, I want you to know that I'm not here to judge you. 

        {previous_question}
        Patient: {previous_answer}

        So, tell me, what's on your mind today? Is there anything specific that's been weighing on you lately? Feel free to share as much or as little as you're comfortable with. I'm here to support you, no matter what.

        And remember, you're not alone in this. We're in this together, and together, we can navigate through whatever challenges you may be facing. Take your time, and whenever you're ready, I'm here to listen.
        {trait_detection_prompt}
        """

        messages = [{"role": "system", "content": prompt}]

        response = client.chat.completions.create(
            messages=messages,
            model=model,
        )

        # Extract detected traits from the response
        detected_traits = []
        for trait in mental_health_traits:
            if trait.lower() in response.choices[0].message.content.lower():
                detected_traits.append(trait)

        return detected_traits, response.choices[0].message.content

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
    
def get_serious_mental_disorders(previous_responses):
    try:
        client, model = get_text_client_and_model()
        responses = ""
        for response in previous_responses:
            responses += f"{response}\n"
        prompt = f"""
        You're a mental health professional, and you're having previous responses of the patients of their discussions with the mental health expert. Please identify any serious mental disorders present in the patient's responses. Serious mental disorders include anything that requires immediate attention or intervention, such as Schizophrenia, Dissociative disorders, Personality disorders, Suicidal ideation, etc.
        If you detect any serious mental disorders, please list them below in a comma-separated format.
        If you don't detect any serious mental disorders, can respond with 'None'. 
        
        \nPatient: {responses}
        """

        messages = [{"role": "system", "content": prompt}]

        response = client.chat.completions.create(
            messages=messages,
            model=model,
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def send_mail(disorders):
    server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
    SENDER_MAIL_ID = os.getenv("SENDER_MAIL_ID")
    APP_PASSWORD = os.getenv("APP_PASSWORD")
    RECEIVER_1 = os.getenv("RECEIVER_EMAIL_1")
    RECEIVER_2 = os.getenv("RECEIVER_EMAIL_2")
    RECEIVER_3 = os.getenv("RECEIVER_EMAIL_3")
    server.login(SENDER_MAIL_ID, APP_PASSWORD)
    disorders = disorders.split(",")
    # create a sentense with the disorders, if there are more than 1, add 'and' before the last one
    if len(disorders) > 1:
        disorders[-1] = "and " + disorders[-1]
        
    disorders = ", ".join(disorders)
    message = f"""
    Subject: Urgent Alert: Patient Mental Health Concerns

    Dear [Recipient's Name],

    I am writing to urgently bring to your attention concerning observations regarding a patient's mental health condition. During our recent interaction, the patient exhibited symptoms indicative of the following serious mental disorders: {disorders}.

    It is crucial that appropriate interventions and support are provided to ensure the patient's safety and well-being. I highly recommend immediate action and coordination with relevant healthcare professionals to address these concerns effectively.

    Please let me know if you require any further information or assistance regarding this matter. Your prompt attention to this issue is greatly appreciated.
    
    """
    server.sendmail(SENDER_MAIL_ID, RECEIVER_1, message)
    server.sendmail(SENDER_MAIL_ID, RECEIVER_2, message)
    server.sendmail(SENDER_MAIL_ID, RECEIVER_3, message)
    server.quit()
    st.success("Email sent successfully!")
    return True

    
session_state = st.session_state
if "user_index" not in st.session_state:
    st.session_state["user_index"] = 0


def signup(json_file_path="data.json"):
    st.title("Signup Page")
    with st.form("signup_form"):
        st.write("Fill in the details below to create an account:")
        name = st.text_input("Name:")
        email = st.text_input("Email:")
        age = st.number_input("Age:", min_value=0, max_value=120)
        sex = st.radio("Sex:", ("Male", "Female", "Other"))
        password = st.text_input("Password:", type="password")
        confirm_password = st.text_input("Confirm Password:", type="password")

        st.info("Take the personality test [here](https://www.16personalities.com/free-personality-test) and enter your personality type below." )
        st.info("The test should not be older than 3 months.")
        personality_type = st.selectbox(
            "Select Personality Type",
            [
                "INTJ - The Architect",
                "INTP - The Logician",
                "ENTJ - The Commander",
                "ENTP - The Debater",
                "INFJ - The Advocate",
                "INFP - The Mediator",
                "ENFJ - The Protagonist",
                "ENFP - The Campaigner",
                "ISTJ - The Logistician",
                "ISFJ - The Defender",
                "ESTJ - The Executive",
                "ESFJ - The Consul",
                "ISTP - The Virtuoso",
                "ISFP - The Adventurer",
                "ESTP - The Entrepreneur",
                "ESFP - The Entertainer",
            ],
        )

        interested_in_groups = st.radio(
            "Are you interested in joining groups?", ("Yes", "No")
        )

        if st.form_submit_button("Signup"):
            if password == confirm_password:
                user = create_account(
                    name,
                    email,
                    age,
                    sex,
                    password,
                    personality_type,
                    interested_in_groups,
                    json_file_path,
                )
                session_state["logged_in"] = True
                session_state["user_info"] = user
            else:
                st.error("Passwords do not match. Please try again.")


def check_login(username, password, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        for user in data["users"]:
            if user["email"] == username and user["password"] == password:
                session_state["logged_in"] = True
                session_state["user_info"] = user
                st.success("Login successful!")
                # render_dashboard(user)
                return user
        return None
    except Exception as e:
        st.error(f"Error checking login: {e}")
        return None


def initialize_database(json_file_path="data.json"):
    try:
        # Check if JSON file exists
        if not os.path.exists(json_file_path):
            # Create an empty JSON structure
            data = {"users": []}
            with open(json_file_path, "w") as json_file:
                json.dump(data, json_file)
    except Exception as e:
        print(f"Error initializing database: {e}")


def create_account(
    name,
    email,
    age,
    sex,
    password,
    personality_type,
    interested_in_groups,
    json_file_path="data.json",
):
    try:
        # Check if the JSON file exists or is empty
        if not os.path.exists(json_file_path) or os.stat(json_file_path).st_size == 0:
            data = {"users": []}
        else:
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)

        # Append new user data to the JSON structure
        user_info = {
            "name": name,
            "email": email,
            "age": age,
            "sex": sex,
            "password": password,
            "personality_type": personality_type,
            "interested_in_groups": interested_in_groups,
            "therapist": None,
            "mental_health_traits": None,
            "questions": None,
            "group": None,
        }
        data["users"].append(user_info)

        # Save the updated data to JSON
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        st.success("Account created successfully! You can now login.")
        return user_info
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        st.error(f"Error creating account: {e}")
        return None


def login(json_file_path="data.json"):
    st.title("Login Page")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    login_button = st.button("Login")

    if login_button:
        user = check_login(username, password, json_file_path)
        if user is not None:
            session_state["logged_in"] = True
            session_state["user_info"] = user
        else:
            st.error("Invalid credentials. Please try again.")


def get_user_info(email, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            for user in data["users"]:
                if user["email"] == email:
                    return user
        return None
    except Exception as e:
        st.error(f"Error getting user information: {e}")
        return None


def render_dashboard(user_info, json_file_path="data.json"):
    try:
        st.title(f"Welcome to the Dashboard, {user_info['name']}!")
        st.subheader("User Information:")
        st.write(f"Name: {user_info['name']}")
        st.write(f"Sex: {user_info['sex']}")
        st.write(f"Age: {user_info['age']}")
        st.write(f"Your personality type: {user_info['personality_type']}")
        if user_info["therapist"] is not None:
            st.write(f"Your therapist: {user_info['therapist']['name']}")
    except Exception as e:
        st.error(f"Error rendering dashboard: {e}")


def generate_conversational_reply(chat_history, therapist_info):
    """Generate a supportive multi-turn reply using the configured LLM provider.

    Set LLM_PROVIDER=gemini (Gemini API), openai (OpenAI API), or ollama
    (local Ollama server) in .env. Gemini and OpenAI use the OpenAI Python
    client; Ollama uses its local HTTP chat endpoint.
    """
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen

    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    therapist_name = (therapist_info or {}).get("name", "MANAS")
    personality_type = (therapist_info or {}).get("mbti_type", "")

    system_prompt = f"""You are MANAS, an AI mental-wellness support assistant. You are not a human therapist or a licensed clinician.
The selected assistant profile is {therapist_name} ({personality_type}). Use a warm, respectful style, but do not claim to be a real person or licensed professional.
Respond naturally to the user's latest message and use earlier conversation messages for context. Usually reply in 2-5 sentences and ask at most one gentle follow-up question when helpful.
Do not diagnose a mental disorder, prescribe treatment, or present guesses as clinical facts. Do not claim the conversation is completely confidential.
If the user describes immediate danger, imminent self-harm, or intent to harm someone, prioritize immediate safety: encourage contacting local emergency services and a trusted person who can be physically present. Do not rely on this chatbot as the sole source of help.
Be empathetic, non-judgmental, and avoid repetitive generic introductions."""

    messages = [{"role": "system", "content": system_prompt}]
    last_signature = None
    for item in chat_history[-12:]:
        role = item.get("role")
        content = item.get("content")
        if role in ("user", "assistant") and isinstance(content, str) and content.strip():
            signature = (role, content.strip())
            # Ignore adjacent duplicate messages caused by resubmitting during a timeout.
            if signature == last_signature:
                continue
            messages.append({"role": role, "content": content.strip()})
            last_signature = signature

    if provider in ("gemini", "openai"):
        if provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY", "").strip()
            model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()
            base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
            if not api_key or api_key == "paste_your_new_gemini_key_here":
                raise RuntimeError(
                    "GEMINI_API_KEY is missing. Add your Gemini API key to .env, then restart Streamlit."
                )
            client = OpenAI(api_key=api_key, base_url=base_url, timeout=45.0, max_retries=0)
        else:
            api_key = os.getenv("OPENAI_API_KEY", "").strip()
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
            if not api_key:
                raise RuntimeError(
                    "OPENAI_API_KEY is missing. Add your OpenAI API key to .env, then restart Streamlit."
                )
            client = OpenAI(api_key=api_key, timeout=60.0, max_retries=1)

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=220,
            )
        except Exception as exc:
            # Preserve provider error details for the terminal without exposing keys.
            raise RuntimeError(f"{provider.capitalize()} request failed: {type(exc).__name__}: {exc}") from exc

        answer = response.choices[0].message.content if response.choices else None
        if not isinstance(answer, str) or not answer.strip():
            raise RuntimeError(f"{provider.capitalize()} returned an empty response. Check model access and retry.")
        return answer.strip()

    if provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.7},
        }
        request = Request(
            url=f"{base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=180) as response:
                result = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            raise RuntimeError(
                f"Ollama returned HTTP {exc.code}. Check that model '{model}' is installed. Details: {detail}"
            ) from exc
        except URLError as exc:
            raise RuntimeError(
                f"Could not connect to Ollama at {base_url}. Start Ollama and run 'ollama run {model}' first."
            ) from exc
        except TimeoutError as exc:
            raise RuntimeError(
                "The local model took too long to respond. Try again or use a smaller Ollama model."
            ) from exc

        answer = (result.get("message") or {}).get("content", "")
        if not isinstance(answer, str) or not answer.strip():
            raise RuntimeError("The local model returned an empty response.")
        return answer.strip()

    raise RuntimeError(
        f"Unknown LLM_PROVIDER '{provider}'. Set it to 'gemini', 'openai', or 'ollama' in .env."
    )

def save_chat_history(email, chat_history, json_file_path="data.json"):
    """Persist a patient's chat history in data.json without overwriting other fields."""
    try:
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        user_record = next(
            (user for user in data.get("users", []) if user.get("email") == email),
            None,
        )
        if user_record is None:
            return False

        user_record["chat_history"] = chat_history[-40:]
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        return True
    except Exception as exc:
        print(f"Could not save MANAS chat history: {type(exc).__name__}: {exc}")
        return False


def main(json_file_path="data.json", therapists="therapists.json"):
    st.sidebar.title("MANAS - Mental Health Assistant")
    page = st.sidebar.radio(
        "Go to",
        (
            "Signup/Login",
            "Dashboard",
            "Find therapist",  ## list
            "Your therapist",  ## details of other people with same therapist
            "ChatBot",  ## chat with therapist
            "Lifestyle Recommendations",  ## meditation
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
        if session_state.get("logged_in"):
            render_dashboard(session_state["user_info"])
        else:
            st.warning("Please login/signup to view the dashboard.")
            
            
    elif page == "Find therapist":
        if session_state.get("logged_in"):
            st.title("Find therapist")
            st.write("Find a therapist that suits your personality type")

            # Load therapist data from JSON file
            with open(therapists, "r") as json_file:
                data = json.load(json_file)

                # Filter therapists based on user's personality type
                therapist_options = [
                    f"{therapist['name']} - {therapist['clients_helped']}"
                    for therapist in data
                    if therapist["mbti_type"]
                    == session_state["user_info"]["personality_type"]
                ]

                # Display select box for therapists
                selected_therapist = st.selectbox(
                    "Select a therapist:", therapist_options
                )

                # If a therapist is selected
                if selected_therapist:
                    therapist_name, therapist_clients_helped = selected_therapist.split(
                        " - "
                    )
                    therapist_info = [
                        therapist
                        for therapist in data
                        if therapist["name"] == therapist_name
                        and therapist["clients_helped"] == therapist_clients_helped
                    ][0]

                    # Display information of selected therapist
                    st.subheader("Therapist Information:")

                    therapist_name = therapist_info['name']
                    experience = therapist_info['experience']
                    job_description = therapist_info['job_description']
                    clients_helped = therapist_info['clients_helped']

                    st.markdown(f"**Name:** {therapist_name}")
                    st.markdown(f"**Experience:** {experience}")
                    st.markdown(f"**Job Description:** {job_description}")
                    st.markdown(f"**Clients helped:** {clients_helped}")


                    # Button to select therapist
                    if st.button("Select this therapist"):
                        # Update user's therapist information
                        with open(json_file_path, "r+") as json_file:
                            data = json.load(json_file)
                            user_index = next(
                                (
                                    i
                                    for i, user in enumerate(data["users"])
                                    if user["email"]
                                    == session_state["user_info"]["email"]
                                ),
                                None,
                            )
                            if user_index is not None:
                                user_info = data["users"][user_index]
                                user_info["therapist"] = therapist_info
                                session_state["user_info"] = user_info
                                json_file.seek(0)
                                json.dump(data, json_file, indent=4)
                                json_file.truncate()
                                st.success("Therapist selected successfully!")
                            else:
                                st.error("User not found.")
        else:
            st.warning("Please login/signup to find a therapist.")


    elif page == "Your therapist":
        if session_state.get("logged_in"):
            # if therapist is not none, show the therapist details
            st.title("Your therapist")
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)
                if session_state["user_info"]["therapist"] is None:
                    st.warning("You do not have a therapist yet.")
                    return
                therapist_name = session_state["user_info"]["therapist"]["name"]
                therapist_mbti_type = session_state["user_info"]["therapist"][
                    "mbti_type"
                ]
                therapist_info = session_state["user_info"]["therapist"]
                st.subheader(f"Therapist: {therapist_name}")
                st.write(f"MBTI Type: {therapist_mbti_type}")
                st.write(f"Experience: {therapist_info['experience']}")
                st.write(f"Job Description: {therapist_info['job_description']}")
                st.write(f"Clients helped: {therapist_info['clients_helped']}")
                users_with_same_therapist = [
                    user
                    for user in data["users"]
                    if user["therapist"] and user["therapist"]["name"] == therapist_name
                    and user["therapist"]["mbti_type"] == therapist_mbti_type
                ]
                st.subheader("Users with the same therapist:")
                for user in users_with_same_therapist:
                    st.subheader(f"Name: {user['name']}")
                    st.write(f"Email: {user['email']}")
                    st.write(f"Age: {user['age']}")

        else:
            st.warning("Please login/signup to view your therapists.")
    elif page == "ChatBot":
        if not session_state.get("logged_in"):
            st.warning("Please login/signup to chat.")
        else:
            user_info = session_state.get("user_info", {})
            st.title("MANAS – AI Mental Wellness Assistant")
            st.caption(
                "Supportive AI conversation, not a medical diagnosis or a replacement for professional care."
            )

            therapist_info = user_info.get("therapist")
            if not therapist_info:
                st.warning("Please select a therapist profile from 'Find therapist' before starting a conversation.")
            else:
                st.subheader(f"Selected profile: {therapist_info.get('name', 'MANAS')}")
                st.caption(
                    f"Style profile: {therapist_info.get('mbti_type', 'General')} · "
                    f"Experience listed: {therapist_info.get('experience', 'Not specified')}"
                )

                email = user_info.get("email", "")
                history_key = f"manas_chat_history_{email}"

                if history_key not in session_state:
                    stored_history = user_info.get("chat_history")
                    if not isinstance(stored_history, list):
                        stored_history = []
                        # Preserve the old question/answer transcript where available.
                        old_questions = user_info.get("questions") or []
                        for item in old_questions:
                            if not isinstance(item, dict):
                                continue
                            old_question = item.get("question")
                            old_response = item.get("response")
                            if isinstance(old_question, str) and old_question.strip():
                                stored_history.append({"role": "assistant", "content": old_question})
                            if isinstance(old_response, str) and old_response.strip():
                                stored_history.append({"role": "user", "content": old_response})

                    if not stored_history:
                        stored_history = [{
                            "role": "assistant",
                            "content": (
                                f"Hi {user_info.get('name', 'there')}, I'm MANAS, your AI mental-wellness support assistant. "
                                "I'm here to listen. What's been on your mind lately?"
                            ),
                        }]
                    session_state[history_key] = stored_history[-40:]

                chat_history = session_state[history_key]
                for message in chat_history:
                    role = message.get("role")
                    content = message.get("content", "")
                    if role in ("user", "assistant") and content:
                        with st.chat_message(role):
                            st.markdown(content)

                prompt = st.chat_input("Share what's on your mind...")
                if prompt:
                    candidate_history = chat_history + [{"role": "user", "content": prompt.strip()}]
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    try:
                        with st.spinner("MANAS is preparing a response..."):
                            reply = generate_conversational_reply(candidate_history, therapist_info)
                    except Exception as exc:
                        # Keep the patient's message so it is not lost when Streamlit reruns.
                        session_state[history_key] = candidate_history[-40:]
                        saved = save_chat_history(email, session_state[history_key], json_file_path)
                        if not saved:
                            st.warning("Your message remains in this session but could not be saved to the local data file.")
                        st.error(
                            "MANAS could not generate a reply. Check the VS Code terminal for the technical error, "
                            "then verify your selected LLM provider, API key or local model, model name, and quota."
                        )
                        print(f"MANAS response error: {type(exc).__name__}: {exc}")
                    else:
                        candidate_history.append({"role": "assistant", "content": reply})
                        candidate_history = candidate_history[-40:]
                        session_state[history_key] = candidate_history
                        user_info["chat_history"] = candidate_history
                        session_state["user_info"] = user_info
                        if not save_chat_history(email, candidate_history, json_file_path):
                            st.warning("The reply worked, but the chat history could not be saved to data.json.")
                        with st.chat_message("assistant"):
                            st.markdown(reply)

    elif page == "Lifestyle Recommendations":

        if session_state.get("logged_in"):
            st.title("Lifestyle Recommendations")
            st.write("Here are some lifestyle recommendations to improve your mental health:")
            st.image("mental-health.jpg")
            st.markdown(f"# Dietary Recommendations")
            st.write(f"Taking care of your mental health involves more than just your emotions—it also involves what you eat. Here are some dietary recommendations that can help support your mental well-being:")
            st.markdown(f"#### 1. Balance Your Plate")
            st.write(f"Aim for a balanced diet that includes plenty of fruits, vegetables, whole grains, lean proteins (like chicken, fish, tofu), and healthy fats (such as avocados and nuts). This mix of nutrients helps keep both your body and mind in good shape.")
            st.markdown(f"#### 2. Discover Omega-3s")
            st.write(f"Consider adding foods rich in omega-3 fatty acids to your meals. These healthy fats, found in fish like salmon, trout, and sardines, as well as in nuts and seeds like flaxseeds and walnuts, can give your mood a little lift.")
            st.markdown(f"#### 3. Mind Your Sugar")
            st.write(f"Be mindful of your sugar intake. Too much sugar, especially from sweets and processed foods, can leave you feeling low and tired. Instead, opt for natural sources of sweetness like fruits.")
            st.markdown(f"#### 4. Easy on the Caffeine and Alcohol")
            st.write(f"While a cup of coffee or tea can give you a boost, too much caffeine can make you jittery and anxious. Similarly, while alcohol might seem relaxing at first, it can actually worsen your mood in the long run. Enjoy them in moderation.")
            st.markdown(f"#### 5. Stay Hydrated")
            st.write(f"Don't forget to drink enough water throughout the day. Dehydration can leave you feeling sluggish and irritable, so keep a water bottle handy and sip regularly.")
            st.markdown(f"#### 6. Choose Whole Foods")
            st.write(f"Focus on eating whole foods rather than relying heavily on supplements. Whole foods offer a variety of nutrients that your body and mind need to function at their best.")
            st.markdown(f"#### 7. Explore Different Diets")
            st.write(f"Some eating styles, like the Mediterranean diet, have been linked to better mental health. This diet emphasizes fresh fruits and vegetables, whole grains, fish, and healthy fats like olive oil.")
            st.markdown(f"#### 8. Time Your Meals")
            st.write(f"Try to stick to regular meal times and avoid skipping meals. This can help keep your blood sugar levels stable, which in turn can help regulate your mood.")
            st.markdown(f"#### 9. Seek Expert Advice")
            st.write(f"If you're unsure about what to eat or if you have specific dietary concerns, consider talking to a registered dietitian or nutritionist. They can offer personalized advice tailored to your needs.")
            st.markdown(f"#### 10. Listen to Your Body")
            st.write(f"Pay attention to how different foods make you feel. Keeping a food diary can help you identify any patterns between your diet and your mood.")
            st.write(f"\n\nBy making small changes to your diet, you can take positive steps towards supporting your mental health and well-being.")
            st.image("food_image.jpg")

            st.markdown(f"# Sleep Schedule")
            st.write(f"Getting enough quality sleep is crucial for your mental health. Here are some tips to help you improve your sleep schedule:")
            st.markdown(f"#### 1. Consistency is Key")
            st.write(f"Aim to go to bed and wake up at the same time every day, even on weekends. Consistency helps regulate your body's internal clock, making it easier to fall asleep and wake up feeling refreshed.")
            st.markdown(f"#### 2. Create a Bedtime Routine")
            st.write(f"Develop a relaxing bedtime routine to signal to your body that it's time to wind down. This could include activities like reading, taking a warm bath, or practicing relaxation techniques such as deep breathing or meditation.")
            st.markdown(f"#### 3. Limit Screen Time Before Bed")
            st.write(f"Minimize exposure to screens (phones, tablets, computers, TVs) at least an hour before bedtime. The blue light emitted by screens can interfere with your body's production of melatonin, the hormone that regulates sleep.")
            st.markdown(f"#### 4. Watch Your Caffeine Intake")
            st.write(f"Be mindful of consuming caffeine in the afternoon and evening, as it can disrupt your sleep. Try to limit caffeine intake to the morning hours or switch to decaffeinated options later in the day.")
            st.markdown(f"#### 5. Create a Comfortable Sleep Environment")
            st.write(f"Make your bedroom conducive to sleep by keeping it cool, dark, and quiet. Invest in a comfortable mattress and pillows, and consider using blackout curtains or white noise machines to block out any disturbances.")
            st.markdown(f"#### 6. Limit Naps")
            st.write(f"While short naps can be refreshing, avoid taking long naps during the day, especially close to bedtime. Napping too much or too late in the day can interfere with your ability to fall asleep at night.")
            st.markdown(f"#### 7. Get Regular Exercise")
            st.write(f"Engage in regular physical activity during the day, but try to avoid vigorous exercise close to bedtime. Exercise can help improve sleep quality and reduce symptoms of anxiety and depression.")
            st.markdown(f"#### 8. Watch Your Diet")
            st.write(f"Be mindful of what you eat and drink, especially in the hours leading up to bedtime. Avoid heavy meals, spicy foods, and excessive liquids, which can cause discomfort and disrupt sleep.")
            st.markdown(f"#### 9. Manage Stress")
            st.write(f"Practice stress-reduction techniques such as mindfulness, yoga, or journaling to help calm your mind and prepare for sleep. Managing stress can improve both the quality and duration of your sleep.")
            st.markdown(f"#### 10. Seek Professional Help if Needed")
            st.write(f"If you're struggling with persistent sleep problems or insomnia that are affecting your mental health, don't hesitate to seek help from a healthcare professional. They can provide personalized advice and treatment options to address your sleep issues.")
            st.write(f"\n\nBy prioritizing your sleep and following these recommendations, you can improve your mental health and overall well-being.")
            st.image("sleep.jpg")
            
            st.markdown(f"# Exercise Recommendations")
            st.write(f"Physical activity is not only good for your body but also for your mental health. Here are some exercise recommendations to boost your mood and well-being:")
            st.markdown(f"#### 1. Find Activities You Enjoy")
            st.write(f"Choose activities that you enjoy and that fit your lifestyle. Whether it's walking, dancing, swimming, or yoga, find something that makes you feel good and keeps you motivated.")
            st.markdown(f"#### 2. Start Slowly and Build Up")
            st.write(f"If you're new to exercise, start slowly and gradually increase the intensity and duration of your workouts. This can help prevent injury and make exercise more enjoyable.")
            st.markdown(f"#### 3. Set Realistic Goals")
            st.write(f"Set achievable goals for your fitness routine. Whether it's walking for 30 minutes a day or running a 5K, having clear goals can help keep you focused and motivated.")
            st.markdown(f"#### 4. Mix It Up")
            st.write(f"Include a variety of activities in your exercise routine to keep things interesting and prevent boredom. Try different types of workouts, such as strength training, cardio, and flexibility exercises.")
            st.markdown(f"#### 5. Stay Consistent")
            st.write(f"Consistency is key when it comes to exercise. Aim to be active most days of the week, even if it's just for a short walk or a quick workout at home.")
            st.markdown(f"#### 6. Listen to Your Body")
            st.write(f"Pay attention to how your body feels during and after exercise. If you experience pain or discomfort, stop the activity and consult a healthcare professional.")
            st.markdown(f"#### 7. Get Moving Throughout the Day")
            st.write(f"Find ways to incorporate movement into your daily routine, such as taking the stairs instead of the elevator, parking farther away from your destination, or doing quick stretches during breaks.")
            st.markdown(f"#### 8. Buddy Up")
            st.write(f"Exercise with a friend or family member to help stay motivated and accountable. Having a workout buddy can make exercise more fun and enjoyable.")
            st.markdown(f"#### 9. Stay Hydrated")
            st.write(f"Don't forget to drink plenty of water before, during, and after your workouts. Staying hydrated is essential for optimal performance and recovery.")
            st.markdown(f"#### 10. Rest and Recover")
            st.write(f"Give your body time to rest and recover between workouts. This can help prevent burnout and reduce the risk of overuse injuries.")
            st.write(f"\n\nBy incorporating regular physical activity into your routine, you can improve your mood, reduce stress, and boost your overall mental well-being.")
            st.image("Mental-Health-Benefits-of-Exercise.jpg")
            
            st.markdown(f"# Breathing Exercises - Breathing in, Breathing out")
            st.write("Meditate to calm your mind")
            st.video("https://youtu.be/8vkYJf8DOsc?si=G2skZLg0dsrZBkxa")
        else:
            st.warning("Please login/signup to meditate.")
    else:
        st.error("Invalid page selection.")


if __name__ == "__main__":
    initialize_database()
    main()
