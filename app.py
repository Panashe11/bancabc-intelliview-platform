import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="BancABC | INTELLIVIEW — Customer Intelligence & Decision Support",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Relative path first (for GitHub / Streamlit Cloud), fallback to local Windows path
LOCAL_PATH = r"C:\Users\chade\Downloads\BancABC_2026\bancabc_intelliview_scored_customers.csv"
SCORED_DATA_PATH = (
    "bancabc_intelliview_scored_customers.csv"
    if os.path.exists("bancabc_intelliview_scored_customers.csv")
    else LOCAL_PATH
)

HUB_NAME_MAP = {
    "501": "Harare Main",
    "504": "Samora Machel (Harare)",
    "511": "Borrowdale (Harare)",
    "517": "Bulawayo Main",
    "523": "Mutare",
    "529": "Gweru",
}

NAV_SECTIONS = [
    ("EXECUTIVE", [("overview", "Executive Overview")]),
    (
        "CUSTOMER INTELLIGENCE",
        [
            ("intelligence", "Customer Intelligence"),
            ("retention", "Customer Retention"),
            ("segmentation", "Customer Segmentation"),
        ],
    ),
    (
        "GROWTH & CHANNELS",
        [
            ("growth", "Growth Opportunities"),
            ("digital", "Digital Engagement"),
            ("experience", "Customer Experience"),
        ],
    ),
    ("GOVERNANCE", [("settings", "Settings")]),
]

NAV_ICONS = {
    "overview": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>""",
    "intelligence": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>""",
    "retention": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>""",
    "segmentation": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>""",
    "growth": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>""",
    "digital": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>""",
    "experience": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>""",
    "settings": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>""",
}

if "active_nav" not in st.session_state:
    st.session_state.active_nav = "overview"

