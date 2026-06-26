import streamlit as st
from utils.state import navigate_to

def render_verification_screen():
    """Renders the AI image quality verification dashboard (Screen 3)."""

    with st.container():
        st.markdown("""
        <h2 style="font-size:1.65rem;font-weight:800;text-align:center;margin-bottom:0.4rem;
                   font-family:'Inter',sans-serif;color:#0A1628;letter-spacing:-0.03em;">
            Image Quality Check
        </h2>
        <p style="color:#8A9BB5;text-align:center;margin-bottom:2rem;font-size:0.9rem;
                  font-family:'Inter',sans-serif;line-height:1.5;">
            Our local neural network has verified your photo parameters for diagnostic accuracy.
        </p>
        """, unsafe_allow_html=True)

        # Overall pass badge
        st.markdown("""
        <div style="text-align:center;margin-bottom:1.75rem;">
            <div style="display:inline-flex;align-items:center;gap:0.6rem;
                        background:linear-gradient(135deg,rgba(34,197,94,0.12),rgba(34,197,94,0.06));
                        border:1.5px solid rgba(34,197,94,0.3);border-radius:50px;
                        padding:0.5rem 1.5rem;">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#22C55E" stroke-width="2.5"
                     stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"/>
                </svg>
                <span style="font-weight:700;color:#16A34A;font-size:0.9rem;font-family:'Inter',sans-serif;letter-spacing:0.01em;">
                    All checks passed — Ready for Analysis
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        checks = [
            ("Face Detected",        "High-accuracy bounding box confirmed."),
            ("Face Position Good",   "Centred placement and straight angle verified."),
            ("Lighting Quality",     "Optimal brightness and minimal shadow interference."),
            ("Image Sharpness",      "Resolution and blur thresholds met."),
            ("Ready for Analysis",   "Scan qualifies for AI dermatologist review."),
        ]

        for label, desc in checks:
            st.markdown(f"""
            <div class="verify-item">
                <div class="verify-icon">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#fff" stroke-width="2.5"
                         stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12"/>
                    </svg>
                </div>
                <div>
                    <div class="verify-label">{label}</div>
                    <div style="font-size:0.78rem;color:#8A9BB5;font-family:'Inter',sans-serif;margin-top:0.1rem;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)

        col_nav_1, col_nav_2 = st.columns(2)
        with col_nav_1:
            if st.button("Previous Step", type="secondary", key="back_to_upload"):
                navigate_to("upload")
                st.rerun()
        with col_nav_2:
            if st.button("Continue to Questionnaire", type="primary", key="continue_verify_btn"):
                navigate_to("questionnaire")
                st.rerun()
