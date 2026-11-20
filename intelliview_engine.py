import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FILE_PATH = r"C:\Users\chade\Downloads\BancABC_2026\BancABC_2026.csv"
OUTPUT_DIR = r"C:\Users\chade\Downloads\BancABC_2026"
SCORED_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "bancabc_intelliview_scored_customers.csv")
MODEL_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "bancabc_inactivity_model.joblib")


def build_intelliview_dataset(file_path: str) -> pd.DataFrame:
    print(f"Loading raw transactions from: {file_path} ...")
    df = pd.read_csv(file_path, low_memory=False)
    print(f"Loaded {df.shape[0]:,} rows x {df.shape[1]} columns")

    df.columns = [
        c.strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
        for c in df.columns
    ]

    if "transaction_id" in df.columns:
        df = df.drop_duplicates(subset=["transaction_id"]).copy()

    for col in ["date", "customer_last_transaction", "last_service_interaction", "last_digital_session"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

    amt_col = "amount_usd" if "amount_usd" in df.columns else [c for c in df.columns if "amount" in c][0]
    df["amount_usd"] = pd.to_numeric(df[amt_col], errors="coerce").fillna(0.0).abs()

    if "status" in df.columns:
        df = df[df["status"].astype(str).str.strip().str.lower() == "completed"].copy()

    df = df.dropna(subset=["customer_id", "date"]).copy()
    df["customer_id"] = df["customer_id"].astype(str).str.strip()

    ref_dt = df["date"].max()
    tx_type = df["type"].astype(str).str.upper() if "type" in df.columns else pd.Series("", index=df.index)
    df["is_active_tx"] = ~tx_type.isin(["SERVICE FEE", "INTEREST_POSTING", "MAINTENANCE_FEE"])
    df["is_inflow"] = df["dr_cr_indicator"].astype(str).str.upper().str.strip() == "CR" if "dr_cr_indicator" in df.columns else False

    dig_col = df["digital_channels_used"].fillna("").astype(str).str.strip() if "digital_channels_used" in df.columns else pd.Series("", index=df.index)
    df["is_digital"] = (dig_col != "") & (dig_col.str.lower() != "nan")

    active_df = df[df["is_active_tx"]].copy()

    df_sorted = df.sort_values("date")
    keep_cols = [
        c for c in [
            "customer_id", "branch_id", "email", "products_held", "loan_types",
            "card_types", "digital_channels_used", "customer_currencies", "service_reasons"
        ] if c in df.columns
    ]
    cust = df_sorted.groupby("customer_id")[keep_cols].last().reset_index(drop=True)

    hub_map = {
        "ZW591": "Harare — Samora Machel Hub",
        "ZW592": "Bulawayo — Jason Moyo Hub",
        "ZW593": "Mutare — Herbert Chitepo Hub",
        "ZW594": "Gweru — Main Street Hub",
        "ZW883": "Masvingo — Robert Mugabe Hub",
        "ZW884": "Kwekwe — Central Hub",
    }
    if "branch_id" in cust.columns:
        cust["branch_hub"] = cust["branch_id"].astype(str).str[:5].map(hub_map).fillna(cust["branch_id"].astype(str))
    else:
        cust["branch_hub"] = "Harare Main Hub"

    curr_raw = cust["customer_currencies"].fillna("USD").astype(str).str.upper() if "customer_currencies" in cust.columns else pd.Series("USD", index=cust.index)
    cust["currency_group"] = np.where(curr_raw.str.contains("ZWG|ZIG"), "ZiG", "$-USD")

    ref_period = ref_dt.to_period("M")
    month_labels = ["jun", "jul", "aug", "sep", "oct", "nov"]
    periods = [ref_period - i for i in range(5, -1, -1)]

    active_df["ym"] = active_df["date"].dt.to_period("M")
    monthly_piv = (
        active_df[active_df["ym"].isin(periods)]
        .groupby(["customer_id", "ym"])["transaction_id"]
        .count()
        .unstack(fill_value=0)
    )
    for p, m_name in zip(periods, month_labels):
        col_name = f"tx_count_{m_name}"
        cust[col_name] = cust["customer_id"].map(monthly_piv[p]).fillna(0).astype(int) if p in monthly_piv.columns else 0

    m_cols = [f"tx_count_{m}" for m in month_labels]
    cust["total_6m_tx_count"] = cust[m_cols].sum(axis=1)

    rfm = active_df.groupby("customer_id").agg(
        total_tx_count=("transaction_id", "count"),
        first_tx_date=("date", "min"),
        last_tx_date=("date", "max"),
        avg_tx_value_usd=("amount_usd", "mean"),
        total_volume_usd=("amount_usd", "sum"),
        digital_tx_ratio=("is_digital", "mean"),
    ).reset_index()

    inflows = (
        df[df["is_inflow"]]
        .groupby("customer_id")["amount_usd"]
        .agg(total_inflow_usd="sum", avg_monthly_inflow_usd=lambda s: s.sum() / 6.0)
        .reset_index()
    )

    cust = cust.merge(rfm, on="customer_id", how="left").merge(inflows, on="customer_id", how="left")
    for c in ["total_tx_count", "avg_tx_value_usd", "total_volume_usd", "digital_tx_ratio", "total_inflow_usd", "avg_monthly_inflow_usd"]:
        cust[c] = cust[c].fillna(0.0)

    cust["days_since_last_tx"] = (ref_dt - cust["last_tx_date"]).dt.days.fillna(999).clip(lower=0)
    cust["tenure_months"] = ((ref_dt - cust["first_tx_date"]).dt.days / 30.44).fillna(1).clip(lower=1).round(1)

    first_half = cust[["tx_count_jun", "tx_count_jul", "tx_count_aug"]].sum(axis=1)
    second_half = cust[["tx_count_sep", "tx_count_oct", "tx_count_nov"]].sum(axis=1)
    cust["tx_freq_change_pct"] = ((second_half - first_half) / first_half.clip(lower=1)).clip(-1.0, 3.0)

    prod_str = cust["products_held"].fillna("").astype(str) if "products_held" in cust.columns else pd.Series("", index=cust.index)
    dig_str = cust["digital_channels_used"].fillna("").astype(str) if "digital_channels_used" in cust.columns else pd.Series("", index=cust.index)

    cust["has_savings_account"] = prod_str.str.contains("Savings|Current", case=False).astype(int)
    cust["has_fixed_deposit"] = prod_str.str.contains("Fixed Deposit|Call Deposit", case=False).astype(int)
    cust["has_prepaid_visa"] = prod_str.str.contains("Credit Card|Prepaid|Visa", case=False).astype(int)
    cust["has_a360_app"] = (prod_str.str.contains("Digital Banking", case=False) | dig_str.str.contains("Mobile App|Internet", case=False)).astype(int)
    cust["has_ally_whatsapp"] = dig_str.str.contains("USSD|WhatsApp|Ally", case=False).astype(int)
    cust["product_count"] = (
        cust["has_savings_account"] + cust["has_fixed_deposit"] + cust["has_prepaid_visa"] + cust["has_a360_app"] + cust["has_ally_whatsapp"]
    )

    q66 = cust["avg_monthly_inflow_usd"].quantile(0.66)
    q33 = cust["avg_monthly_inflow_usd"].quantile(0.33)
    cust["inflow_tier"] = np.where(
        cust["avg_monthly_inflow_usd"] >= q66,
        "High Inflow",
        np.where(cust["avg_monthly_inflow_usd"] >= q33, "Middle Inflow", "Low Inflow"),
    )

    v80 = cust["total_volume_usd"].quantile(0.80)
    v60 = cust["total_volume_usd"].quantile(0.60)
    def assign_persona(row):
        if row["total_volume_usd"] >= v80 and row["has_fixed_deposit"] == 1:
            return "Corporate / High-Net-Worth"
        if row["total_volume_usd"] >= v60:
            return "SME / Active Trader"
        if row["has_a360_app"] == 1 and row["digital_tx_ratio"] >= 0.5:
            return "Salaried Digital Professional"
        if row["currency_group"] == "$-USD" and row["avg_monthly_inflow_usd"] > 0:
            return "FX / Remittance Recipient"
        return "Retail Everyday Banking"

    cust["customer_segment"] = cust.apply(assign_persona, axis=1)

    srv_str = cust["service_reasons"].fillna("").astype(str) if "service_reasons" in cust.columns else pd.Series("", index=cust.index)
    cust["high_friction_flag"] = srv_str.str.contains("closure|complaint|dispute", case=False).astype(int)

    recency_pts = np.clip((cust["days_since_last_tx"] / 120.0) * 50.0, 0, 50)
    drop_pts = np.clip((-cust["tx_freq_change_pct"]) * 40.0, 0, 40)
    friction_pts = cust["high_friction_flag"] * 10.0

    cust["inactivity_risk_score"] = (recency_pts + drop_pts + friction_pts).round(1)
    cust["risk_category"] = pd.cut(
        cust["inactivity_risk_score"], bins=[-1.0, 39.9, 69.9, 100.0], labels=["Low", "Medium", "High"]
    ).astype(str)
    cust["early_behaviour_alert"] = ((cust["inactivity_risk_score"] >= 55.0) | (cust["tx_freq_change_pct"] <= -0.40)).astype(int)
    cust["inactivity_target_label"] = (cust["risk_category"] == "High").astype(int)

    feats = [
        "tenure_months", "product_count", "total_6m_tx_count", "tx_freq_change_pct",
        "days_since_last_tx", "digital_tx_ratio", "avg_tx_value_usd", "avg_monthly_inflow_usd", "high_friction_flag"
    ]
    X = cust[feats].fillna(0.0)
    y = cust["inactivity_target_label"]
    if y.nunique() > 1 and len(cust) >= 40:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
        pipe = Pipeline([("scaler", StandardScaler()), ("clf", GradientBoostingClassifier(random_state=42))])
        pipe.fit(X_train, y_train)
        auc = roc_auc_score(y_test, pipe.predict_proba(X_test)[:, 1])
        print(f"Gradient Boosting Inactivity Model ROC-AUC: {auc:.4f}")
        cust["ml_churn_prob"] = pipe.predict_proba(X)[:, 1].round(4)
        joblib.dump(pipe, MODEL_OUTPUT_PATH)
    else:
        cust["ml_churn_prob"] = (cust["inactivity_risk_score"] / 100.0).round(4)

    def xai_reason(row):
        parts = []
        if row["days_since_last_tx"] >= 45:
            parts.append(f"{int(row['days_since_last_tx'])}d inactive")
        if row["tx_freq_change_pct"] <= -0.30:
            parts.append(f"Tx velocity {int(row['tx_freq_change_pct']*100)}%")
        if row["high_friction_flag"] == 1:
            parts.append(f"Friction: {row.get('service_reasons', 'Complaint')}")
        return " | ".join(parts) if parts else "Healthy recurring velocity"

    cust["explainable_ai_reason"] = cust.apply(xai_reason, axis=1)

    def cross_sell(row):
        if row["risk_category"] == "High":
            return 0, "Retention_Outreach", "Resolve high inactivity risk before pitching products"
        if row["has_a360_app"] == 0:
            return 1, "A360_App_Onboarding", "Active customer without A360 Digital Banking"
        if row["has_fixed_deposit"] == 0 and row["inflow_tier"] == "High Inflow":
            return 1, "Fixed_Deposit_Wealth", "High monthly inflow tier with no Fixed Deposit"
        if row["has_prepaid_visa"] == 0 and row["currency_group"] == "$-USD":
            return 1, "Prepaid_Visa_Card", "USD transactor eligible for Prepaid Visa Card"
        return 0, "Ally_WhatsApp_Nurture", "Maintain engagement via Ally WhatsApp Banking"

    cs = cust.apply(cross_sell, axis=1)
    cust["cross_sell_eligible"] = [x[0] for x in cs]
    cust["cross_sell_target"] = [x[1] for x in cs]
    cust["cross_sell_reason"] = [x[2] for x in cs]

    cust["priority_score"] = (
        cust["total_volume_usd"].rank(pct=True) * 40.0 + (cust["inactivity_risk_score"] / 100.0) * 60.0
    ).round(1)
    cust = cust.sort_values("priority_score", ascending=False).reset_index(drop=True)
    cust["priority_rank"] = cust.index + 1

    cust.to_csv(SCORED_OUTPUT_PATH, index=False)
    print(f"Saved {len(cust):,} scored customer profiles to: {SCORED_OUTPUT_PATH}")
    return cust


if __name__ == "__main__":
    build_intelliview_dataset(FILE_PATH)
