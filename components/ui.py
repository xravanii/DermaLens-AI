import streamlit as st
import random
import math

# ─── SVG Icons (Lucide-style, inline) ─────────────────────────
ICON_DNA      = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 15c6.667-6 13.333 0 20-6"/><path d="M9 22c1.798-1.998 2.518-3.995 2.807-5.993"/><path d="M15 2c-1.798 1.998-2.518 3.995-2.807 5.993"/><path d="m17 6-2.5-2.5"/><path d="m14 8-1-1"/><path d="m7 18 2.5 2.5"/><path d="m3.5 14.5.5.5"/><path d="m20 9 .5.5"/><path d="m6.5 17.5 1 1"/></svg>'
ICON_SCAN     = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" y1="12" x2="17" y2="12"/></svg>'
ICON_HISTORY  = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
ICON_USER     = '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
ICON_LOCK     = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'
ICON_LOGOUT   = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>'
ICON_CHECK    = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#22C55E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
ICON_TIP      = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#4D9FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
ICON_FLASK    = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6l1 9H8L9 3z"/><path d="M6.2 20.6A2 2 0 0 0 8 22h8a2 2 0 0 0 1.8-1.4L20 12H4l2.2 8.6z"/></svg>'
ICON_MAP      = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" y1="3" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="21"/></svg>'
ICON_TARGET   = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
ICON_CALENDAR = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
ICON_BOT      = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></svg>'
ICON_DOWNLOAD = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'
ICON_PLUS     = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>'
ICON_SETTINGS = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'
ICON_HELP     = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'

# ─── Step metadata ─────────────────────────────────────────────
STEP_ORDER = ["welcome", "upload", "verification", "questionnaire", "questionnaire_summary", "analysis", "report"]
STEP_LABELS = {
    "welcome":               "Welcome",
    "upload":                "Upload",
    "verification":          "Image Check",
    "questionnaire":         "Questionnaire",
    "questionnaire_summary": "Review",
    "analysis":              "Analysing",
    "report":                "Report",
}
HERO_META = {
    "welcome":               {"title": "Welcome to DermaLens AI",            "desc": "Get a clinically-inspired skin analysis powered by AI in under 60 seconds.", "time": "~60 sec",  "step": "Step 1 of 6 — Start"},
    "upload":                {"title": "Upload Your Skin Photo",              "desc": "Provide a high-resolution, well-lit image of the target skin area.",            "time": "~10 sec",  "step": "Step 2 of 6 — Image Upload"},
    "verification":          {"title": "Image Quality Check",                 "desc": "Our neural model verifies image parameters before clinical analysis begins.",    "time": "~5 sec",   "step": "Step 3 of 6 — Verification"},
    "questionnaire":         {"title": "Skin Health Questionnaire",           "desc": "Answer 4 quick clinical questions to personalise your assessment.",              "time": "~30 sec",  "step": "Step 4 of 6 — Questionnaire"},
    "questionnaire_summary": {"title": "Review Your Answers",                 "desc": "Confirm your questionnaire responses before running the AI analysis.",           "time": "~5 sec",   "step": "Step 5 of 6 — Review"},
    "analysis":              {"title": "AI Analysis in Progress",             "desc": "Multi-spectral dermal analysis running — please wait.",                          "time": "~15 sec",  "step": "Step 6 of 6 — Analysis"},
    "report":                {"title": "Your Skin Report is Ready",           "desc": "Review your personalised dermatology-grade assessment and regimen.",              "time": "Done",     "step": "Complete"},
    "history":               {"title": "Scan History",                        "desc": "Review all previous skin analysis sessions.",                                     "time": "—",        "step": "History"},
    "signin":                {"title": "Sign In",                             "desc": "Access your DermaLens AI account.",                                               "time": "—",        "step": "Account"},
    "signup":                {"title": "Create Account",                      "desc": "Join DermaLens AI for personalised skin tracking.",                               "time": "—",        "step": "Account"},
}

STEP_IDX = {s: i for i, s in enumerate(STEP_ORDER)}


