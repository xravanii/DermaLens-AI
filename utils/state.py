import streamlit as st
import datetime

# Exported so app.py can use it for nav_step validation
STEP_ORDER = ["welcome", "upload", "verification", "questionnaire", "questionnaire_summary", "analysis", "report"]
STEP_IDX   = {s: i for i, s in enumerate(STEP_ORDER)}


def init_state():
    """Initialises all session state variables needed for navigation and data storage."""
    defaults = {
        "current_step":           "welcome",
        "uploaded_image":         None,
        "uploaded_image_name":    None,
        "uploaded_image_size":    None,
        "answers":                [None, None, None, None],
        "current_question_index": 0,
        "scan_history":           [],
        "auth_user":              None,   # None = guest / logged out
        "history_logged":         False,
        "uploader_key":           100,
        "selected_tip":           None,
        "chat_messages":          [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def reset_scan():
    """Resets all fields related to a single scan run, preserving auth and history."""
    st.session_state.current_step           = "welcome"
    st.session_state.uploaded_image         = None
    st.session_state.uploaded_image_name    = None
    st.session_state.uploaded_image_size    = None
    st.session_state.answers                = [None, None, None, None]
    st.session_state.current_question_index = 0
    st.session_state.history_logged         = False
    st.session_state.uploader_key           = st.session_state.get("uploader_key", 100) + 1
    st.session_state.chat_messages          = []


def navigate_to(step_name: str):
    """Sets the current active step in the application flow."""
    st.session_state.current_step = step_name


def add_to_history(date_str, score, concern, skin_type, answers=None):
    """Appends an analysis result to the persistent scan history list."""
    st.session_state.scan_history.append({
        "date":      date_str,
        "score":     score,
        "concern":   concern,
        "skin_type": skin_type,
        "answers":   answers or [],
    })
