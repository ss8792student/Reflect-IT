import streamlit as st
from main import handle_message

st.set_page_config(page_title="Reflect-IT Tutor", page_icon="🪞", layout="centered")

st.title("🪞 Reflect-IT Adaptive Tutor")
st.caption("Teachable AI that helps you refine your understanding and reasoning through reflection.")

st.sidebar.header("📚 Select Your Subject")
subject = st.sidebar.radio(
    "Choose your subject:",
    ["Science", "History", "Math"],
    index=0
)

student = st.sidebar.text_input("Student ID (e.g., S1)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Explain your concept or ask a question...", key="chat_input_main")

if user_input:
    if student and subject:
        response = handle_message(student, subject, user_input)
        st.session_state.chat_history.append(("student", user_input))
        st.session_state.chat_history.append(("ai", response))
    else:
        st.warning("Please enter your Student ID and select a subject first.")

for role, message in st.session_state.chat_history:
    if role == "student":
        with st.chat_message("user"):
            st.markdown(message)
    else:
        with st.chat_message("assistant"):
            st.markdown(message)

st.markdown("---")
st.markdown("<small>Reflect-IT © 2025</small>", unsafe_allow_html=True)


