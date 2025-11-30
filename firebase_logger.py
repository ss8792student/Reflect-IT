import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json
import streamlit as st

# load json key from streamlit secrets
firebase_key = st.secrets["FIREBASE_API_KEY"]
cred = credentials.Certificate(json.loads(firebase_key))

# initialize firebase app once
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def log_message(session_id, role, message, subject=None):
    """
    Logs a single message under the user's session.
    Each session_id has its own document, messages are in a subcollection.
    """
    # reference the session doc
    session_ref = db.collection("reflect-it-sessions").document(session_id)
    # add message to 'messages' subcollection
    session_ref.collection("messages").add({
        "role": role,
        "message": message,
        "subject": subject,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
