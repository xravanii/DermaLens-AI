import streamlit as st
from utils.state import navigate_to, reset_scan
from components.ui import ICON_SCAN, ICON_CALENDAR


def render_history_screen():
    """Renders the Scan History page."""

    with st.container():
        st.markdown("""
        <h2 style="font-size:1.65rem;font-weight:800;margin-bottom:0.4rem;
                   font-family:'Inter',sans-serif;color:#0A1628;letter-spacing:-0.03em;">
            Scan History
        </h2>
        <p style="color:#8A9BB5;margin-bottom:1.75rem;font-size:0.9rem;
                  font-family:'Inter',sans-serif;">
            A record of all your previous DermaLens AI skin analysis sessions.
        </p>
        """, unsafe_allow_html=True)

        history = st.session_state.get("scan_history", [])

        if not history:
            st.markdown("""
            <div style="text-align:center;padding:3rem 1rem;">
                <div style="width:56px;height:56px;border-radius:18px;background:rgba(77,159,255,0.08);
                            border:1.5px solid rgba(77,159,255,0.15);display:inline-flex;
                            align-items:center;justify-content:center;margin-bottom:1rem;">
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#4D9FFF" stroke-width="1.5"
                         stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                    </svg>
                </div>
                <div style="font-size:1rem;font-weight:700;color:#0A1628;font-family:'Inter',sans-serif;margin-bottom:0.4rem;">
                    No scans yet
                </div>
                <div style="font-size:0.85rem;color:#8A9BB5;font-family:'Inter',sans-serif;">
                    Complete your first skin analysis to see results here.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for i, scan in enumerate(reversed(history)):
                scan_idx = len(history) - 1 - i  # original index
                _render_history_card(scan, scan_idx)

        st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            if st.button("Start New Scan", type="primary", key="hist_new_scan"):
                reset_scan()
                st.rerun()
        with col1:
            if st.button("Back", type="secondary", key="hist_back"):
                navigate_to("welcome")
                st.rerun()


def _render_history_card(scan, idx):
    """Renders a single scan history card."""
    score = scan.get("score", 0)
    if score >= 80:
        score_color = "#22C55E"
    elif score >= 60:
        score_color = "#4D9FFF"
    elif score >= 40:
        score_color = "#F59E0B"
    else:
        score_color = "#EF4444"

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.88);border:1.5px solid rgba(77,159,255,0.12);
                border-radius:16px;padding:1.25rem 1.5rem;margin-bottom:0.85rem;
                box-shadow:0 2px 8px rgba(10,22,40,0.06);transition:all 0.3s ease;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.75rem;">
            <div>
                <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.3rem;">
                    {ICON_CALENDAR}
                    <span style="font-weight:700;font-size:0.9rem;color:#0A1628;font-family:'Inter',sans-serif;">
                        {scan.get('date', '—')}
                    </span>
                </div>
                <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
                    <span class="stat-pill">{scan.get('skin_type', '—')} Skin</span>
                    <span class="stat-pill">{scan.get('concern', '—')}</span>
                </div>
            </div>
            <div style="text-align:center;flex-shrink:0;">
                <div style="font-size:1.75rem;font-weight:800;color:{score_color};
                            font-family:'Inter',sans-serif;letter-spacing:-0.04em;line-height:1;">
                    {score}
                </div>
                <div style="font-size:0.65rem;text-transform:uppercase;font-weight:700;
                            color:#8A9BB5;font-family:'Inter',sans-serif;letter-spacing:0.06em;">
                    / 100
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # View Report button navigates back to report page
    if st.button("View Report", key=f"hist_view_{idx}", type="secondary"):
        navigate_to("report")
        st.rerun()
