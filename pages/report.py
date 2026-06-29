import streamlit as st
from utils.state import navigate_to, add_to_history
from utils.ml_service import analyze_skin
from components.ui import (
    ICON_CHECK, ICON_MAP, ICON_TARGET, ICON_TIP, ICON_BOT, ICON_FLASK, ICON_LOCK,
    ICON_SCAN,
    render_circular_metric, render_large_health_score, get_daily_tip,
    render_privacy_notice, render_chat_widget,
)
import datetime
import io

from pages.summary import estimate_skin_type

# ReportLab imports
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT



# SVG icons for section headers in report
ICON_AI = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>'
ICON_CART = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>'
ICON_SUNRISE = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 18a5 5 0 0 0-10 0"/><line x1="12" y1="2" x2="12" y2="9"/><line x1="4.22" y1="10.22" x2="5.64" y2="11.64"/><line x1="1" y1="18" x2="3" y2="18"/><line x1="21" y1="18" x2="23" y2="18"/><line x1="18.36" y1="11.64" x2="19.78" y2="10.22"/></svg>'
ICON_MOON = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
ICON_DOWNLOAD2 = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'
ICON_PLUS2 = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>'

# ─── PDF Generator ────────────────────────────────────────────
def generate_pdf(report_data, date_str, time_str) -> io.BytesIO:
    """Builds a complete DermaLens AI skin report PDF using ReportLab.
    Returns a BytesIO buffer ready for st.download_button."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="DermaLens AI Skin Report",
        author="DermaLens AI",
    )

    # ── Styles ──────────────────────────────────────────────────
    base = getSampleStyleSheet()
    navy  = colors.HexColor("#0A1628")
    blue  = colors.HexColor("#4D9FFF")
    teal  = colors.HexColor("#06B6D4")
    green = colors.HexColor("#22C55E")
    red   = colors.HexColor("#EF4444")
    grey  = colors.HexColor("#4A5568")
    light = colors.HexColor("#8A9BB5")

    title_style = ParagraphStyle(
        "DLTitle", parent=base["Title"],
        fontSize=26, textColor=navy, spaceAfter=4,
        fontName="Helvetica-Bold", alignment=TA_CENTER,
    )
    subtitle_style = ParagraphStyle(
        "DLSubtitle", parent=base["Normal"],
        fontSize=11, textColor=blue, spaceAfter=2,
        fontName="Helvetica-Bold", alignment=TA_CENTER,
    )
    meta_style = ParagraphStyle(
        "DLMeta", parent=base["Normal"],
        fontSize=9, textColor=light, spaceAfter=16,
        fontName="Helvetica", alignment=TA_CENTER,
    )
    section_style = ParagraphStyle(
        "DLSection", parent=base["Normal"],
        fontSize=13, textColor=navy, spaceBefore=14, spaceAfter=6,
        fontName="Helvetica-Bold", borderPad=2,
    )
    body_style = ParagraphStyle(
        "DLBody", parent=base["Normal"],
        fontSize=10, textColor=grey, spaceAfter=4,
        fontName="Helvetica", leading=15,
    )
    bullet_style = ParagraphStyle(
        "DLBullet", parent=base["Normal"],
        fontSize=10, textColor=grey, spaceAfter=3,
        fontName="Helvetica", leftIndent=16, leading=14,
    )
    label_style = ParagraphStyle(
        "DLLabel", parent=base["Normal"],
        fontSize=9, textColor=light, spaceAfter=0,
        fontName="Helvetica-Bold", leading=12,
    )
    value_style = ParagraphStyle(
        "DLValue", parent=base["Normal"],
        fontSize=11, textColor=navy, spaceAfter=6,
        fontName="Helvetica-Bold", leading=14,
    )

    def hr():
        return HRFlowable(width="100%", thickness=0.5,
                         color=colors.HexColor("#E2E8F0"),
                         spaceAfter=10, spaceBefore=10)

    def section(text):
        return Paragraph(text, section_style)

    def body(text):
        return Paragraph(text, body_style)

    def bullet(text):
        return Paragraph(f"\u2022  {text}", bullet_style)

    # ── Build story ─────────────────────────────────────────────
    story = []

    # Header
    story.append(Paragraph("DermaLens AI", title_style))
    story.append(Paragraph("AI Skin Analysis Report", subtitle_style))
    story.append(Paragraph(f"Scan Date: {date_str} &nbsp;·&nbsp; {time_str}", meta_style))
    story.append(hr())

    # ── Summary metrics table ───────────────────────────────────
    story.append(section("Skin Health Overview"))
    metrics = [
        ["Metric", "Result"],
        ["Skin Health Score",  f"{report_data['skin_health']}/100"],
        ["Skin Type",          report_data["skin_type"]],
        ["Primary Skin Concern", report_data["concern"]],
        ["Confidence",         f"{report_data['confidence']:.0f}%"],
        ["Hydration",         f"{report_data['hydration']}%"],
        ["Oil Balance",       f"{report_data['oil_balance']}%"],
        ["Barrier Health",    f"{report_data['barrier_health']}%"],
        ["Sensitivity",       report_data["sensitivity"]],
    ]
    tbl = Table(metrics, colWidths=[6*cm, 10*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  colors.HexColor("#0A1628")),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0),  10),
        ("FONTNAME",    (0, 1), (0, -1),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 1), (-1, -1), 10),
        ("TEXTCOLOR",   (0, 1), (0, -1),  colors.HexColor("#4A5568")),
        ("TEXTCOLOR",   (1, 1), (1, -1),  colors.HexColor("#0A1628")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
            [colors.HexColor("#F8FAFC"), colors.white]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING",   (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 0), (-1, 0),
            [colors.HexColor("#0A1628")]),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.4*cm))
    story.append(hr())

    # ── Clinical AI Summary ─────────────────────────────────────
    story.append(section("Clinical AI Summary"))
    story.append(body(
    f"""
    The uploaded image indicates <b>{report_data['concern']}</b>.
    The AI prediction confidence is <b>{report_data['confidence']:.1f}%</b>.
    This report provides personalized skincare recommendations based on the detected skin concern.
    """
))
    story.append(hr())

    # ── Morning Routine ─────────────────────────────────────────
    story.append(section("Morning Routine"))
    for i, step in enumerate(report_data["morning_routine"], 1):
        story.append(body(f"<b>{i}. {step['step']}</b> \u2014 {step['description']}"))
    story.append(hr())

    # ── Night Routine ───────────────────────────────────────────
    story.append(section("Night Routine"))
    for i, step in enumerate(report_data["night_routine"], 1):
        story.append(body(f"<b>{i}. {step['step']}</b> \u2014 {step['description']}"))
    story.append(hr())

    # ── Recommended Ingredients ─────────────────────────────────
    story.append(section("Recommended Ingredients"))
    for ing in report_data["recommendations"]:
        story.append(body(
            f"<b>{ing['name']}</b> ({ing['usage']} \u00b7 {ing['frequency']})"
        ))
        story.append(bullet(ing["benefits"]))
    story.append(hr())

    # ── Ingredients to Avoid ────────────────────────────────────
    story.append(section("Ingredients to Avoid"))
    for ing in report_data["avoid"]:
        story.append(body(f"<b>{ing['name']}</b> ({ing['type']})"))
        story.append(bullet(ing["benefits"]))
    story.append(hr())

    # Footer
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "Generated by DermaLens AI \u00b7 For informational purposes only. "
        "Not a substitute for professional medical advice.",
        ParagraphStyle("footer", parent=base["Normal"],
                       fontSize=8, textColor=light, alignment=TA_CENTER)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer


def render_report_screen():
    """Renders the comprehensive, interactive AI Skin Report (Screen 7)."""

    # Run AI only once per uploaded image
    if "analysis_result" not in st.session_state or st.session_state.analysis_result is None:

        if st.session_state.uploaded_image is None:
            st.error("No image uploaded.")
            return

        with st.spinner("Running AI analysis..."):
            st.session_state.analysis_result = analyze_skin(
                st.session_state.uploaded_image
            )
#  -----
    result = st.session_state.analysis_result

    condition = result.get("condition", "Unknown")
    confidence = result.get("confidence", 0)
    predictions = result.get("all_predictions", [])

    answers = st.session_state.get("answers", [])
    skin_type = estimate_skin_type(answers) if answers else "Unknown"

    # Temporary values until we implement medical scoring
    health_score = min(100, max(65, int(100 - confidence/2)))

    if condition == "Healthy":
        hydration = 90
        oil_balance = 88
        barrier_health = 92
        sensitivity = "Low"

    elif condition == "Acne":
        hydration = 70
        oil_balance = 45
        barrier_health = 68
        sensitivity = "High"

    elif condition == "Pigmentation":
        hydration = 82
        oil_balance = 80
        barrier_health = 85
        sensitivity = "Medium"

    elif condition == "Wrinkles":
        hydration = 62
        oil_balance = 78
        barrier_health = 72
        sensitivity = "Medium"

    else:
        hydration = 75
        oil_balance = 75
        barrier_health = 75
        sensitivity = "Unknown"

    if condition == "Acne":

        morning_routine = [
            {
                "step": "Salicylic Acid Cleanser",
                "description": "Remove excess oil and unclog pores."
            },
            {
                "step": "Niacinamide Serum",
                "description": "Reduce inflammation and regulate sebum."
            },
            {
                "step": "Oil-Free SPF 50",
                "description": "Protect acne-prone skin from UV damage."
            }
        ]

        night_routine = [
            {
                "step": "Gentle Cleanser",
                "description": "Wash away dirt and excess oil."
            },
            {
                "step": "Benzoyl Peroxide / Adapalene",
                "description": "Treat active acne lesions."
            },
            {
                "step": "Lightweight Moisturizer",
                "description": "Maintain hydration without clogging pores."
            }
        ]

        recommendations = [
            {
                "name": "Salicylic Acid",
                "usage": "AM/PM",
                "benefits": "Unclogs pores and reduces acne.",
                "frequency": "Daily"
            },
            {
                "name": "Niacinamide",
                "usage": "AM",
                "benefits": "Controls excess oil and calms redness.",
                "frequency": "Daily"
            },
            {
                "name": "Ceramides",
                "usage": "PM",
                "benefits": "Repairs the skin barrier.",
                "frequency": "Daily"
            }
        ]

        avoid = [
            {
                "name": "Heavy Oils",
                "type": "Avoid",
                "benefits": "Can clog pores and worsen acne."
            },
            {
                "name": "Over-scrubbing",
                "type": "Avoid",
                "benefits": "Irritates inflamed skin."
            },
            {
                "name": "Picking Pimples",
                "type": "Avoid",
                "benefits": "May cause scarring and infection."
            }
        ]

    elif condition == "Pigmentation":

        morning_routine = [
            {
                "step": "Gentle Cleanser",
                "description": "Clean skin without irritation."
            },
            {
                "step": "Vitamin C Serum",
                "description": "Brighten skin and reduce pigmentation."
            },
            {
                "step": "Broad Spectrum SPF 50",
                "description": "Prevent pigmentation from worsening."
            }
        ]

        night_routine = [
            {
                "step": "Gentle Cleanser",
                "description": "Remove impurities."
            },
            {
                "step": "Azelaic Acid / Alpha Arbutin",
                "description": "Fade dark spots gradually."
            },
            {
                "step": "Moisturizer",
                "description": "Support skin repair overnight."
            }
        ]

        recommendations = [
            {
                "name": "Vitamin C",
                "usage": "AM",
                "benefits": "Brightens skin and reduces pigmentation.",
                "frequency": "Daily"
            },
            {
                "name": "Alpha Arbutin",
                "usage": "PM",
                "benefits": "Fades dark spots.",
                "frequency": "Daily"
            },
            {
                "name": "Azelaic Acid",
                "usage": "PM",
                "benefits": "Improves uneven skin tone.",
                "frequency": "3–4x/week"
            }
        ]

        avoid = [
            {
                "name": "Skipping Sunscreen",
                "type": "Avoid",
                "benefits": "UV exposure worsens pigmentation."
            },
            {
                "name": "Harsh Exfoliation",
                "type": "Avoid",
                "benefits": "May increase skin irritation."
            }
        ]

    elif condition == "Wrinkles":

        morning_routine = [
            {
                "step": "Hydrating Cleanser",
                "description": "Clean without drying the skin."
            },
            {
                "step": "Vitamin C Serum",
                "description": "Fight free radicals."
            },
            {
                "step": "SPF 50",
                "description": "Reduce photoaging."
            }
        ]

        night_routine = [
            {
                "step": "Gentle Cleanser",
                "description": "Clean skin before treatment."
            },
            {
                "step": "Retinol Serum",
                "description": "Stimulate collagen production."
            },
            {
                "step": "Ceramide Moisturizer",
                "description": "Repair the skin barrier overnight."
            }
        ]

        recommendations = [
            {
                "name": "Retinol",
                "usage": "PM",
                "benefits": "Boosts collagen production.",
                "frequency": "3x/week"
            },
            {
                "name": "Peptides",
                "usage": "AM/PM",
                "benefits": "Improves skin elasticity.",
                "frequency": "Daily"
            },
            {
                "name": "Ceramides",
                "usage": "PM",
                "benefits": "Repairs the skin barrier.",
                "frequency": "Daily"
            }
        ]

        avoid = [
            {
                "name": "Smoking",
                "type": "Avoid",
                "benefits": "Accelerates collagen breakdown."
            },
            {
                "name": "Excess Sun Exposure",
                "type": "Avoid",
                "benefits": "Causes premature skin aging."
            }
        ]

    else:

        morning_routine = [
            {
                "step": "Gentle Cleanser",
                "description": "Maintain healthy skin."
            },
            {
                "step": "Light Moisturizer",
                "description": "Keep skin hydrated."
            },
            {
                "step": "SPF 50",
                "description": "Daily UV protection."
            }
        ]

        night_routine = [
            {
                "step": "Gentle Cleanser",
                "description": "Clean before bed."
            },
            {
                "step": "Hydrating Serum",
                "description": "Maintain moisture balance."
            },
            {
                "step": "Moisturizer",
                "description": "Support overnight repair."
            }
        ]

        recommendations = [
            {
                "name": "Hyaluronic Acid",
                "usage": "AM/PM",
                "benefits": "Provides long-lasting hydration.",
                "frequency": "Daily"
            },
            {
                "name": "Ceramides",
                "usage": "PM",
                "benefits": "Maintains a healthy skin barrier.",
                "frequency": "Daily"
            },
            {
                "name": "Vitamin C",
                "usage": "AM",
                "benefits": "Protects against environmental damage.",
                "frequency": "Daily"
            }
        ]

        avoid = [
            {
                "name": "Skipping Sunscreen",
                "type": "Avoid",
                "benefits": "Increases long-term skin damage."
            },
            {
                "name": "Over-cleansing",
                "type": "Avoid",
                "benefits": "Can weaken the skin barrier."
            }
        ]
    report_data = {
        "skin_health": health_score,
        "skin_type": skin_type,
        "concern": condition,
        "confidence": confidence,
        "hydration": hydration,
        "oil_balance": oil_balance,
        "barrier_health": barrier_health,
        "sensitivity": sensitivity,
        "morning_routine": morning_routine,

        "night_routine": night_routine,

        "recommendations": recommendations,

        "avoid": avoid
    }
    if condition == "Acne":
        clinical_summary = f"""
        The uploaded image indicates signs of <strong>Acne</strong> with an AI confidence of <strong>{confidence:.1f}%</strong>.
        The analysis suggests acne-prone skin that may benefit from gentle cleansing, oil control, and non-comedogenic skincare.
        Consistent use of ingredients like Niacinamide and Salicylic Acid may help improve skin condition over time.
        """

    elif condition == "Pigmentation":
        clinical_summary = f"""
        The uploaded image indicates <strong>Pigmentation</strong> with an AI confidence of <strong>{confidence:.1f}%</strong>.
        Uneven skin tone and localized dark spots appear to be the primary concern.
        Daily sunscreen and brightening ingredients such as Vitamin C and Niacinamide are recommended.
        """

    elif condition == "Wrinkles":
        clinical_summary = f"""
        The uploaded image indicates visible <strong>Wrinkles</strong> with an AI confidence of <strong>{confidence:.1f}%</strong>.
        The analysis suggests early or moderate signs of skin aging.
        Maintaining hydration, daily SPF protection, and retinol-based nighttime care may improve skin texture.
        """

    else:
        clinical_summary = f"""
        The uploaded image indicates <strong>Healthy Skin</strong> with an AI confidence of <strong>{confidence:.1f}%</strong>.
        No major visible skin concerns were detected.
        Continue maintaining a balanced skincare routine and consistent sun protection.
        """
    print("Analysis Result:")
    print(report_data)
    print(type(report_data))
#   ----
    # 1. Log to history ONCE per scan
    if "history_logged" not in st.session_state:
        st.session_state.history_logged = False

    current_time = datetime.datetime.now()
    date_str = current_time.strftime("%B %d, %Y")
    time_str = current_time.strftime("%I:%M %p")

    if not st.session_state.history_logged:
        add_to_history(
            date_str,
            93,          # Temporary health score
            condition,
            skin_type
        )
        st.session_state.history_logged = True

    # ── Report Header bar ─────────────────────────────────────
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;
                margin-bottom:1.5rem;padding:1.25rem 1.75rem;
                background:linear-gradient(135deg,#0D1F3C 0%,#112040 100%);
                border-radius:20px;border:1px solid rgba(77,159,255,0.15);
                box-shadow:0 8px 24px rgba(10,22,40,0.18);">
        <div>
            <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.1em;color:#06B6D4;margin-bottom:0.35rem;
                        font-family:'Inter',sans-serif;">AI Skin Report</div>
            <div style="font-size:1.5rem;font-weight:800;color:#FFFFFF;letter-spacing:-0.03em;
                        font-family:'Inter',sans-serif;line-height:1.2;">
                Dermal Assessment Results
            </div>
            <div style="font-size:0.8rem;color:rgba(255,255,255,0.5);margin-top:0.3rem;
                        font-family:'Inter',sans-serif;">
                {date_str} &nbsp;·&nbsp; {time_str}
            </div>
        </div>
        <div style="text-align:right;">
            <div style="display:inline-flex;align-items:center;gap:0.5rem;
                        background:rgba(34,197,94,0.15);border:1px solid rgba(34,197,94,0.3);
                        border-radius:50px;padding:0.35rem 0.85rem;">
                <span style="width:7px;height:7px;border-radius:50%;background:#22C55E;"></span>
                <span style="font-size:0.75rem;font-weight:700;color:#22C55E;
                             font-family:'Inter',sans-serif;">Analysis Complete</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.5])

    # ═══ LEFT COLUMN ════════════════════════════════════════════
    with col_left:
        with st.container():


            st.markdown("""
            <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;
                        color:#4D9FFF;margin-bottom:1rem;font-family:'Inter',sans-serif;">
                Dermal Assessment
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<p style='text-align:center;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#8A9BB5;margin-bottom:0;font-family:\"Inter\",sans-serif;'>Overall Skin Health Score</p>", unsafe_allow_html=True)
            st.markdown(render_large_health_score(report_data["skin_health"]), unsafe_allow_html=True)

            # Stat pills
            st.markdown(f"""
            <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:0.4rem;margin-bottom:1.5rem;">
                <span class="stat-pill">{report_data['skin_type']} Skin</span>
                <span class="stat-pill">{report_data['concern']}</span>
                <span class="stat-pill">{report_data['confidence']:.0f}% Confidence</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)

            # Face Visualization

            # Skin Goals
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.5rem;font-size:0.88rem;font-weight:700;color:#0A1628;
                        margin-bottom:1rem;font-family:'Inter',sans-serif;">
                {ICON_TARGET} Skin Goal Milestones
            </div>
            """, unsafe_allow_html=True)

            goals = [
                ("Pore Tightening Progress", 0.65, "65%"),
                ("Sebum Balance Control", 0.80, "80%"),
                ("Hydration Restoration", 0.72, "72%"),
            ]
            for g_label, g_val, g_pct in goals:
                st.markdown(f"""
                <div class="goal-row">
                    <div class="goal-label-row">
                        <span class="goal-label">{g_label}</span>
                        <span class="goal-pct">{g_pct}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(g_val)

            st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)

            # Daily tip
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.5rem;font-size:0.88rem;font-weight:700;color:#0A1628;
                        margin-bottom:0.5rem;font-family:'Inter',sans-serif;">
                {ICON_TIP} Daily Skin Tip
            </div>
            <div class="tip-card">
                <p style="color:#4A5568;font-size:0.85rem;line-height:1.65;margin:0;font-family:'Inter',sans-serif;
                          font-style:italic;padding-left:0.5rem;">
                    {get_daily_tip()}
                </p>
            </div>
            """, unsafe_allow_html=True)

            render_privacy_notice()
            #avoid
            st.markdown("""
            <div style="display:flex;align-items:center;gap:0.5rem;font-size:0.78rem;font-weight:700;color:#EF4444;
                        text-transform:uppercase;letter-spacing:0.06em;font-family:'Inter',sans-serif;margin:1.25rem 0 0.65rem;">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#EF4444" stroke-width="2.5"
                     stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
                </svg>
                Ingredients to Avoid
            </div>
            """, unsafe_allow_html=True)
            for ing in report_data["avoid"]:
                st.markdown(f"""
                <div class="ingredient-card ingredient-card-avoid">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                        <span style="font-weight:800;color:#EF4444;font-size:0.95rem;font-family:'Inter',sans-serif;">{ing['name']}</span>
                        <span style="font-size:0.72rem;font-weight:700;background:rgba(245,158,11,0.1);
                                     color:#D97706;padding:0.2rem 0.65rem;border-radius:50px;
                                     font-family:'Inter',sans-serif;border:1px solid rgba(245,158,11,0.2);">
                            {ing['type']}
                        </span>
                    </div>
                    <div style="font-size:0.82rem;color:#4A5568;font-family:'Inter',sans-serif;">
                        {ing['benefits']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)


    # ═══ RIGHT COLUMN ════════════════════════════════════════════
    with col_right:
        with st.container():
            # result = st.session_state.get("analysis_result", {})
            # condition = result.get("condition", "Unknown")
            # confidence = result.get("confidence", 0)
            # predictions = result.get("all_predictions", [])
            # answers = st.session_state.get("answers", [])
            # skin_type = estimate_skin_type(answers) if answers else "Unknown"

            st.markdown("""
            <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;
                        color:#4D9FFF;margin-bottom:1rem;font-family:'Inter',sans-serif;">
                Bio-Metric Status
            </div>
            """, unsafe_allow_html=True)

            # Summary 4 mini cards
            sum_1, sum_2, sum_3, sum_4 = st.columns(4)
            cards = [
                (sum_1, "Score", "93/100", "#4D9FFF"),
                (sum_2, "Concern", condition, "#EF4444"),
                (sum_3, "Confidence", f"{confidence:.1f}%", "#22C55E"),
                (sum_4, "Type", skin_type, "#0A1628"),
            ]


            for col, label, value, color in cards:
                with col:
                    st.markdown(f"""
                    <div class="mini-card">
                        <div style="font-size:0.65rem;color:#8A9BB5;text-transform:uppercase;font-weight:700;
                                    font-family:'Inter',sans-serif;letter-spacing:0.07em;margin-bottom:0.3rem;">{label}</div>
                        <div style="font-size:1.1rem;font-weight:800;color:{color};font-family:'Inter',sans-serif;
                                    letter-spacing:-0.02em;line-height:1.2;">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.write("")

            # Circular gauges
            met_col1, met_col2, met_col3, met_col4 = st.columns(4)
            with met_col1:
                st.markdown(render_circular_metric("Hydration",   f"{report_data['hydration']}%",      report_data['hydration'],     color="#4D9FFF"), unsafe_allow_html=True)
            with met_col2:
                st.markdown(render_circular_metric("Oil Balance", f"{report_data['oil_balance']}%",    report_data['oil_balance'],   color="#06B6D4"), unsafe_allow_html=True)
            with met_col3:
                st.markdown(render_circular_metric("Barrier",     f"{report_data['barrier_health']}%", report_data['barrier_health'],color="#22C55E"), unsafe_allow_html=True)
            with met_col4:
                st.markdown(f"""
                <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;margin:0.5rem;position:relative;">
                    <div class="sensitivity-badge">
                        <span style="font-size:0.82rem;font-weight:800;color:#B45309;font-family:'Inter',sans-serif;">{report_data['sensitivity']}</span>
                    </div>
                    <span style="font-size:0.7rem;text-transform:uppercase;font-weight:700;color:#8A9BB5;
                                 margin-top:0.5rem;letter-spacing:0.08em;font-family:'Inter',sans-serif;">Sensitivity</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)

            # Clinical AI Summary
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(77,159,255,0.07),rgba(6,182,212,0.04));
                        border:1.5px solid rgba(77,159,255,0.15);border-radius:16px;
                        padding:1.25rem 1.5rem;margin-bottom:1.75rem;">
                <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.6rem;">
                    {ICON_AI}
                    <span style="font-size:0.88rem;font-weight:700;color:#0A1628;font-family:'Inter',sans-serif;">
                        Clinical AI Summary
                    </span>
                </div>
                    <p style="color:#4A5568;font-size:0.87rem;line-height:1.65;margin:0;font-family:'Inter',sans-serif;">
                        {clinical_summary}



            """, unsafe_allow_html=True)

            # Skincare Regimen tabs
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.5rem;font-size:0.88rem;font-weight:700;color:#0A1628;
                        margin-bottom:1rem;font-family:'Inter',sans-serif;">
                {ICON_SCAN} Skincare Regimen
            </div>
            """, unsafe_allow_html=True)

            tab_morning, tab_night = st.tabs(["Morning Regimen", "Night Regimen"])

            with tab_morning:
                st.write("")
                for idx, r_step in enumerate(report_data["morning_routine"]):
                    st.markdown(f"""
                    <div class="timeline-item">
                        <div class="timeline-num">{idx + 1}</div>
                        <div>
                            <div class="timeline-text">{r_step['step']}</div>
                            <div style="font-size:0.78rem;color:#8A9BB5;font-family:'Inter',sans-serif;margin-top:0.15rem;">{r_step['description']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            with tab_night:
                st.write("")
                for idx, r_step in enumerate(report_data["night_routine"]):
                    st.markdown(f"""
                    <div class="timeline-item" style="border-left-color:#06B6D4;">
                        <div class="timeline-num" style="background:linear-gradient(135deg,#06B6D4,#0891B2);">{idx + 1}</div>
                        <div>
                            <div class="timeline-text">{r_step['step']}</div>
                            <div style="font-size:0.78rem;color:#8A9BB5;font-family:'Inter',sans-serif;margin-top:0.15rem;">{r_step['description']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)

            # Recommended Ingredients
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.5rem;font-size:0.88rem;font-weight:700;color:#0A1628;
                        margin-bottom:1rem;font-family:'Inter',sans-serif;">
                {ICON_FLASK} Active Ingredients Formulation
            </div>
            <div style="display:flex;align-items:center;gap:0.5rem;font-size:0.78rem;font-weight:700;color:#22C55E;
                        text-transform:uppercase;letter-spacing:0.06em;font-family:'Inter',sans-serif;margin-bottom:0.65rem;">
                {ICON_CHECK} Recommended Actives
            </div>
            """, unsafe_allow_html=True)
            for ing in report_data["recommendations"]:
                st.markdown(f"""
                <div class="ingredient-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                        <span style="font-weight:800;color:#0A1628;font-size:0.95rem;font-family:'Inter',sans-serif;">{ing['name']}</span>
                        <span style="font-size:0.72rem;font-weight:700;background:rgba(77,159,255,0.12);
                                     color:#4D9FFF;padding:0.2rem 0.65rem;border-radius:50px;
                                     font-family:'Inter',sans-serif;border:1px solid rgba(77,159,255,0.2);">
                            {ing['usage']}
                        </span>
                    </div>
                    <div style="font-size:0.82rem;color:#4A5568;font-family:'Inter',sans-serif;margin-bottom:0.2rem;">
                        <strong style="color:#0A1628;">Benefit:</strong> {ing['benefits']}
                    </div>
                    <div style="font-size:0.78rem;color:#8A9BB5;font-family:'Inter',sans-serif;">
                        <strong style="color:#4A5568;">Frequency:</strong> {ing['frequency']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Ingredients to avoid

            # OTC Products
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.5rem;font-size:0.88rem;font-weight:700;color:#0A1628;
                        margin-bottom:0.5rem;font-family:'Inter',sans-serif;">
                {ICON_CART} Suggested OTC Skin Products
            </div>
            <p style="color:#8A9BB5;font-size:0.8rem;margin-bottom:1rem;font-family:'Inter',sans-serif;">
                Neutral, clinically formulated products matched to your regimen requirements.
            </p>
            """, unsafe_allow_html=True)

            prod_col1, prod_col2 = st.columns(2)
            products = [
                (prod_col1, "Cleanser",     "CeraVe Foaming Facial Cleanser",        "Contains Ceramides, Hyaluronic Acid, and Niacinamide for gentle cleansing."),
                (prod_col2, "Active Serum", "The Ordinary Niacinamide 10% + Zinc 1%","Balances oil production and visibly minimises the appearance of pores."),
            ]
            for col, category, name, desc in products:
                with col:
                    st.markdown(f"""
                    <div class="product-card">
                        <div style="font-size:0.7rem;color:#4D9FFF;font-weight:700;text-transform:uppercase;
                                    letter-spacing:0.08em;font-family:'Inter',sans-serif;margin-bottom:0.35rem;">
                            {category}
                        </div>
                        <div style="font-size:0.88rem;font-weight:800;color:#0A1628;font-family:'Inter',sans-serif;
                                    margin-bottom:0.4rem;letter-spacing:-0.01em;line-height:1.3;">
                            {name}
                        </div>
                        <p style="color:#8A9BB5;font-size:0.78rem;margin:0;font-family:'Inter',sans-serif;line-height:1.45;">
                            {desc}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)

            # Scan History expander
            with st.expander("Scan Consultation History"):
                if len(st.session_state.scan_history) <= 1:
                    st.markdown("<p style='color:#8A9BB5;font-size:0.85rem;font-family:\"Inter\",sans-serif;padding:0.5rem 0;'>No previous scans recorded. This is your first skin analysis.</p>", unsafe_allow_html=True)
                else:
                    for past in reversed(st.session_state.scan_history[:-1]):
                        st.markdown(f"""
                        <div style="display:flex;justify-content:space-between;align-items:center;
                                    padding:0.75rem 1rem;background:rgba(240,244,250,0.8);border-radius:12px;
                                    margin-bottom:0.5rem;border:1px solid rgba(77,159,255,0.08);">
                            <div>
                                <strong style="font-size:0.85rem;color:#0A1628;font-family:'Inter',sans-serif;">{past['date']}</strong>
                                <div style="font-size:0.75rem;color:#8A9BB5;font-family:'Inter',sans-serif;margin-top:0.15rem;">
                                    {past['concern']} · {past['skin_type']}
                                </div>
                            </div>
                            <span style="font-weight:800;color:#4D9FFF;font-size:0.9rem;font-family:'Inter',sans-serif;">
                                {past['score']}/100
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)

            render_chat_widget()

            st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)

            # Action buttons
            col_act_left, col_act_right = st.columns(2)
            with col_act_left:
                pdf_buffer = generate_pdf(
    report_data,
    date_str,
    time_str
)
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_buffer.getvalue(),
                    file_name="DermaLens_AI_Skin_Report.pdf",
                    mime="application/pdf",
                    type="secondary",
                    key="download_report_btn"
                )
            with col_act_right:
                if st.button("New Analysis", type="primary", key="new_analysis_btn"):
                    from utils.state import reset_scan
                    reset_scan()
                    st.rerun()
