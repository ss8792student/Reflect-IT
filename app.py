import streamlit as st
import uuid
from reflect_engine import ReflectEngine
from firebase_logger import log_message

st.set_page_config(page_title="Reflect-IT", page_icon="🪞", layout="wide")

engine = ReflectEngine()

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # unique ID per user session

if "history" not in st.session_state:
    st.session_state.history = []

if "current_subject" not in st.session_state:
    st.session_state.current_subject = None

st.title("🪞 Reflect-IT")

subject = st.sidebar.selectbox(
    "Choose a subject:",
    ["Science", "Math", "History"]
)

if subject != st.session_state.current_subject:
    st.session_state.current_subject = subject
    st.session_state.history = []

    intro = engine.intro_message(subject)
    st.session_state.history.append(("ai", intro))
    log_message(st.session_state.session_id, "ai", intro, subject)  # log intro

for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)

user_input = st.chat_input("Type your message…")

if user_input:
    st.session_state.history.append(("user", user_input))
    
    st.chat_message("user").write(user_input)
    
    log_message(st.session_state.session_id, "user", user_input, subject)

    ai_response = engine.generate(user_input, subject)
    st.session_state.history.append(("ai", ai_response))
    
    st.chat_message("assistant").write(ai_response)
    
    log_message(st.session_state.session_id, "ai", ai_response, subject)