def render_header(current_step: str):
    """Renders the fixed header bar as pure HTML — zero Streamlit widgets inside it.
    All interactive buttons are <a href='?action=X'> links processed by app.py."""

    current_idx = STEP_IDX.get(current_step, 0)
    user = st.session_state.get("auth_user", None)

    # ── Step progress ─────────────────────────────────────────
    steps_html = ""
    for i, key in enumerate(STEP_ORDER):
        label = STEP_LABELS[key]
        if i < current_idx:
            steps_html += f'<a class="dl-step-label done" href="?nav_step={key}" title="Return to {label}">{label}</a>'
        elif i == current_idx:
            steps_html += f'<span class="dl-step-label active">{label}</span>'
        else:
            steps_html += f'<span class="dl-step-label">{label}</span>'
        if i < len(STEP_ORDER) - 1:
            steps_html += '<span class="dl-step-sep">›</span>'

    # ── Profile button + dropdown ─────────────────────────────
    if user:
        avatar_inner = f'<span class="dl-avatar-letter">{user["name"][0].upper()}</span>'
        profile_info = (
            f'<div class="dl-drop-user-info">'
            f'<div class="dl-drop-avatar">{user["name"][0].upper()}</div>'
            f'<div>'
            f'<div class="dl-drop-name">{user["name"]}</div>'
            f'<div class="dl-drop-email">{user["email"]}</div>'
            f'</div>'
            f'</div>'
            f'<div class="dl-drop-sep"></div>'
        )
        dropdown_items = (
            f'{profile_info}'
            f'<a href="?action=history" class="dl-drop-item">{ICON_HISTORY} <span>Scan History</span></a>'
            f'<a href="?action=settings" class="dl-drop-item">{ICON_SETTINGS} <span>Settings</span></a>'
            f'<a href="?action=help" class="dl-drop-item">{ICON_HELP} <span>Help</span></a>'
            f'<div class="dl-drop-sep"></div>'
            f'<a href="?action=logout" class="dl-drop-item dl-drop-danger">{ICON_LOGOUT} <span>Logout</span></a>'
        )
        profile_section = (
            f'<div class="dl-profile-wrap">'
            f'<div class="dl-profile-btn" title="Account">{avatar_inner}</div>'
            f'<div class="dl-dropdown">{dropdown_items}</div>'
            f'</div>'
        )
    else:
        # Guest: show a direct Sign In link button — no dropdown
        profile_section = f'<a href="?action=signin" class="dl-nav-btn">{ICON_USER} Sign In</a>'

    # ── Full header HTML ──────────────────────────────────────
    header_html = (
        f'<div class="dl-header">'
        f'<a class="dl-logo" href="?action=home">'
        f'<div class="dl-logo-icon">{ICON_DNA}</div>'
        f'<div class="dl-logo-text">Derma<span>Lens</span> AI</div>'
        f'</a>'
        f'<nav class="dl-steps">{steps_html}</nav>'
        f'<div class="dl-nav-actions">'
        f'<a href="?action=new_scan" class="dl-nav-btn dl-nav-primary">{ICON_PLUS} New Scan</a>'
        f'<a href="?action=history"  class="dl-nav-btn">{ICON_HISTORY} History</a>'
        f'{profile_section}'
        f'</div>'
        f'</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)


def render_hero(current_step: str):
    """Injects the compact blue hero banner below the navbar."""
    meta = HERO_META.get(current_step, HERO_META["welcome"])
    st.markdown(f"""
    <div class="dl-hero">
      <div class="dl-hero-main">
        <div class="dl-hero-tag">{meta['step']}</div>
        <div class="dl-hero-title">{meta['title']}</div>
        <div class="dl-hero-desc">{meta['desc']}</div>
      </div>
      <div class="dl-hero-meta">
        <span class="dl-hero-badge"><span class="dot"></span>Est. Time: {meta['time']}</span>
        <span class="dl-hero-badge">{ICON_LOCK} HIPAA Safe · Local Processing</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Metric helpers ────────────────────────────────────────────

def render_circular_metric(label, value, percentage, size=90, stroke=8, color="#4D9FFF"):
    r = 40
    circumference = 2 * math.pi * r
    dashoffset = circumference - (percentage / 100.0) * circumference
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;margin:0.5rem;position:relative;">
        <svg width="{size}" height="{size}" viewBox="0 0 100 100" style="transform:rotate(-90deg);">
            <circle cx="50" cy="50" r="{r}" stroke="#EBF3FF" stroke-width="{stroke}" fill="transparent"/>
            <circle cx="50" cy="50" r="{r}" stroke="{color}" stroke-width="{stroke}" fill="transparent"
                    stroke-dasharray="{circumference}" stroke-dashoffset="{dashoffset}"
                    stroke-linecap="round" style="transition:stroke-dashoffset 1s ease-in-out;"/>
        </svg>
        <div style="position:absolute;text-align:center;top:50%;transform:translateY(-50%);">
            <span style="font-size:1.1rem;font-weight:800;color:#0A1628;font-family:'Inter',sans-serif;">{value}</span>
        </div>
        <span style="font-size:0.7rem;text-transform:uppercase;font-weight:700;color:#8A9BB5;margin-top:0.5rem;letter-spacing:0.08em;font-family:'Inter',sans-serif;">{label}</span>
    </div>
    """


def render_large_health_score(score):
    r = 42
    circumference = 2 * math.pi * r
    dashoffset = circumference - (score / 100.0) * circumference
    if score >= 80:
        color, label = "#22C55E", "Excellent"
    elif score >= 60:
        color, label = "#4D9FFF", "Good"
    elif score >= 40:
        color, label = "#F59E0B", "Fair"
    else:
        color, label = "#EF4444", "Needs Care"
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;margin:1rem 0;position:relative;">
        <svg width="190" height="190" viewBox="0 0 100 100" style="transform:rotate(-90deg);">
            <circle cx="50" cy="50" r="{r}" stroke="#EBF3FF" stroke-width="6" fill="transparent"/>
            <circle cx="50" cy="50" r="{r}" stroke="{color}" stroke-width="6" fill="transparent"
                    stroke-dasharray="{circumference}" stroke-dashoffset="{dashoffset}"
                    stroke-linecap="round" style="transition:stroke-dashoffset 1.2s ease-in-out;"/>
        </svg>
        <div style="position:absolute;display:flex;flex-direction:column;align-items:center;justify-content:center;">
            <span style="font-size:2.6rem;font-weight:800;color:#0A1628;line-height:1;font-family:'Inter',sans-serif;letter-spacing:-0.04em;">{score}</span>
            <span style="font-size:0.72rem;color:#8A9BB5;font-weight:600;font-family:'Inter',sans-serif;letter-spacing:0.04em;text-transform:uppercase;">/ 100</span>
            <span style="font-size:0.78rem;color:{color};font-weight:700;font-family:'Inter',sans-serif;margin-top:0.2rem;">{label}</span>
        </div>
    </div>
    """


def get_daily_tip():
    tips = [
        "Always apply sunscreen (SPF 30+) even on cloudy days. UV radiation accelerates skin aging and dark spots.",
        "Double cleansing at night is critical to break down sebum, SPF, and environmental pollution thoroughly.",
        "Pat your face dry with a clean microfiber towel; rubbing causes friction and worsens skin irritation.",
        "Hyaluronic acid works best when applied to slightly damp skin to seal in optimal hydration.",
        "Incorporate one active ingredient at a time when starting a new routine to isolate and monitor skin sensitivity.",
        "Clean your smartphone screen regularly. It harbors acne-causing bacteria that transfers to your cheeks.",
        "Moisturizing is vital even for oily skin. Depriving oily skin of hydration can trigger excess sebum production.",
    ]
    if "selected_tip" not in st.session_state:
        st.session_state.selected_tip = random.choice(tips)
    return st.session_state.selected_tip


def render_privacy_notice():
    st.markdown(f"""
    <div class="privacy-card">
        <div style="display:flex;align-items:center;gap:0.6rem;color:#8A9BB5;font-size:0.78rem;font-family:'Inter',sans-serif;">
            {ICON_LOCK}
            <span><strong style="color:#4A5568;">Privacy &amp; HIPAA Notice:</strong> Your uploaded images are processed locally in real-time, encrypted end-to-end, and are not permanently stored on any server.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_chat_widget():
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.5rem;margin-top:1.5rem;margin-bottom:0.5rem;">
        {ICON_BOT}
        <span style="font-size:1.05rem;font-weight:700;color:#0A1628;font-family:'Inter',sans-serif;">AI Dermatologist Assistant</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Ask follow-up questions about your scan report or skin health.")
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-end;margin-bottom:0.75rem;">
                <div style="background:linear-gradient(135deg,#4D9FFF,#06B6D4);color:#fff;padding:0.7rem 1.2rem;border-radius:18px 18px 4px 18px;max-width:80%;font-size:0.88rem;font-family:'Inter',sans-serif;box-shadow:0 4px 12px rgba(77,159,255,0.25);">
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-start;margin-bottom:0.75rem;">
                <div style="background:rgba(240,244,250,0.9);color:#0A1628;padding:0.7rem 1.2rem;border-radius:18px 18px 18px 4px;max-width:80%;font-size:0.88rem;font-family:'Inter',sans-serif;border:1px solid rgba(77,159,255,0.12);">
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    user_input = st.chat_input("Ask DermaLens AI...")
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        st.session_state.chat_messages.append({"role": "assistant", "content": "This feature will be available in a future update."})
        st.rerun()
