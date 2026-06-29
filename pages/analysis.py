import streamlit as st
import time
from utils.state import navigate_to

from io import BytesIO
from ml.predict import predict_image

# SVG icon for analysis loading icon
ICON_ANALYSIS = '<svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 15c6.667-6 13.333 0 20-6"/><path d="M9 22c1.798-1.998 2.518-3.995 2.807-5.993"/><path d="M15 2c-1.798 1.998-2.518 3.995-2.807 5.993"/><path d="m17 6-2.5-2.5"/><path d="m14 8-1-1"/><path d="m7 18 2.5 2.5"/></svg>'


def render_analysis_screen():
    """Renders the simulated AI analysis loading progress page (Screen 6)."""

    with st.container():
        # Header
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:0.5rem;">
            <div style="width:64px;height:64px;border-radius:20px;
                        background:linear-gradient(135deg,#4D9FFF,#06B6D4);
                        display:inline-flex;align-items:center;justify-content:center;
                        margin-bottom:1.25rem;
                        box-shadow:0 8px 24px rgba(77,159,255,0.35);">
                {ICON_ANALYSIS}
            </div>
            <h2 style="font-size:1.65rem;font-weight:800;margin-bottom:0.4rem;
                       font-family:'Inter',sans-serif;color:#0A1628;letter-spacing:-0.03em;">
                Analysing Skin Profile
            </h2>
            <p style="color:#8A9BB5;font-size:0.9rem;font-family:'Inter',sans-serif;
                      margin-bottom:2.25rem;line-height:1.5;">
                Running multi-spectral analysis across dermal layers. This takes just a moment.
            </p>
        </div>
        """, unsafe_allow_html=True)

        progress_bar = st.progress(0.0)
        status_text = st.empty()
# Run AI only once
        if "analysis_result" not in st.session_state:

            uploaded_image = BytesIO(st.session_state.uploaded_image)

            st.session_state.analysis_result = predict_image(uploaded_image)
            


        # Analysis steps
        steps = [
            ("Processing clinical image",                  0.15, 0.6),
            ("Detecting facial landmarks",                 0.35, 0.7),
            ("Analysing pore dilation and sebum density",  0.55, 0.8),
            ("Checking pigmentation and inflammation",      0.75, 0.8),
            ("Cross-referencing dermatological database",  0.90, 0.6),
            ("Generating personalised skin report",         1.00, 0.7),
        ]

        for msg, val, delay in steps:
            status_text.markdown(
                f"""<div style="text-align:center;"><div style="display:inline-flex;align-items:center;gap:0.75rem;
                                background:rgba(77,159,255,0.08);border:1px solid rgba(77,159,255,0.18);
                                border-radius:50px;padding:0.55rem 1.35rem;margin-top:1rem;">
                        <span style="width:8px;height:8px;border-radius:50%;background:#4D9FFF;
                                     flex-shrink:0;"></span>
                        <span style="font-size:0.92rem;font-weight:600;color:#0A1628;
                                     font-family:'Inter',sans-serif;">{msg}...</span>
                    </div></div>""",
                unsafe_allow_html=True
            )
            progress_bar.progress(val)
            time.sleep(delay)

        navigate_to("report")
        st.rerun()