# BancABC Corporate Navy & Gold Enterprise Theme (10m Boardroom Visibility)
st.markdown(
    """
    <style>
    /* Main canvas & pure white high-contrast text */
    .stApp {
        background: linear-gradient(160deg, #071936 0%, #0C234B 55%, #102D5E 100%);
        color: #FFFFFF;
    }
    html, body, [class*="css"], p, span, div, label, li, td, th, h1, h2, h3, h4 {
        color: #FFFFFF !important;
    }

    /* Sidebar container matching BancABC corporate navy */
    section[data-testid="stSidebar"] {
        background-color: #102B5B !important;
        border-right: 1px solid #244682 !important;
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 1.1rem;
    }

    /* Sidebar Brand Header Lockup */
    .bancabc-header {
        border-bottom: 1px solid rgba(255, 255, 255, 0.22);
        padding-bottom: 14px;
        margin-bottom: 14px;
    }
    .bancabc-lockup {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .bancabc-logo-col {
        border-right: 1px solid rgba(255, 255, 255, 0.35);
        padding-right: 12px;
        line-height: 1.1;
    }
    .bancabc-name {
        font-size: 20px !important;
        font-weight: 900 !important;
        letter-spacing: -0.3px;
        color: #FFFFFF !important;
    }
    .bancabc-sub {
        font-size: 10px !important;
        color: #CBD5E1 !important;
        letter-spacing: 0.4px;
    }
    .intelliview-wordmark {
        font-size: 16px !important;
        font-weight: 800 !important;
        letter-spacing: 2.2px;
        color: #F5B82E !important;
    }
    .platform-tagline {
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #E2E8F0 !important;
        margin-top: 8px;
    }

    /* Sidebar Section Labels */
    .nav-section-title {
        font-size: 11px !important;
        font-weight: 800 !important;
        letter-spacing: 1.3px;
        color: #93B4E8 !important;
        margin: 14px 0 6px 4px;
        text-transform: uppercase;
    }

    /* Sidebar Navigation Buttons (Default & Active Gold-Bordered State) */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        justify-content: flex-start !important;
        text-align: left !important;
        background-color: transparent !important;
        border: 2px solid transparent !important;
        border-radius: 10px !important;
        padding: 9px 14px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #E2E8F0 !important;
        transition: all 0.15s ease-in-out;
        margin-bottom: 2px;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
    }
    /* Active Sidebar Item with Gold Pill Outline & Left Accent Bar */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background-color: rgba(245, 184, 46, 0.10) !important;
        border: 2px solid #F5B82E !important;
        border-left: 6px solid #F5B82E !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }

    /* Executive Glass Cards */
    .glass-card {
        background-color: #0D2754;
        border: 1.5px solid #265196;
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 10px 26px rgba(0, 0, 0, 0.38);
        height: 100%;
    }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .card-title {
        font-size: 17px !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
    }
    .badge-bank {
        background-color: #133875;
        color: #F5B82E !important;
        border: 1.5px solid #F5B82E;
        padding: 3px 11px;
        border-radius: 8px;
        font-size: 12px !important;
        font-weight: 800 !important;
    }
    .big-stat {
        font-size: 44px !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        line-height: 1.1;
    }
    .stat-green {
        font-size: 16px !important;
        font-weight: 800 !important;
        color: #34D399 !important;
        margin-left: 10px;
    }
    .stat-sub {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #CBD5E1 !important;
        margin-top: 8px;
    }

    /* Top Filter Radio Pills */
    div[role="radiogroup"] > label {
        background-color: #0D2754 !important;
        border: 1.5px solid #2E64B8 !important;
        border-radius: 10px;
        padding: 6px 13px !important;
        margin-right: 5px;
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }
    div[role="radiogroup"] > label:hover {
        border-color: #F5B82E !important;
        background-color: #153B7A !important;
    }

    /* Multiselect / Selectbox Input & Dropdown Visibility */
    div[data-baseweb="select"] > div,
    input[type="text"] {
        background-color: #0D2754 !important;
        border: 1.5px solid #2E64B8 !important;
        color: #FFFFFF !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] div {
        color: #FFFFFF !important;
    }
    span[data-baseweb="tag"] {
        background-color: #153B7A !important;
        border: 1.5px solid #F5B82E !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }
    span[data-baseweb="tag"] span,
    span[data-baseweb="tag"] svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    ul[role="listbox"],
    div[role="listbox"] {
        background-color: #091E42 !important;
        border: 1.5px solid #2E64B8 !important;
        border-radius: 10px !important;
    }
    li[role="option"],
    div[role="option"] {
        background-color: #091E42 !important;
        color: #FFFFFF !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 9px 14px !important;
    }
    li[role="option"]:hover,
    div[role="option"]:hover,
    li[aria-selected="true"],
    div[aria-selected="true"] {
        background-color: #153B7A !important;
        color: #F5B82E !important;
        font-weight: 800 !important;
    }

    /* Primary action / download buttons */
    .stDownloadButton > button {
        background-color: #133875 !important;
        color: #FFFFFF !important;
        border: 2px solid #F5B82E !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
    }
    .stDownloadButton > button:hover {
        background-color: #1B4E9E !important;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #0D2754;
        border: 1.5px solid #265196;
        border-radius: 14px;
        padding: 16px 20px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #F5B82E !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, low_memory=False)
    if "branch_hub" in data.columns:
        data["branch_hub"] = (
            data["branch_hub"]
            .astype(str)
            .str.replace(r"\.0$", "", regex=True)
            .str.strip()
            .replace(HUB_NAME_MAP)
        )
    return data


if not os.path.exists(SCORED_DATA_PATH):
    st.error(
        f"Scored file not found at `{SCORED_DATA_PATH}`.\n\n"
        "Run `python intelliview_engine.py` in your terminal first."
    )
    st.stop()

df = load_data(SCORED_DATA_PATH)

# Sidebar with BancABC | INTELLIVIEW Lockup & Categorized Navigation
with st.sidebar:
    st.markdown(
        """
        <div class="bancabc-header">
            <div class="bancabc-lockup">
                <div class="bancabc-logo-col">
                    <div class="bancabc-name">BancABC</div>
                    <div class="bancabc-sub">part of atlasmara</div>
                </div>
                <div class="intelliview-wordmark">INTELLIVIEW</div>
            </div>
            <div class="platform-tagline">Customer Intelligence &amp; Decision Support</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for section_label, items in NAV_SECTIONS:
        st.markdown(f'<div class="nav-section-title">{section_label}</div>', unsafe_allow_html=True)
        for key, label in items:
            is_active = st.session_state.active_nav == key
            if st.button(
                label,
                key=f"nav_{key}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
            ):
                st.session_state.active_nav = key
                st.rerun()

# Top Slicer Bar (Branch Hub, Segment, Month, Risk Tier, Currency)
f1, f2, f3, f4, f5 = st.columns([1.3, 1.3, 1.8, 1.3, 1.0])
with f1:
    hub_opts = sorted(df["branch_hub"].dropna().unique().tolist())
    sel_hubs = st.multiselect("City / Branch Hub", hub_opts, placeholder="All Branch Hubs")
with f2:
    seg_opts = sorted(df["customer_segment"].dropna().unique().tolist())
    sel_segs = st.multiselect("Customer Segment", seg_opts, placeholder="All Segments")
with f3:
    st.markdown("<div style='font-size:13px;font-weight:700;margin-bottom:4px;'>Reporting Period</div>", unsafe_allow_html=True)
    sel_month = st.radio(
        "Month",
        ["All (6M)", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],
        horizontal=True,
        label_visibility="collapsed",
    )
with f4:
    st.markdown("<div style='font-size:13px;font-weight:700;margin-bottom:4px;'>Inactivity Risk Tier</div>", unsafe_allow_html=True)
    sel_tier = st.radio(
        "Risk Tier",
        ["All Tiers", "High", "Medium", "Low"],
        horizontal=True,
        label_visibility="collapsed",
    )
with f5:
    st.markdown("<div style='font-size:13px;font-weight:700;margin-bottom:4px;'>Currency</div>", unsafe_allow_html=True)
    sel_curr = st.radio(
        "Currency",
        ["All", "$-USD", "ZiG"],
        horizontal=True,
        label_visibility="collapsed",
    )

st.markdown("<hr style='border-color:#244682; margin:8px 0 18px 0;'>", unsafe_allow_html=True)

filtered = df.copy()
if sel_hubs:
    filtered = filtered[filtered["branch_hub"].isin(sel_hubs)]
if sel_segs:
    filtered = filtered[filtered["customer_segment"].isin(sel_segs)]
if sel_tier != "All Tiers":
    filtered = filtered[filtered["risk_category"] == sel_tier]
if sel_curr != "All":
    filtered = filtered[filtered["currency_group"] == sel_curr]

month_col_map = {
    "All (6M)": "total_6m_tx_count",
    "Jun": "tx_count_jun",
    "Jul": "tx_count_jul",
    "Aug": "tx_count_aug",
    "Sep": "tx_count_sep",
    "Oct": "tx_count_oct",
    "Nov": "tx_count_nov",
}
active_tx_col = month_col_map[sel_month]
active_page = st.session_state.active_nav

# 1. EXECUTIVE OVERVIEW
if active_page == "overview":
    total_cust = len(filtered)
    healthy_pct = ((filtered["risk_category"] == "Low").mean() * 100.0) if total_cust > 0 else 0.0
    early_alerts = int(filtered["early_behaviour_alert"].sum()) if total_cust > 0 else 0
    total_tx = int(filtered[active_tx_col].sum()) if total_cust > 0 else 0
    avg_inflow = filtered["avg_monthly_inflow_usd"].mean() if total_cust > 0 else 0.0

    col1, col2, col3 = st.columns([1.05, 1.15, 1.0])

    with col1:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-header">
                    <span class="card-title">Customer Base Overview</span>
                    <span class="badge-bank">AI Scored</span>
                </div>
                <div>
                    <span class="big-stat">{total_cust:,}</span>
                    <span class="stat-green">▲ {healthy_pct:.1f}% Healthy</span>
                </div>
                <div class="stat-sub">Early Decline Alerts: <b style="color:#F5B82E;">{early_alerts:,}</b> accounts</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        m_names = ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]
        m_vals = [int(filtered[f"tx_count_{m.lower()}"].sum()) for m in m_names]
        fig_spark = go.Figure(
            go.Scatter(
                x=m_names,
                y=m_vals,
                mode="lines+markers+text",
                text=[f"{v:,}" for v in m_vals],
                textposition="top center",
                textfont=dict(color="#FFFFFF", size=12),
                line=dict(color="#38BDF8", width=4),
                marker=dict(size=9, color="#F5B82E", line=dict(width=2, color="#FFFFFF")),
                fill="tozeroy",
                fillcolor="rgba(56, 189, 248, 0.16)",
            )
        )
        fig_spark.update_layout(
            height=205,
            margin=dict(l=15, r=15, t=28, b=15),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF", size=13),
            xaxis=dict(showgrid=False, color="#FFFFFF", tickfont=dict(size=13, color="#FFFFFF")),
            yaxis=dict(showgrid=False, showticklabels=False),
        )
        st.plotly_chart(fig_spark, width="stretch")

    with col2:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-header">
                    <span class="card-title">Top Segments by Volume &amp; Avg. Inflow</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <span class="big-stat">{total_tx:,}</span>
                        <span class="stat-green">▲ Active</span>
                        <div class="stat-sub">Total Transactions ({sel_month})</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="stat-sub">Avg. Monthly Inflow:</div>
                        <div style="font-size:28px; font-weight:900; color:#F5B82E;">${avg_inflow:,.2f}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        seg_vol = (
            filtered.groupby("customer_segment", as_index=False)["total_volume_usd"]
            .sum()
            .sort_values("total_volume_usd", ascending=True)
        )
        fig_seg = go.Figure(
            go.Bar(
                x=seg_vol["total_volume_usd"],
                y=seg_vol["customer_segment"],
                orientation="h",
                marker_color="#1D63B8",
                marker_line=dict(color="#38BDF8", width=1.5),
                text=[f"${v:,.0f}" for v in seg_vol["total_volume_usd"]],
                textposition="auto",
                textfont=dict(color="#FFFFFF", size=13, family="Arial Black"),
            )
        )
        fig_seg.update_layout(
            height=230,
            margin=dict(l=10, r=15, t=15, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF", size=13),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(color="#FFFFFF", tickfont=dict(size=13, color="#FFFFFF")),
        )
        st.plotly_chart(fig_seg, width="stretch")

    with col3:
        st.markdown(
            """
            <div class="glass-card">
                <div class="card-header">
                    <span class="card-title">Product Adoption by Inflow Tier</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        prod_cols = ["has_savings_account", "has_fixed_deposit", "has_prepaid_visa", "has_a360_app", "has_ally_whatsapp"]
        prod_labels = ["Savings", "Fixed Dep", "Visa Card", "A360 App", "Ally Chat"]

        for tier_name, bar_color in [("Middle Inflow", "#1D63B8"), ("High Inflow", "#F5B82E")]:
            sub_t = filtered[filtered["inflow_tier"] == tier_name]
            rates = [(sub_t[c].mean() * 100.0) if len(sub_t) > 0 else 0.0 for c in prod_cols]
            fig_p = go.Figure(
                go.Bar(
                    x=prod_labels,
                    y=rates,
                    text=[f"{r:.0f}%" for r in rates],
                    textposition="outside",
                    textfont=dict(color="#FFFFFF", size=12, family="Arial Black"),
                    marker_color=bar_color,
                )
            )
            fig_p.update_layout(
                title=dict(text=tier_name, font=dict(size=14, color="#FFFFFF")),
                height=180,
                margin=dict(l=10, r=10, t=30, b=25),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#FFFFFF"),
                xaxis=dict(color="#FFFFFF", tickfont=dict(size=12, color="#FFFFFF")),
                yaxis=dict(
                    range=[0, 122],
                    showgrid=True,
                    gridcolor="#244682",
                    color="#FFFFFF",
                    tickfont=dict(size=11, color="#FFFFFF"),
                ),
            )
            st.plotly_chart(fig_p, width="stretch")

    st.markdown(
        """
        <div class="glass-card" style="margin-top:10px;">
            <div class="card-header">
                <span class="card-title">Customer Inactivity Risk Performance &amp; Revenue Exposure</span>
                <span class="badge-bank">Explainable AI Tiers</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    risk_summary = (
        filtered.groupby("risk_category", as_index=False)
        .agg(
            Accounts=("customer_id", "count"),
            Avg_Risk_Score=("inactivity_risk_score", "mean"),
            Monthly_Inflow_Exposure_USD=("avg_monthly_inflow_usd", "sum"),
            Total_Volume_Exposure_USD=("total_volume_usd", "sum"),
        )
    )
    st.dataframe(risk_summary, width="stretch")

# 2. CUSTOMER INTELLIGENCE & CUSTOMER RETENTION (XAI + Early Decline)
elif active_page in ("intelligence", "retention"):
    title_txt = (
        "Customer Intelligence — Behavioral Profiles & Risk Scoring"
        if active_page == "intelligence"
        else "Customer Retention — Early Behavioral Decline & Explainable AI"
    )
    st.subheader(title_txt)
    search_id = st.text_input("Filter by Customer ID:", "")
    xai_df = (
        filtered[filtered["customer_id"].astype(str).str.contains(search_id.strip(), case=False)]
        if search_id.strip()
        else filtered
    )
    cols = [
        "priority_rank", "customer_id", "branch_hub", "customer_segment",
        "inactivity_risk_score", "ml_churn_prob", "risk_category",
        "days_since_last_tx", "tx_freq_change_pct", "explainable_ai_reason"
    ]
    st.dataframe(xai_df[[c for c in cols if c in xai_df.columns]].head(200), width="stretch")

# 3. CUSTOMER SEGMENTATION
elif active_page == "segmentation":
    st.subheader("Customer Segmentation — Branch Hub & Segment Matrix")
    seg_matrix = (
        filtered.groupby(["branch_hub", "customer_segment"], as_index=False)
        .agg(
            Customers=("customer_id", "count"),
            Avg_Monthly_Inflow_USD=("avg_monthly_inflow_usd", "mean"),
            Total_Volume_USD=("total_volume_usd", "sum"),
            Avg_Products_Held=("product_count", "mean"),
            High_Risk_Accounts=("risk_category", lambda s: (s == "High").sum()),
        )
        .sort_values("Total_Volume_USD", ascending=False)
    )
    st.dataframe(seg_matrix, width="stretch")

# 4. GROWTH OPPORTUNITIES (Cross-Sell & Priority Queue)
elif active_page == "growth":
    st.subheader("Growth Opportunities — Prioritized Cross-Sell & Next-Best-Action Queue")
    cols = [
        "priority_rank", "customer_id", "branch_hub", "customer_segment", "inflow_tier",
        "currency_group", "risk_category", "cross_sell_eligible",
        "cross_sell_target", "cross_sell_reason", "priority_score"
    ]
    available_cols = [c for c in cols if c in filtered.columns]
    st.dataframe(filtered[available_cols].head(200), width="stretch")
    st.download_button(
        label="Export Filtered Action Queue (CSV)",
        data=filtered[available_cols].to_csv(index=False).encode("utf-8"),
        file_name="bancabc_priority_action_queue.csv",
        mime="text/csv",
    )

# 5. DIGITAL ENGAGEMENT (A360 App, Ally WhatsApp & Prepaid Visa)
elif active_page == "digital":
    st.subheader("Digital Engagement — Channel Adoption & Digital Transaction Ratio")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("A360 Mobile App", f"{filtered['has_a360_app'].mean() * 100:.1f}%")
    d2.metric("Ally WhatsApp Banking", f"{filtered['has_ally_whatsapp'].mean() * 100:.1f}%")
    d3.metric("Prepaid Visa Card", f"{filtered['has_prepaid_visa'].mean() * 100:.1f}%")
    d4.metric("Avg Digital Tx Ratio", f"{filtered['digital_tx_ratio'].mean() * 100:.1f}%")

    hub_dig = (
        filtered.groupby("branch_hub", as_index=False)
        .agg(
            A360_App_Pct=("has_a360_app", lambda s: round(s.mean() * 100, 1)),
            Ally_WhatsApp_Pct=("has_ally_whatsapp", lambda s: round(s.mean() * 100, 1)),
            Prepaid_Visa_Pct=("has_prepaid_visa", lambda s: round(s.mean() * 100, 1)),
            Avg_Digital_Ratio_Pct=("digital_tx_ratio", lambda s: round(s.mean() * 100, 1)),
        )
    )
    st.dataframe(hub_dig, width="stretch")

# 6. CUSTOMER EXPERIENCE (What-If Retention & Friction Simulator)
elif active_page == "experience":
    st.subheader("Customer Experience — Service Friction & Retention 'What-If' Simulator")
    s1, s2, s3 = st.columns(3)
    sim_days = s1.slider("Days Since Last Transaction", 0, 180, 65)
    sim_drop = s2.slider("6-Month Velocity Change (%)", -100, 100, -45) / 100.0
    sim_fric = s3.selectbox("Service Complaint / Closure Flag?", ["No", "Yes"])

    recency_pts = min(50.0, (sim_days / 120.0) * 50.0)
    velocity_pts = min(40.0, max(0.0, -sim_drop) * 40.0)
    friction_pts = 10.0 if sim_fric == "Yes" else 0.0
    score = min(100.0, max(0.0, recency_pts + velocity_pts + friction_pts))
    tier = "High" if score >= 70 else ("Medium" if score >= 40 else "Low")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Simulated Risk Score", f"{score:.1f} / 100", f"{tier} Risk Tier")
    m2.metric("Recency Impact", f"+{recency_pts:.1f} pts", f"{sim_days} days")
    m3.metric("Velocity Impact", f"+{velocity_pts:.1f} pts", f"{int(sim_drop * 100)}% change")
    m4.metric("Service Friction", f"+{friction_pts:.1f} pts", sim_fric)

    if tier == "High":
        st.error("**Recommended Action:** Suppress product cross-sell pitches and trigger immediate RM / Ally WhatsApp retention outreach.")
    elif tier == "Medium":
        st.warning("**Recommended Action:** Enroll in low-friction digital engagement nurture and verify service satisfaction.")
    else:
        st.success("**Recommended Action:** Healthy engagement profile — eligible for A360 App, Fixed Deposit, or Prepaid Visa cross-sell.")

# 7. GOVERNANCE & SETTINGS
elif active_page == "settings":
    st.subheader("Governance & Platform Configuration")
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="card-header">
                <span class="card-title">Model Governance &amp; Data Pipeline Metadata</span>
                <span class="badge-bank">Production Ready</span>
            </div>
            <p class="stat-sub"><b>Active Dataset:</b> {SCORED_DATA_PATH}</p>
            <p class="stat-sub"><b>Total Scored Customers:</b> {len(df):,} unique accounts across {df['branch_hub'].nunique()} regional branch hubs</p>
            <p class="stat-sub"><b>Risk Scoring Weights:</b> 50% Recency Gap (120-day horizon) + 40% 6-Month Velocity Decline + 10% Service Friction Flag</p>
            <p class="stat-sub"><b>Cross-Sell Guardrail:</b> Automatically suppresses product pitches for High-Risk or High-Friction accounts</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
