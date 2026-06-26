import streamlit as st
from utils.state import navigate_to

# SVG icons for question categories
QUESTION_ICONS = [
    # Water drop (oiliness)
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#4D9FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
    # Droplets (washing)
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#4D9FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/></svg>',
    # Band-aid (dry patches)
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#4D9FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="8" width="20" height="8" rx="4"/><path d="M9 12h6"/><path d="M12 9v6"/></svg>',
    # Face / t-zone
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#4D9FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="5"/><path d="M12 13v8"/><path d="M9 18h6"/></svg>',
]

# Definition of the 4 clinical questions
QUESTIONS = [
    {
        "text": "How oily does your skin become after a few hours?",
        "options": ["Very Dry", "Balanced", "Oily", "Very Oily"],
    },
    {
        "text": "How does your skin feel after washing?",
        "options": ["Tight", "Comfortable", "Slightly Oily"],
    },
    {
        "text": "Do you experience dry patches?",
        "options": ["Never", "Rarely", "Sometimes", "Frequently"],
    },
    {
        "text": "Is your T-zone oily while your cheeks remain dry?",
        "options": ["No", "Sometimes", "Yes"],
    }
]

# Warning icon SVG
ICON_WARN = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#B45309" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'


def render_questionnaire_screen():
    """Renders one question at a time (Screen 4) with validation and state preservation."""
    idx = st.session_state.current_question_index
    total_q = len(QUESTIONS)
    current_q = QUESTIONS[idx]

    with st.container():
        # Top progress row
        progress_pct = int(((idx + 1) / total_q) * 100)
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
            <span style="font-size:0.78rem;font-weight:700;color:#4D9FFF;text-transform:uppercase;
                         letter-spacing:0.08em;font-family:'Inter',sans-serif;">
                Questionnaire
            </span>
            <span style="font-size:0.78rem;font-weight:600;color:#8A9BB5;font-family:'Inter',sans-serif;">
                Question {idx + 1} of {total_q} &nbsp;·&nbsp; {progress_pct}% Complete
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar
        progress_val = float(idx + 1) / float(total_q)
        st.progress(progress_val)
        st.write("")

        # Question icon + text
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1rem;">
            <div style="width:42px;height:42px;border-radius:14px;
                        background:linear-gradient(135deg,rgba(77,159,255,0.15),rgba(6,182,212,0.1));
                        border:1.5px solid rgba(77,159,255,0.25);
                        display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                {QUESTION_ICONS[idx]}
            </div>
            <div>
                <div style="font-size:0.7rem;font-weight:700;color:#4D9FFF;text-transform:uppercase;
                            letter-spacing:0.08em;font-family:'Inter',sans-serif;margin-bottom:0.15rem;">
                    Q{idx + 1}
                </div>
                <div style="font-size:1.15rem;font-weight:800;color:#0A1628;font-family:'Inter',sans-serif;
                            letter-spacing:-0.02em;line-height:1.3;">
                    {current_q['text']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Find default index from state
        current_saved_answer = st.session_state.answers[idx]
        if current_saved_answer in current_q["options"]:
            default_idx = current_q["options"].index(current_saved_answer)
        else:
            default_idx = None

        # Radio selection
        selected_option = st.radio(
            current_q["text"],
            options=current_q["options"],
            index=default_idx,
            key=f"q_{idx}_radio",
            label_visibility="collapsed"
        )

        # Save selection back to state
        if selected_option is not None:
            st.session_state.answers[idx] = selected_option

        # Helper hint
        if selected_option is None:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.5rem;margin-top:0.75rem;
                        padding:0.65rem 1rem;background:rgba(245,158,11,0.08);
                        border:1px solid rgba(245,158,11,0.2);border-radius:12px;">
                {ICON_WARN}
                <span style="font-size:0.8rem;color:#B45309;font-weight:600;font-family:'Inter',sans-serif;">
                    Please select an answer to continue.
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)

        col_prev, col_next = st.columns(2)
        has_answered = st.session_state.answers[idx] is not None

        with col_prev:
            if idx == 0:
                if st.button("Previous Step", type="secondary", key="prev_btn"):
                    navigate_to("verification")
                    st.rerun()
            else:
                if st.button("Previous Question", type="secondary", key="prev_btn"):
                    st.session_state.current_question_index -= 1
                    st.rerun()

        with col_next:
            if idx < total_q - 1:
                if st.button("Next Question", type="primary", disabled=not has_answered, key="next_btn"):
                    st.session_state.current_question_index += 1
                    st.rerun()
            else:
                if st.button("Finish and Review", type="primary", disabled=not has_answered, key="next_btn"):
                    navigate_to("questionnaire_summary")
                    st.rerun()
