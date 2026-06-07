# app.py — AI Maturity Compass
# Full application with context layer, consistency flags, self-perception gap

import streamlit as st
import plotly.graph_objects as go
from questions import QUESTIONS, DIMENSIONS, DIMENSION_SUBTITLES, DIMENSION_ICONS, MATURITY_LEVELS
from assessor import compute_scores, get_score_label, compute_self_perception_gap
from report_generator import generate_report, SECTOR_BENCHMARKS
from context_questions import CONTEXT_QUESTIONS, BARRIER_DIMENSION_MAP

st.set_page_config(
    page_title="AI Maturity Compass | GCC Energy",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
        background-color: #F5F7FA;
        color: #0D1B2A;
    }
    .stApp { background: #F5F7FA; }

    .hero-container {
        background: linear-gradient(135deg, #003366 0%, #004080 60%, #005599 100%);
        border-radius: 16px;
        padding: 52px 60px;
        margin-bottom: 36px;
        position: relative;
        overflow: hidden;
    }
    .hero-container::after {
        content: '🧭';
        position: absolute;
        right: 60px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 96px;
        opacity: 0.12;
    }
    .hero-tag {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.3);
        color: #A8D5FF;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        padding: 6px 14px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    .hero-title { font-size: 44px; font-weight: 700; color: #FFF; line-height: 1.15; margin: 0 0 16px 0; }
    .hero-title span { color: #4FC3F7; }
    .hero-subtitle { font-size: 16px; color: rgba(255,255,255,0.75); line-height: 1.7; max-width: 600px; margin: 0 0 20px 0; }
    .methodology-note { font-size: 12px; color: rgba(255,255,255,0.45); font-style: italic; border-left: 2px solid rgba(79,195,247,0.5); padding-left: 12px; }

    .section-header { font-size: 22px; font-weight: 700; color: #003366; margin: 36px 0 6px 0; }
    .section-sub { font-size: 14px; color: #6B7280; margin-bottom: 24px; }

    .card {
        background: #FFFFFF;
        border: 1px solid #E5E9F0;
        border-radius: 12px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 1px 4px rgba(0,51,102,0.05);
    }
    .card-accent { border-left: 4px solid #003366; }
    .card-warning { border-left: 4px solid #F59E0B; background: #FFFBEB; }
    .card-success { border-left: 4px solid #22C55E; background: #F0FDF4; }
    .card-danger  { border-left: 4px solid #EF4444; background: #FEF2F2; }

    .context-header {
        font-size: 13px; font-weight: 600; color: #003366;
        letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 16px;
    }
    .help-text { font-size: 12px; color: #9CA3AF; font-style: italic; margin-bottom: 10px; }

    .dim-number { font-size: 11px; font-weight: 600; color: #4FC3F7; letter-spacing: 2px; text-transform: uppercase; }
    .dim-title { font-size: 18px; font-weight: 700; color: #003366; margin: 4px 0; }
    .dim-subtitle { font-size: 13px; color: #6B7280; font-style: italic; margin-bottom: 18px; padding-bottom: 16px; border-bottom: 1px solid #F0F2F5; }
    .q-type-badge {
        display: inline-block; background: #EEF4FF; color: #003366;
        font-size: 10px; font-weight: 600; letter-spacing: 1.5px;
        text-transform: uppercase; padding: 3px 8px; border-radius: 3px; margin-bottom: 5px;
    }
    .q-text { font-size: 14px; font-weight: 500; color: #1A2B3C; line-height: 1.55; margin-bottom: 10px; }

    .score-card {
        background: linear-gradient(135deg, #003366, #004A8F);
        border-radius: 16px; padding: 36px 32px; text-align: center;
        box-shadow: 0 4px 20px rgba(0,51,102,0.25);
    }
    .score-number { font-size: 72px; font-weight: 700; line-height: 1; font-family: 'IBM Plex Mono', monospace; }
    .score-denom { font-size: 28px; color: rgba(255,255,255,0.35); }
    .maturity-label { font-size: 22px; font-weight: 700; margin: 14px 0 4px 0; }
    .gartner-equiv { font-size: 11px; color: rgba(255,255,255,0.4); letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 16px; }
    .maturity-desc { font-size: 13px; color: rgba(255,255,255,0.7); line-height: 1.65; text-align: left; }

    .flag-card {
        background: #FFFBEB; border: 1px solid #FCD34D;
        border-left: 4px solid #F59E0B;
        border-radius: 8px; padding: 14px 18px; margin-bottom: 10px;
    }
    .flag-title { font-size: 12px; font-weight: 700; color: #92400E; margin-bottom: 4px; }
    .flag-text { font-size: 12px; color: #78350F; line-height: 1.5; }

    .perception-card {
        border-radius: 10px; padding: 16px 20px; margin-top: 16px;
    }
    .perception-over { background: #FEF2F2; border: 1px solid #FCA5A5; border-left: 4px solid #EF4444; }
    .perception-under { background: #F0FDF4; border: 1px solid #86EFAC; border-left: 4px solid #22C55E; }
    .perception-aligned { background: #EFF6FF; border: 1px solid #93C5FD; border-left: 4px solid #3B82F6; }

    .benchmark-pill {
        display: inline-block; padding: 6px 14px; border-radius: 20px;
        font-size: 12px; font-weight: 600; margin: 4px;
    }

    .progress-bar-bg { background: #EEF0F5; border-radius: 4px; height: 7px; width: 100%; margin-top: 5px; }
    .progress-bar-fill { height: 7px; border-radius: 4px; }

    .report-wrapper {
        background: #FFFFFF; border: 1px solid #E5E9F0;
        border-top: 4px solid #003366; border-radius: 12px;
        padding: 40px 48px; margin-top: 24px;
        box-shadow: 0 2px 12px rgba(0,51,102,0.08);
        color: #0D1B2A; line-height: 1.75;
    }
    .report-wrapper h2 { font-size: 20px; font-weight: 700; color: #003366; margin-top: 32px; margin-bottom: 10px; padding-bottom: 8px; border-bottom: 2px solid #EEF4FF; }
    .report-wrapper h3 { font-size: 16px; font-weight: 600; color: #003366; margin-top: 22px; margin-bottom: 6px; }
    .report-wrapper p { font-size: 15px; color: #1A2B3C; margin-bottom: 14px; }
    .report-wrapper strong { color: #003366; }
    .report-wrapper ul, .report-wrapper ol { padding-left: 20px; margin-bottom: 14px; }
    .report-wrapper li { font-size: 15px; color: #1A2B3C; margin-bottom: 6px; }
    .report-wrapper hr { border: none; border-top: 1px solid #EEF0F5; margin: 24px 0; }
    .report-wrapper em { font-size: 12px; color: #9CA3AF; }

    .stButton > button {
        background: linear-gradient(135deg, #003366, #0055A4);
        color: white; border: none; border-radius: 8px;
        font-family: 'IBM Plex Sans', sans-serif; font-weight: 600;
        font-size: 15px; padding: 14px 36px; width: 100%;
        transition: opacity 0.2s; box-shadow: 0 2px 8px rgba(0,51,102,0.3);
    }
    .stButton > button:hover { opacity: 0.88; }
    .stButton > button:disabled { background: #D1D5DB; color: #9CA3AF; box-shadow: none; }

    .stRadio > label { display: none; }
    .stTextInput input { border: 1px solid #E5E9F0 !important; border-radius: 8px !important; background: #FFF !important; color: #0D1B2A !important; }
    .stSelectbox > div > div { border: 1px solid #E5E9F0 !important; border-radius: 8px !important; background: #FFF !important; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
defaults = {
    "responses": {}, "context_responses": {}, "results": None,
    "report_text": None, "show_results": False,
    "org_name": "", "org_sector": "Power Generation", "org_country": "Saudi Arabia",
    "self_perception_gap": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── HERO ──
st.markdown("""
<div class="hero-container">
    <div class="hero-tag">GCC Energy &nbsp;·&nbsp; AI Advisory</div>
    <div class="hero-title">AI Maturity <span>Compass</span></div>
    <div class="hero-subtitle">
        25 questions. 5 dimensions. One consulting-grade report with a sector-specific,
        context-calibrated 90-day roadmap — built for GCC energy operators navigating
        the gap between AI ambition and operational value.
    </div>
    <div class="methodology-note">
        Grounded in Gartner's AI Maturity Model (7 pillars), consolidated into 5 dimensions
        calibrated for GCC energy execution reality. Benchmarks derived from public GCC energy
        AI disclosures — stated as indicative, not proprietary survey data.
    </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# RESULTS VIEW
# ════════════════════════════════════════════
def show_results_view(results):
    dim_scores = results["dimension_scores"]
    overall = results["overall_score"]
    maturity = results["maturity_level"]
    type_avgs = results.get("type_averages", {})
    consistency_flags = results.get("consistency_flags", {})
    colour = maturity["colour"]

    org_name    = st.session_state.org_name or "Your Organisation"
    org_sector  = st.session_state.org_sector
    org_country = st.session_state.org_country
    perception  = st.session_state.self_perception_gap or {}
    benchmark   = SECTOR_BENCHMARKS.get(org_sector, SECTOR_BENCHMARKS["Other Energy"])

    st.markdown('<div class="section-header">📊 Assessment Results</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{org_name} · {org_sector} · {org_country}</div>', unsafe_allow_html=True)

    # ── MATURITY LEVELS GUIDE ──
    with st.expander("📖 Maturity Level Guide — What Each Level Means", expanded=False):
        st.markdown(
            "<div style='font-size:12px;color:#9CA3AF;font-style:italic;margin-bottom:16px;"
            "border-left:3px solid #4FC3F7;padding-left:10px;'>"
            "Five maturity levels grounded in Gartner's AI Maturity Model, relabelled for GCC energy "
            "operator context. Gartner equivalents shown for reference.</div>",
            unsafe_allow_html=True
        )
        level_meta = [
            (1, "🔴", "#EF4444", "#FEF2F2", "Digital Laggard", "Foundational", "1.0 – 1.8",
             "AI activity is absent or entirely exploratory. No formal strategy, fragmented data, and no executive accountability for AI outcomes. The organisation faces significant risk of falling behind GCC peers as the region accelerates toward AI-native operations."),
            (2, "🟠", "#F97316", "#FFF7ED", "Pilot Stage", "Emerging", "1.8 – 2.6",
             "Early pilots exist but results are inconsistent and not at scale. AI sits in pockets — typically in IT or strategy — rather than embedded in operations. The most common trap: deploying technology before fixing the underlying accountability, data quality, and capability gaps that will prevent adoption."),
            (3, "🟡", "#D97706", "#FFFBEB", "Emerging Operator", "Operational", "2.6 – 3.4",
             "AI is operational in defined areas with structured ownership and measurable outcomes. Foundational capability exists but the organisation has not yet scaled across functions or asset classes. The critical question: is the capability internally owned or dependent on external vendors?"),
            (4, "🟢", "#22C55E", "#F0FDF4", "Scaling Practitioner", "Scaled", "3.4 – 4.2",
             "AI is embedded across multiple functions with board-level visibility and measurable ROI. The organisation is building genuine competitive differentiation through operational intelligence. The remaining challenge is institutionalising value measurement so AI investment is reported with the same rigour as capital expenditure."),
            (5, "🔵", "#0055A4", "#EFF6FF", "AI-Native Enterprise", "Transformational", "4.2 – 5.0",
             "AI is business DNA. Decisions across operations, finance, and strategy are AI-augmented by default. Internal capability is the norm — external vendors execute, not advise. The organisation serves as a GCC benchmark and actively shapes national AI ecosystem development."),
        ]
        for lvl, lv_icon, lv_colour, lv_bg, lv_label, lv_gartner, lv_range, lv_desc in level_meta:
            st.markdown(f"""
<div style="display:flex;gap:16px;padding:16px 0;border-bottom:1px solid #F0F2F5;align-items:flex-start;">
  <div style="min-width:40px;text-align:center;">
    <div style="background:{lv_bg};border:2px solid {lv_colour};border-radius:8px;padding:6px 4px;font-size:18px;">{lv_icon}</div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:700;color:{lv_colour};margin-top:4px;">L{lvl}</div>
  </div>
  <div style="flex:1;">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;flex-wrap:wrap;">
      <span style="font-size:15px;font-weight:700;color:#003366;">{lv_label}</span>
      <span style="background:#EEF4FF;color:#003366;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;padding:2px 8px;border-radius:3px;">Gartner: {lv_gartner}</span>
      <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#9CA3AF;">Score {lv_range}</span>
    </div>
    <div style="font-size:13px;color:#4B5563;line-height:1.65;">{lv_desc}</div>
  </div>
</div>""", unsafe_allow_html=True)

    col_score, col_chart = st.columns([1, 2], gap="large")

    with col_score:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-number" style="color:{colour};">{overall}<span class="score-denom">/5</span></div>
            <div class="maturity-label" style="color:{colour};">{maturity['icon']} {maturity['label']}</div>
            <div class="gartner-equiv">Level {maturity['level']} of 5 · Gartner: {maturity['gartner']}</div>
            <div class="maturity-desc">{maturity['description']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Sector benchmark
        gcc_range_low = benchmark.get("gcc_range_low", 2.0)
        gcc_range_high = benchmark.get("gcc_range_high", 2.8)
        if overall < gcc_range_low:
            position_label = "Below indicative range"
            position_colour = "#EF4444"
        elif overall > gcc_range_high:
            position_label = "Above indicative range"
            position_colour = "#22C55E"
        else:
            position_label = "Within indicative range"
            position_colour = "#F59E0B"
        st.markdown(f"""
        <div class="card" style="margin-top:16px;padding:18px 20px;">
            <div style="font-size:11px;font-weight:600;color:#6B7280;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;">
                Sector Benchmark
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span style="font-size:13px;color:#374151;">Indicative Sector Range</span>
                <span style="font-family:'IBM Plex Mono',monospace;font-weight:700;color:#374151;">{gcc_range_low} — {gcc_range_high}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span style="font-size:13px;color:#374151;">Your Score</span>
                <span style="font-family:'IBM Plex Mono',monospace;font-weight:700;color:{colour};">{overall}/5.0</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span style="font-size:13px;color:#374151;">Position</span>
                <span style="font-size:12px;font-weight:700;color:{position_colour};">{position_label}</span>
            </div>
            <div style="font-size:11px;color:#9CA3AF;font-style:italic;border-top:1px solid #F0F2F5;padding-top:8px;">
                Indicative ranges based on publicly available GCC energy AI disclosures. Not derived from a proprietary survey dataset.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Self-perception gap
        if perception and perception.get("gap") is not None:
            direction = perception["direction"]
            card_class = {"overestimate": "perception-over", "underestimate": "perception-under", "aligned": "perception-aligned"}.get(direction, "perception-aligned")
            icon = {"overestimate": "⚠️", "underestimate": "✅", "aligned": "✓"}.get(direction, "•")
            st.markdown(f"""
            <div class="perception-card {card_class}">
                <div style="font-size:12px;font-weight:700;color:#374151;margin-bottom:6px;">{icon} Self-Perception Gap</div>
                <div style="font-size:12px;color:#4B5563;line-height:1.55;">{perception['interpretation']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Pattern analysis
        if type_avgs:
            st.markdown('<div style="margin-top:16px;font-size:11px;font-weight:600;color:#6B7280;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;">Pattern Analysis</div>', unsafe_allow_html=True)
            type_icons = {"Current State": "📍", "Accountability": "👤", "Dependency": "🔗", "Translation": "⚙️", "Evidence": "✅"}
            for qtype, avg in sorted(type_avgs.items(), key=lambda x: x[1]):
                icon = type_icons.get(qtype, "•")
                pct = (avg / 5.0) * 100
                c = "#EF4444" if avg < 2.0 else "#F97316" if avg < 2.6 else "#EAB308" if avg < 3.4 else "#22C55E"
                st.markdown(f"""
                <div style="margin-bottom:9px;">
                    <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;">
                        <span style="color:#374151;">{icon} {qtype}</span>
                        <span style="color:{c};font-weight:600;font-family:'IBM Plex Mono',monospace;">{avg}</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width:{pct}%;background:{c};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with col_chart:
        categories = list(dim_scores.keys())
        values = list(dim_scores.values())

        # Short labels for radar chart — full names in key below
        SHORT_LABELS = {
            "Strategic Mandate & Executive Accountability": "D1 · Strategic Mandate",
            "Data & OT Infrastructure Readiness":          "D2 · Data & OT",
            "Operational Credibility of the AI Programme": "D3 · Operational Credibility",
            "Internal Capability & Ownership":             "D4 · Internal Capability",
            "Value Realisation Discipline":                "D5 · Value Realisation",
        }
        short_cats = [SHORT_LABELS.get(c, c) for c in categories]
        cats_plot = short_cats + [short_cats[0]]
        vals_plot = values + [values[0]]

        range_mid = round((benchmark["gcc_range_low"] + benchmark["gcc_range_high"]) / 2, 2)
        median_vals = [range_mid] * len(categories) + [range_mid]

        fig = go.Figure()
        for ref_val in [1, 2, 3, 4, 5]:
            fig.add_trace(go.Scatterpolar(
                r=[ref_val] * len(categories) + [ref_val],
                theta=cats_plot, fill=None,
                line=dict(color="rgba(0,51,102,0.07)", width=1),
                showlegend=False, hoverinfo="skip",
            ))
        fig.add_trace(go.Scatterpolar(
            r=median_vals, theta=cats_plot, fill="toself",
            fillcolor="rgba(100,116,139,0.06)",
            line=dict(color="rgba(100,116,139,0.4)", width=1.5, dash="dot"),
            name=f"GCC {org_sector} Range midpoint ({range_mid})",
            hovertemplate=f"Indicative range: {benchmark['gcc_range_low']}–{benchmark['gcc_range_high']}<extra></extra>",
        ))
        fig.add_trace(go.Scatterpolar(
            r=vals_plot, theta=cats_plot, fill="toself",
            fillcolor="rgba(0, 85, 164, 0.12)",
            line=dict(color="#0055A4", width=2.5),
            marker=dict(size=9, color="#4FC3F7", symbol="circle",
                        line=dict(color="#003366", width=2)),
            name=org_name,
            hovertemplate="<b>%{theta}</b><br>Score: %{r}/5<extra></extra>",
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(240,244,250,0.4)",
                radialaxis=dict(
                    visible=True, range=[0, 5], tickvals=[1,2,3,4,5],
                    tickfont=dict(size=10, color="#9CA3AF", family="IBM Plex Mono"),
                    gridcolor="rgba(0,51,102,0.07)", linecolor="rgba(0,51,102,0.07)",
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, color="#1E3A5F", family="IBM Plex Sans"),
                    gridcolor="rgba(0,51,102,0.05)", linecolor="rgba(0,51,102,0.05)",
                ),
            ),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(font=dict(size=11, family="IBM Plex Sans"), bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=70, r=70, t=40, b=40), height=440,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Dimension key below chart
        st.markdown(
            "<div style='background:#FFFFFF;border:1px solid #E5E9F0;border-radius:10px;"
            "padding:16px 20px;margin-top:4px;box-shadow:0 1px 4px rgba(0,51,102,0.04);'>"
            "<div style='font-size:11px;font-weight:600;color:#6B7280;letter-spacing:1.5px;"
            "text-transform:uppercase;margin-bottom:10px;'>Dimension Key</div>",
            unsafe_allow_html=True
        )
        for i, (full, short) in enumerate(SHORT_LABELS.items()):
            dk_score = dim_scores.get(full, 0)
            dk_c = "#EF4444" if dk_score < 1.8 else "#F97316" if dk_score < 2.6 else "#EAB308" if dk_score < 3.4 else "#22C55E" if dk_score < 4.2 else "#0055A4"
            dk_icon = DIMENSION_ICONS.get(full, "•")
            dk_label = get_score_label(dk_score)
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:1px solid #F0F2F5;">
  <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:700;color:#003366;min-width:24px;">D{i+1}</span>
  <span style="font-size:12px;color:#374151;flex:1;">{dk_icon} {full}</span>
  <span style="font-family:'IBM Plex Mono',monospace;font-size:13px;font-weight:700;color:{dk_c};">{dk_score}</span>
  <span style="font-size:10px;color:{dk_c};min-width:90px;text-align:right;">{dk_label}</span>
</div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Dimension scores with consistency flags
    st.markdown('<div class="card" style="margin-top:8px;">', unsafe_allow_html=True)
    for dim, score in sorted(dim_scores.items(), key=lambda x: x[1]):
        label = get_score_label(score)
        pct = (score / 5.0) * 100
        icon = DIMENSION_ICONS.get(dim, "•")
        c = "#EF4444" if score < 1.8 else "#F97316" if score < 2.6 else "#EAB308" if score < 3.4 else "#22C55E" if score < 4.2 else "#0055A4"
        flag = consistency_flags.get(dim, {})
        flag_html = ""
        if flag.get("flagged"):
            flag_html = f'<span style="font-size:10px;color:#F59E0B;font-weight:600;margin-left:8px;">⚠ Consistency Flag</span>'
        st.markdown(f"""
        <div style="margin-bottom:16px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                <span style="font-size:13px;color:#374151;font-weight:500;">{icon} {dim}{flag_html}</span>
                <span style="font-family:'IBM Plex Mono',monospace;font-size:14px;font-weight:700;color:{c};">
                    {score} <span style="font-size:11px;opacity:0.7;">{label}</span>
                </span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width:{pct}%;background:{c};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Consistency flags detail
    flagged_dims = {d: f for d, f in consistency_flags.items() if f.get("flagged")}
    if flagged_dims:
        st.markdown('<div class="section-header" style="font-size:18px;">⚠️ Consistency Flags</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">These dimensions show internally contradictory answers. The gap itself is a diagnostic finding.</div>', unsafe_allow_html=True)
        for dim, flag_data in flagged_dims.items():
            st.markdown(f"""
            <div class="flag-card">
                <div class="flag-title">⚠ {dim}</div>
                <div class="flag-text">{flag_data['interpretation']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Report
    st.markdown('<div class="section-header">📋 Consulting Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Sector-calibrated, context-aware advisory report. Formatted as a consulting deliverable for executive review.</div>', unsafe_allow_html=True)

    if st.session_state.report_text is None:
        col_btn = st.columns([1,2,1])[1]
        with col_btn:
            if st.button("Generate My Consulting Report →"):
                with st.spinner("Generating your sector-calibrated report — 20–30 seconds..."):
                    report = generate_report(
                        org_name=org_name,
                        org_sector=org_sector,
                        org_country=org_country,
                        dimension_scores=dim_scores,
                        overall_score=overall,
                        maturity_level=maturity,
                        type_averages=type_avgs,
                        consistency_flags=consistency_flags,
                        self_perception_gap=perception,
                        context_responses=st.session_state.context_responses,
                    )
                    st.session_state.report_text = report
                    st.rerun()
    else:
        # Strip any code block formatting the API may have introduced
        import re
        clean_report = st.session_state.report_text
        # Remove fenced code blocks (```...```)
        clean_report = re.sub(r'```[\w]*\n?', '', clean_report)
        # Remove inline code backticks but preserve the text inside
        clean_report = re.sub(r'`([^`]+)`', r'\1', clean_report)

        st.markdown('<div class="report-wrapper">', unsafe_allow_html=True)
        st.markdown(clean_report)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn = st.columns([1,2,1])[1]
        with col_btn:
            if st.button("↩ Start New Assessment"):
                for k, v in defaults.items():
                    st.session_state[k] = v
                st.rerun()


# ════════════════════════════════════════════
# ASSESSMENT FORM
# ════════════════════════════════════════════
def show_assessment_form():

    # ── PROFILE ──
    st.markdown('<div class="section-header">Organisation Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Calibrates sector benchmarks and report recommendations to your context.</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        org_name = st.text_input("Organisation Name", placeholder="e.g. Gulf Power Co",
                                  value=st.session_state.org_name)
    with c2:
        sectors = list(SECTOR_BENCHMARKS.keys())
        idx = sectors.index(st.session_state.org_sector) if st.session_state.org_sector in sectors else 0
        org_sector = st.selectbox("Sector", sectors, index=idx)
    with c3:
        countries = ["Saudi Arabia","UAE","Qatar","Kuwait","Bahrain","Oman","Other GCC"]
        org_country = st.selectbox("Country", countries)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── CONTEXT LAYER ──
    st.markdown('<div class="section-header">Organisational Context</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">5 questions that calibrate the 90-day roadmap to your constraints. Not scored — used only to contextualise recommendations.</div>', unsafe_allow_html=True)

    context_responses = {}
    context_complete = True
    self_perception_answer = None

    st.markdown('<div class="card card-accent">', unsafe_allow_html=True)
    for cq in CONTEXT_QUESTIONS:
        st.markdown(f'<div class="help-text">💡 {cq["help"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="q-text"><b>{cq["text"]}</b></div>', unsafe_allow_html=True)
        options = cq["options"]
        selected = st.radio(
            label=cq["text"],
            options=options,
            index=None,
            key=f"ctx_{cq['id']}",
            label_visibility="collapsed",
        )
        if selected:
            context_responses[cq["id"]] = selected
            if cq["id"] == "ctx_maturity_self":
                self_perception_answer = selected
        else:
            context_complete = False
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid #E5E9F0;margin:8px 0 32px 0;'>", unsafe_allow_html=True)

    # ── ASSESSMENT QUESTIONS ──
    st.markdown('<div class="section-header">Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">25 questions across 5 dimensions. Answer based on current reality — not plans or aspirations.</div>', unsafe_allow_html=True)

    responses = {}
    all_answered = True
    answered_count = 0
    total_count = sum(len(QUESTIONS[d]) for d in DIMENSIONS)

    for i, dimension in enumerate(DIMENSIONS):
        icon = DIMENSION_ICONS[dimension]
        subtitle = DIMENSION_SUBTITLES[dimension]

        st.markdown(f"""
        <div class="card card-accent">
            <div class="dim-number">Dimension {i+1} of 5</div>
            <div class="dim-title">{icon} {dimension}</div>
            <div class="dim-subtitle">"{subtitle}"</div>
        </div>
        """, unsafe_allow_html=True)

        for j, q in enumerate(QUESTIONS[dimension]):
            q_num = i * 5 + j + 1
            options_display = [opt[0] for opt in q["options"]]
            options_scores  = {opt[0]: opt[1] for opt in q["options"]}

            st.markdown(f"""
            <div style="margin-bottom:6px;">
                <span class="q-type-badge">{q['type']}</span>
                <div class="q-text">Q{q_num}. {q['text']}</div>
            </div>
            """, unsafe_allow_html=True)

            selected = st.radio(
                label=q["text"],
                options=options_display,
                index=None,
                key=f"q_{q['id']}",
                label_visibility="collapsed",
            )

            if selected is not None:
                responses[q["id"]] = options_scores[selected]
                answered_count += 1
            else:
                all_answered = False

            if j < len(QUESTIONS[dimension]) - 1:
                st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # Progress bar
    total_questions = total_count + len(CONTEXT_QUESTIONS)
    answered_total  = answered_count + len(context_responses)
    pct = int((answered_total / total_questions) * 100)
    st.markdown(f"""
    <div class="card" style="padding:16px 20px;">
        <div style="display:flex;justify-content:space-between;font-size:13px;color:#6B7280;margin-bottom:8px;">
            <span>Progress</span>
            <span style="font-weight:600;color:#003366;">{answered_total} / {total_questions} questions answered</span>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,#003366,#4FC3F7);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ready = all_answered and context_complete
    col_btn = st.columns([1,2,1])[1]
    with col_btn:
        submit = st.button(
            "Calculate My AI Maturity →" if ready else "Complete all questions to continue",
            disabled=not ready,
        )

    if submit and ready:
        results = compute_scores(responses)
        perception = compute_self_perception_gap(
            self_perception_answer or "",
            results["overall_score"]
        ) if self_perception_answer else {}

        st.session_state.results          = results
        st.session_state.show_results     = True
        st.session_state.org_name         = org_name
        st.session_state.org_sector       = org_sector
        st.session_state.org_country      = org_country
        st.session_state.context_responses= context_responses
        st.session_state.self_perception_gap = perception
        st.rerun()


# ── ROUTER ──
if st.session_state.show_results and st.session_state.results:
    show_results_view(st.session_state.results)
else:
    show_assessment_form()

# ── FOOTER ──
st.markdown("""
<div style="margin-top:64px;padding:28px 0;border-top:1px solid #E5E9F0;text-align:center;">
    <div style="font-size:13px;color:#9CA3AF;">
        AI Maturity Compass · Built by
        <a href="https://linkedin.com/in/qassimalmansoor" target="_blank"
           style="color:#003366;text-decoration:none;font-weight:600;">Qasim Almansoor</a>
    </div>
    <div style="font-size:11px;color:#D1D5DB;margin-top:5px;">
        GCC Energy AI Maturity Framework · Adapted from Gartner's AI Maturity Model · 2026
    </div>
</div>
""", unsafe_allow_html=True)
