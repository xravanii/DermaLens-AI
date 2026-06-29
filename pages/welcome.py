import streamlit as st
from utils.state import navigate_to

def render_welcome_screen():
    """Renders the introductory Welcome Screen of the dermatology scan app."""

    with st.container():
        st.markdown("""
        <div style="text-align:center;margin-bottom:0.5rem;">
            <div style="display:inline-flex;align-items:center;gap:0.5rem;background:rgba(77,159,255,0.1);
                        border:1px solid rgba(77,159,255,0.2);border-radius:50px;padding:0.3rem 1rem;margin-bottom:1.5rem;">
                <span style="width:8px;height:8px;border-radius:50%;background:#22C55E;display:inline-block;"></span>
                <span style="font-size:0.78rem;font-weight:600;color:#4D9FFF;letter-spacing:0.05em;font-family:'Inter',sans-serif;">
                    AI-Powered · HIPAA Safe · Instant Results
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<h1 class="brand-title">DermaLens <span style="color:#4D9FFF;">AI</span></h1>', unsafe_allow_html=True)
        st.markdown('<p class="brand-tagline">Clinically-Inspired Skin Analysis</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="brand-subtitle">Upload a photo of your skin and receive an instant AI-powered dermatology assessment, personalised regimen, and ingredient recommendations — in under 60 seconds.</p>',
            unsafe_allow_html=True
        )

        # Feature pills
        st.markdown("""
        <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:0.5rem;margin-bottom:2rem;">
            <span class="stat-pill">Multi-Spectral Analysis</span>
            <span class="stat-pill">Ingredient Matching</span>
            <span class="stat-pill">Regimen Builder</span>
            <span class="stat-pill">100% Private</span>
        </div>
        """, unsafe_allow_html=True)

        # Illustration
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                st.image("assets/welcome_illustration.png", use_container_width=True)
            except Exception:
                st.markdown(
                    "<div style='height:200px;background:linear-gradient(135deg,rgba(77,159,255,0.1),rgba(6,182,212,0.08));border-radius:20px;display:flex;align-items:center;justify-content:center;color:#4D9FFF;font-weight:700;font-family:Inter,sans-serif;border:1px solid rgba(77,159,255,0.2);font-size:0.95rem;'>Dermatology Scanner Illustration</div>",
                    unsafe_allow_html=True
                )

        st.write("")

        # Start button
        col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 1.5, 1])
        with col_btn_2:
            if st.button("Start Skin Scan", type="primary", key="start_scan_btn"):
                navigate_to("upload")
                st.rerun()

        st.markdown('<div style="text-align:center;margin-top:1rem;font-size:0.75rem;color:#8A9BB5;font-family:Inter,sans-serif;">No account required · Results in 60 seconds</div>', unsafe_allow_html=True)
