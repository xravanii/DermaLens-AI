import streamlit as st
import os

# ── 1. Page Config (must be FIRST Streamlit call) ─────────────
st.set_page_config(
    page_title="DermaLens AI - Personalized Skin Analysis",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 2. Load CSS ────────────────────────────────────────────────
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# ── 3. Import modules ──────────────────────────────────────────
from utils.state import init_state, reset_scan, navigate_to, add_to_history, STEP_IDX
from components.ui import render_header, render_hero
from pages.welcome       import render_welcome_screen
from pages.upload        import render_upload_screen
from pages.verification  import render_verification_screen
from pages.questionnaire import render_questionnaire_screen
from pages.summary       import render_summary_screen
from pages.analysis      import render_analysis_screen
from pages.report        import render_report_screen
from pages.auth          import render_signin_screen, render_signup_screen
from pages.history       import render_history_screen

# ── 4. Initialise state ────────────────────────────────────────
init_state()

# ── 5. Process query-param actions (BEFORE rendering anything) ─
#       Every navbar link fires a ?action=X or ?nav_step=X URL.
#       We intercept here, mutate session_state, clear params, rerun.
_action   = st.query_params.get("action",   None)
_nav_step = st.query_params.get("nav_step", None)

if _action:
    st.query_params.clear()
    if _action == "new_scan":
        reset_scan()
        st.rerun()
    elif _action == "history":
        st.session_state.current_step = "history"
        st.rerun()
    elif _action == "home":
        st.session_state.current_step = "welcome"
        st.rerun()
    elif _action == "signin":
        st.session_state.current_step = "signin"
        st.rerun()
    elif _action == "signup":
        st.session_state.current_step = "signup"
        st.rerun()
    elif _action == "logout":
        st.session_state.auth_user = None
        st.session_state.current_step = "welcome"
        st.rerun()
    elif _action in ("settings", "help"):
        # Future: dedicated pages; for now stay put
        st.session_state.current_step = "welcome"
        st.rerun()
    # Unknown action — ignore silently

elif _nav_step and _nav_step in STEP_IDX:
    current_idx = STEP_IDX.get(st.session_state.current_step, 0)
    nav_idx     = STEP_IDX.get(_nav_step, 0)
    st.query_params.clear()
    if nav_idx < current_idx:          # only allow going back to completed steps
        st.session_state.current_step = _nav_step
        st.rerun()

# ── 6. Render navbar (pure HTML — no Streamlit widgets inside) ─
step = st.session_state.current_step
render_header(step)
render_hero(step)

# ── 7. Route to the correct page ──────────────────────────────
if   step == "welcome":               render_welcome_screen()
elif step == "upload":                render_upload_screen()
elif step == "verification":          render_verification_screen()
elif step == "questionnaire":         render_questionnaire_screen()
elif step == "questionnaire_summary": render_summary_screen()
elif step == "analysis":              render_analysis_screen()
elif step == "report":                render_report_screen()
elif step == "history":               render_history_screen()
elif step == "signin":                render_signin_screen()
elif step == "signup":                render_signup_screen()
else:
    st.session_state.current_step = "welcome"
    st.rerun()
