import streamlit as st
from utils.state import navigate_to

# Simple in-memory user store (session_state prototype)
def _get_users():
    if "registered_users" not in st.session_state:
        st.session_state.registered_users = {}
    return st.session_state.registered_users


def render_signin_screen():
    """Sign In page."""
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        with st.container():
            st.markdown("""
            <h2 style="font-size:1.65rem;font-weight:800;text-align:center;margin-bottom:0.4rem;
                       font-family:'Inter',sans-serif;color:#0A1628;letter-spacing:-0.03em;">
                Sign In
            </h2>
            <p style="color:#8A9BB5;text-align:center;margin-bottom:1.75rem;font-size:0.9rem;
                      font-family:'Inter',sans-serif;">
                Welcome back to DermaLens AI.
            </p>
            """, unsafe_allow_html=True)

            email = st.text_input("Email address", placeholder="you@example.com", key="si_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="si_password")

            st.write("")

            col_back, col_go = st.columns(2)
            with col_back:
                if st.button("Back", type="secondary", key="si_back"):
                    navigate_to("welcome")
                    st.rerun()
            with col_go:
                if st.button("Sign In", type="primary", key="si_submit"):
                    users = _get_users()
                    if email in users and users[email]["password"] == password:
                        st.session_state.auth_user = {
                            "name":  users[email]["name"],
                            "email": email,
                        }
                        navigate_to("welcome")
                        st.rerun()
                    else:
                        st.error("Incorrect email or password. Please try again or sign up.")

            st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)
            st.markdown('<p style="text-align:center;font-size:0.82rem;color:#8A9BB5;font-family:Inter,sans-serif;">No account yet?</p>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1.5, 1])
            with col2:
                if st.button("Create Account", type="secondary", key="si_to_signup"):
                    navigate_to("signup")
                    st.rerun()


def render_signup_screen():
    """Sign Up page."""
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        with st.container():
            st.markdown("""
            <h2 style="font-size:1.65rem;font-weight:800;text-align:center;margin-bottom:0.4rem;
                       font-family:'Inter',sans-serif;color:#0A1628;letter-spacing:-0.03em;">
                Create Account
            </h2>
            <p style="color:#8A9BB5;text-align:center;margin-bottom:1.75rem;font-size:0.9rem;
                      font-family:'Inter',sans-serif;">
                Join DermaLens AI for personalised skin tracking.
            </p>
            """, unsafe_allow_html=True)

            name = st.text_input("Full name", placeholder="Jane Smith", key="su_name")
            email = st.text_input("Email address", placeholder="you@example.com", key="su_email")
            password = st.text_input("Password", type="password", placeholder="Min 6 characters", key="su_password")
            confirm = st.text_input("Confirm password", type="password", placeholder="Repeat password", key="su_confirm")

            st.write("")

            col_back, col_go = st.columns(2)
            with col_back:
                if st.button("Back", type="secondary", key="su_back"):
                    navigate_to("welcome")
                    st.rerun()
            with col_go:
                if st.button("Create Account", type="primary", key="su_submit"):
                    users = _get_users()
                    if not name or not email or not password:
                        st.error("Please fill in all fields.")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters.")
                    elif password != confirm:
                        st.error("Passwords do not match.")
                    elif email in users:
                        st.error("An account with this email already exists. Please sign in.")
                    else:
                        users[email] = {"name": name, "password": password}
                        st.session_state.auth_user = {"name": name, "email": email}
                        navigate_to("welcome")
                        st.rerun()

            st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)
            st.markdown('<p style="text-align:center;font-size:0.82rem;color:#8A9BB5;font-family:Inter,sans-serif;">Already have an account?</p>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1.5, 1])
            with col2:
                if st.button("Sign In instead", type="secondary", key="su_to_signin"):
                    navigate_to("signin")
                    st.rerun()
