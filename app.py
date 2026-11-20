import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="BANCABC ANALYSIS — IntelliView AI Engine",
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

# BancABC High-Contrast Executive Banking Theme (10m Boardroom / Projector Visibility)
st.markdown(
    """
    <style>
    /* Main canvas & global pure white typography */
    .stApp {
        background: linear-gradient(160deg, #04142E 0%, #071D3E 55%, #0A254E 100%);
        color: #FFFFFF;
    }
    html, body, [class*="css"], p, span, div, label, li, td, th, h1, h2, h3, h4 {
        color: #FFFFFF !important;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #030F24;
        border-right: 2px solid #1E4976;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    /* Brand Header Card */
    .brand-card {
        background: linear-gradient(135deg, #003A70 0%, #005596 100%);
        border: 2px solid #F59E0B;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
    }
    .brand-title {
        font-size: 20px !important;
        font-weight: 900 !important;
        letter-spacing: 0.8px;
        color: #FFFFFF !important;
        margin: 0;
    }
    .brand-sub {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #FCD34D !important;
        margin: 4px 0 0 0;
    }

    /* Executive Glass Cards */
    .glass-card {
        background-color: #092244;
        border: 2px solid #1D4ED8;
        border-radius: 16px;
        padding: 22px 24px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45);
        height: 100%;
    }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .card-title {
        font-size: 18px !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
    }
    .badge-bank {
        background-color: #005596;
        color: #FFFFFF !important;
        border: 1.5px solid #F59E0B;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 13px !important;
        font-weight: 800 !important;
    }
    .big-stat {
        font-size: 46px !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        line-height: 1.1;
    }
    .stat-green {
        font-size: 17px !important;
        font-weight: 800 !important;
        color: #34D399 !important;
        margin-left: 10px;
    }
    .stat-sub {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #E2E8F0 !important;
        margin-top: 8px;
    }

    /* Radio pills & interactive controls */
    div[role="radiogroup"] > label {
        background-color: #0B2952 !important;
        border: 1.5px solid #3B82F6 !important;
        border-radius: 10px;
        padding: 7px 14px !important;
        margin-right: 6px;
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }
    div[role="radiogroup"] > label:hover {
        border-color: #F59E0B !important;
        background-color: #10386E !important;
    }

    /* Multiselect, text input & download buttons */
    div[data-baseweb="select"] > div,
    input[type="text"] {
        background-color: #0B2952 !important;
        border: 1.5px solid #3B82F6 !important;
        color: #FFFFFF !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }
    .stDownloadButton > button {
        background-color: #005596 !important;
        color: #FFFFFF !important;
        border: 2px solid #F59E0B !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
    }
    .stDownloadButton > button:hover {
        background-color: #0072CE !important;
    }

    /* Metric cards in Simulator */
    div[data-testid="stMetric"] {
        background-color: #092244;
        border: 2px solid #1D4ED8;
        border-radius: 14px;
        padding: 16px 20px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #FCD34D !important;
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

with st.sidebar:
    st.markdown(
        """
        <div class="brand-card">
            <p class="brand-title">🏛️ BANCABC ANALYSIS</p>
            <p class="brand-sub">IntelliView AI Engine</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Navigation")
    nav_page = st.radio(
        "Navigation",
        [
            "✨ Overview & Persona",
            "📈 Early Behaviour & XAI",
            "🎯 Cross-Sell & Priority",
            "🎛️ What-If Simulator",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### Portfolio Slicers")

    hub_opts = sorted(df["branch_hub"].dropna().unique().tolist())
    sel_hubs = st.multiselect("City / Branch Hub", hub_opts, placeholder="All Branch Hubs")

    seg_opts = sorted(df["customer_segment"].dropna().unique().tolist())
    sel_segs = st.multiselect("Customer Segment", seg_opts, placeholder="All Segments")

p1, p2, p3 = st.columns([2.2, 1.5, 1.2])
with p1:
    sel_month = st.radio(
        "Month",
        ["All (6M)", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],
        horizontal=True,
        label_visibility="collapsed",
    )
with p2:
    sel_tier = st.radio(
        "Risk Tier",
        ["All Tiers", "High", "Medium", "Low"],
        horizontal=True,
        label_visibility="collapsed",
    )
with p3:
    sel_curr = st.radio(
        "Currency",
        ["All", "$-USD", "ZiG"],
        horizontal=True,
        label_visibility="collapsed",
    )

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

if nav_page == "✨ Overview & Persona":
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
                    <span class="card-title">👥 Customer Base Overview</span>
                    <span class="badge-bank">AI Scored</span>
                </div>
                <div>
                    <span class="big-stat">{total_cust:,}</span>
                    <span class="stat-green">▲ {healthy_pct:.1f}% Healthy</span>
                </div>
                <div class="stat-sub">Early Decline Alerts: <b style="color:#FCD34D;">{early_alerts:,}</b> accounts</div>
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
                marker=dict(size=9, color="#F59E0B", line=dict(width=2, color="#FFFFFF")),
                fill="tozeroy",
                fillcolor="rgba(56, 189, 248, 0.18)",
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
                    <span class="card-title">📊 Top Segments by Volume & Avg. Inflow</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <span class="big-stat">{total_tx:,}</span>
                        <span class="stat-green">▲ Active</span>
                        <div class="stat-sub">Total Transactions ({sel_month})</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="stat-sub">Avg. Monthly Inflow:</div>
                        <div style="font-size:28px; font-weight:900; color:#FCD34D;">${avg_inflow:,.2f}</div>
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
                marker_color="#0072CE",
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
                    <span class="card-title">🏦 Product Adoption by Inflow Tier</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        prod_cols = ["has_savings_account", "has_fixed_deposit", "has_prepaid_visa", "has_a360_app", "has_ally_whatsapp"]
        prod_labels = ["Savings", "Fixed Dep", "Visa Card", "A360 App", "Ally Chat"]

        for tier_name, bar_color in [("Middle Inflow", "#0072CE"), ("High Inflow", "#F59E0B")]:
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
                    gridcolor="#1E4976",
                    color="#FFFFFF",
                    tickfont=dict(size=11, color="#FFFFFF"),
                ),
            )
            st.plotly_chart(fig_p, width="stretch")

    st.markdown(
        """
        <div class="glass-card" style="margin-top:10px;">
            <div class="card-header">
                <span class="card-title">🛡️ Customer Inactivity Risk Performance & Revenue Exposure</span>
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

elif nav_page == "📈 Early Behaviour & XAI":
    st.subheader("📈 Early Behavioral Decline Detection & Explainable AI Reason Codes")
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

elif nav_page == "🎯 Cross-Sell & Priority":
    st.subheader("🎯 Prioritized Cross-Sell & Next-Best-Action Queue")
    cols = [
        "priority_rank", "customer_id", "branch_hub", "customer_segment", "inflow_tier",
        "currency_group", "risk_category", "cross_sell_eligible",
        "cross_sell_target", "cross_sell_reason", "priority_score"
    ]
    available_cols = [c for c in cols if c in filtered.columns]
    st.dataframe(filtered[available_cols].head(200), width="stretch")
    st.download_button(
        label="⬇️ Export Filtered Action Queue (CSV)",
        data=filtered[available_cols].to_csv(index=False).encode("utf-8"),
        file_name="bancabc_priority_action_queue.csv",
        mime="text/csv",
    )

elif nav_page == "🎛️ What-If Simulator":
    st.subheader("🎛️ Interactive Customer Re-Engagement 'What-If' Simulator")
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
