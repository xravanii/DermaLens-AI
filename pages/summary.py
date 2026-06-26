import streamlit as st
from utils.state import navigate_to

# SVG icons matching questionnaire icons
QUESTION_ICONS_SVG = [
    '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#4D9FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
    '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#4D9FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/></svg>',
    '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#4D9FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="8" width="20" height="8" rx="4"/><path d="M9 12h6"/><path d="M12 9v6"/></svg>',
    '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#4D9FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="5"/><path d="M12 13v8"/><path d="M9 18h6"/></svg>',
]

# DNA icon
ICON_DNA_SMALL = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#4D9FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 15c6.667-6 13.333 0 20-6"/><path d="M9 22c1.798-1.998 2.518-3.995 2.807-5.993"/><path d="M15 2c-1.798 1.998-2.518 3.995-2.807 5.993"/></svg>'

QUESTIONS_TEXT = [
    "How oily does your skin become after a few hours?",
    "How does your skin feel after washing?",
    "Do you experience dry patches?",
    "Is your T-zone oily while your cheeks remain dry?",
]

# Check SVG
ICON_CHECK_GREEN = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#22C55E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'


def estimate_skin_type(answers):
    """Computes a basic clinical heuristic to estimate skin type from answers."""
    q1, q2, q3, q4 = answers
    if q4 == "Yes" or (q4 == "Sometimes" and q1 in ["Balanced", "Oily"]):
        return "Combination"
    elif q1 in ["Oily", "Very Oily"] or q2 == "Slightly Oily":
        return "Oily"
    elif q1 == "Very Dry" or q2 == "Tight" or q3 == "Frequently":
        return "Dry"
    else:
        return "Balanced (Normal)"


def render_summary_screen():
    """Renders the questionnaire results overview before kicking off ML assessment."""

    with st.container():
        st.markdown("""
        <h2 style="font-size:1.65rem;font-weight:800;text-align:center;margin-bottom:0.4rem;
                   font-family:'Inter',sans-serif;color:#0A1628;letter-spacing:-0.03em;">
            Review Your Answers
        </h2>
        <p style="color:#8A9BB5;text-align:center;margin-bottom:2rem;font-size:0.9rem;
                  font-family:'Inter',sans-serif;">
            Confirm your dermatology consultation responses before AI analysis begins.
        </p>
        """, unsafe_allow_html=True)

        answers = st.session_state.answers
        estimated_type = estimate_skin_type(answers)

        # Status badge
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:1.75rem;">
            <div style="display:inline-flex;align-items:center;gap:0.6rem;
                        background:rgba(34,197,94,0.1);border:1.5px solid rgba(34,197,94,0.25);
                        border-radius:50px;padding:0.4rem 1.25rem;">
                {ICON_CHECK_GREEN}
                <span style="font-weight:700;color:#16A34A;font-size:0.85rem;font-family:'Inter',sans-serif;">
                    Questionnaire Completed — 4 / 4
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Answer cards
        for i, (q, a, icon_svg) in enumerate(zip(QUESTIONS_TEXT, answers, QUESTION_ICONS_SVG)):
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:0.85rem;
                        background:rgba(255,255,255,0.85);border:1.5px solid rgba(77,159,255,0.1);
                        border-radius:16px;padding:1rem 1.25rem;margin-bottom:0.65rem;
                        box-shadow:0 2px 8px rgba(10,22,40,0.06);transition:all 0.3s ease;">
                <div style="width:34px;height:34px;border-radius:12px;flex-shrink:0;
                            background:rgba(77,159,255,0.08);border:1px solid rgba(77,159,255,0.18);
                            display:flex;align-items:center;justify-content:center;">
                    {icon_svg}
                </div>
                <div style="flex:1;">
                    <div style="font-size:0.78rem;font-weight:600;color:#8A9BB5;
                                font-family:'Inter',sans-serif;margin-bottom:0.2rem;">Q{i+1}</div>
                    <div style="font-size:0.88rem;color:#4A5568;font-family:'Inter',sans-serif;
                                margin-bottom:0.4rem;line-height:1.4;">{q}</div>
                    <div style="font-size:0.9rem;font-weight:700;color:#0A1628;font-family:'Inter',sans-serif;">
                        {a if a else '—'}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Estimated skin type badge
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:2rem;margin-top:0.5rem;">
            <div style="display:inline-flex;align-items:center;gap:0.75rem;
                        background:#EBF3FF;border:1.5px solid rgba(77,159,255,0.25);
                        border-radius:16px;padding:0.75rem 1.75rem;">
                {ICON_DNA_SMALL}
                <div>
                    <div style="font-size:0.7rem;font-weight:700;color:#4D9FFF;text-transform:uppercase;
                                letter-spacing:0.08em;font-family:'Inter',sans-serif;">Estimated Profile</div>
                    <div style="font-size:1.05rem;font-weight:800;color:#0A1628;font-family:'Inter',sans-serif;
                                letter-spacing:-0.02em;">{estimated_type} Skin</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)

        col_nav_1, col_nav_2 = st.columns(2)
        with col_nav_1:
            if st.button("Edit Answers", type="secondary", key="edit_answers_btn"):
                st.session_state.current_question_index = 0
                navigate_to("questionnaire")
                st.rerun()
        with col_nav_2:
            if st.button("Run AI Analysis", type="primary", key="continue_to_analysis_btn"):
                navigate_to("analysis")
                st.rerun()
