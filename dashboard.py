import streamlit as st
import pandas as pd

from ai_analyzer import analyze_payments


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="PayRecover AI",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🤖 PayRecover AI")
st.subheader("Intelligent Revenue Recovery Agent")

st.success(
    "🟢 AI Agent Online — Controlled Recovery Mode"
)


# =========================================================
# LOAD ANALYSIS
# =========================================================

results = analyze_payments()


# =========================================================
# AGENT ARCHITECTURE
# =========================================================

st.markdown("## 🏗️ Agent Architecture")

st.info(
    "Payment Failure → Gemini AI Diagnosis → "
    "Recovery Recommendation → Deterministic Safety Engine → "
    "Final Controlled Action → Recovery Simulation → "
    "Revenue & Audit Tracking"
)


# =========================================================
# EXECUTIVE METRICS
# =========================================================

st.markdown("## 📊 Executive Recovery Metrics")

total_at_risk = results["amount"].sum()

total_recovered = results["Recovered Amount"].sum()

total_unrecovered = total_at_risk - total_recovered

recovery_rate = (
    total_recovered / total_at_risk * 100
    if total_at_risk > 0
    else 0
)

payments_recovered = (
    results["Outcome"] == "RECOVERED"
).sum()

total_payments = len(results)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Revenue at Risk",
        f"₹{total_at_risk:,.0f}"
    )

with col2:
    st.metric(
        "💵 Revenue Recovered",
        f"₹{total_recovered:,.0f}"
    )

with col3:
    st.metric(
        "📈 Recovery Rate",
        f"{recovery_rate:.1f}%"
    )

with col4:
    st.metric(
        "✅ Payments Recovered",
        f"{payments_recovered}/{total_payments}"
    )


# =========================================================
# REVENUE LOSS ANALYSIS
# =========================================================

st.markdown("## 💸 Revenue Loss Analysis")

loss_col1, loss_col2 = st.columns(2)

with loss_col1:
    st.metric(
        "Revenue Still at Risk",
        f"₹{total_unrecovered:,.0f}"
    )

with loss_col2:

    unrecovered_count = (
        results["Outcome"] == "NOT RECOVERED"
    ).sum()

    st.metric(
        "Payments Not Recovered",
        unrecovered_count
    )


# =========================================================
# FAILURE REASON ANALYSIS
# =========================================================

st.markdown("## 🔎 Failure Reason Analysis")

failure_revenue = (
    results
    .groupby("failure_reason")["amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(failure_revenue)

failure_table = (
    results
    .groupby("failure_reason")
    .agg(
        Payments=("payment_id", "count"),
        Revenue_at_Risk=("amount", "sum"),
        Revenue_Recovered=(
            "Recovered Amount",
            "sum"
        )
    )
)

failure_table["Recovery_Rate"] = (
    failure_table["Revenue_Recovered"]
    / failure_table["Revenue_at_Risk"]
    * 100
).round(1)

st.dataframe(
    failure_table,
    use_container_width=True
)


# =========================================================
# SAFETY & RISK CONTROLS
# =========================================================

st.markdown("## 🛡️ Safety & Risk Controls")

col1, col2, col3 = st.columns(3)

with col1:

    approved_count = (
        results["Safety Status"] == "APPROVED"
    ).sum()

    st.metric(
        "Approved Actions",
        approved_count
    )

with col2:

    blocked_count = (
        results["Safety Status"] == "BLOCKED"
    ).sum()

    st.metric(
        "Blocked Actions",
        blocked_count
    )

with col3:

    high_risk_count = (
        results["Risk Level"] == "HIGH"
    ).sum()

    st.metric(
        "High Risk Cases",
        high_risk_count
    )


# =========================================================
# AI PERFORMANCE
# =========================================================

st.markdown("## 🧠 AI Analysis")

col1, col2, col3 = st.columns(3)

with col1:

    average_confidence = results[
        "Confidence"
    ].mean()

    st.metric(
        "Average AI Confidence",
        f"{average_confidence:.1f}%"
    )

with col2:

    gemini_count = (
        results["Analysis Source"] == "GEMINI"
    ).sum()

    st.metric(
        "Gemini Analyses",
        gemini_count
    )

with col3:

    fallback_count = (
        results["Analysis Source"] == "LOCAL FALLBACK"
    ).sum()

    st.metric(
        "Local Fallback Analyses",
        fallback_count
    )


# =========================================================
# RECOVERY STRATEGY DISTRIBUTION
# =========================================================

st.markdown("## 🎯 Recovery Strategy Distribution")

strategy_counts = (
    results["Recovery Action"]
    .value_counts()
)

st.bar_chart(strategy_counts)


# =========================================================
# REVENUE BY STRATEGY
# =========================================================

st.markdown("## 💰 Revenue Recovered by Strategy")

strategy_revenue = (
    results
    .groupby("Recovery Action")["Recovered Amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(strategy_revenue)


# =========================================================
# RISK DISTRIBUTION
# =========================================================

st.markdown("## ⚠️ Risk Distribution")

risk_counts = (
    results["Risk Level"]
    .value_counts()
)

st.bar_chart(risk_counts)


# =========================================================
# SAFETY OVERRIDES
# =========================================================

st.markdown("## 🛡️ Safety Overrides")

override_count = (
    results["Safety Override"] == True
).sum()

st.metric(
    "AI Recommendations Overridden by Safety Engine",
    override_count
)


# =========================================================
# RECOVERY RESULTS
# =========================================================

st.markdown("## 📈 Recovery Results")

outcome_counts = (
    results["Outcome"]
    .value_counts()
)

st.bar_chart(outcome_counts)


# =========================================================
# PAYMENT-LEVEL ANALYSIS
# =========================================================

st.markdown("## 🔍 Payment-Level Analysis")

display_columns = [
    "payment_id",
    "customer",
    "amount",
    "failure_reason",
    "Previous Attempts",
    "Analysis Source",
    "Confidence",
    "Recommended Strategy",
    "Recovery Action",
    "Risk Level",
    "Safety Status",
    "Outcome",
    "Recovered Amount",
    "Opportunity Score"
]

available_columns = [
    column
    for column in display_columns
    if column in results.columns
]

st.dataframe(
    results[available_columns],
    use_container_width=True
)


# =========================================================
# AUDIT TRAIL
# =========================================================

st.markdown("## 📋 Recovery Audit Trail")

audit_columns = [
    "payment_id",
    "customer",
    "amount",
    "AI Recommendation",
    "Recommended Strategy",
    "Recovery Action",
    "Safety Status",
    "Safety Override",
    "Risk Level",
    "Risk Score",
    "Outcome",
    "Recovered Amount"
]

available_audit_columns = [
    column
    for column in audit_columns
    if column in results.columns
]

st.dataframe(
    results[available_audit_columns],
    use_container_width=True
)


# =========================================================
# INTERACTIVE PAYMENT TEST
# =========================================================

st.markdown("---")

st.markdown("## 🧪 Test a Payment")

st.write(
    "Enter synthetic payment details to see how "
    "PayRecover AI responds."
)

test_col1, test_col2 = st.columns(2)


with test_col1:

    test_customer = st.text_input(
        "Customer Name",
        "Demo_Customer"
    )

    test_amount = st.number_input(
        "Payment Amount (₹)",
        min_value=1.0,
        value=5000.0,
        step=500.0
    )

    test_reason = st.selectbox(
        "Failure Reason",
        [
            "temporary",
            "insufficient_funds",
            "expired_card",
            "other"
        ]
    )


with test_col2:

    test_description = st.text_input(
        "Failure Description",
        "payment gateway timed out"
    )

    test_attempts = st.number_input(
        "Previous Retry Attempts",
        min_value=0,
        max_value=10,
        value=0,
        step=1
    )


# =========================================================
# TEST PAYMENT ANALYSIS
# =========================================================

if st.button(
    "🤖 Analyze Test Payment",
    type="primary"
):

    from gemini_agent import ask_gemini
    from safety_engine import evaluate_action
    from recovery_strategy import (
        recommend_recovery_strategy
    )

    # -----------------------------------------------------
    # AI DIAGNOSIS
    # -----------------------------------------------------

    test_analysis = ask_gemini(
        payment_description=test_description,
        amount=test_amount,
        previous_attempts=test_attempts
    )

    test_confidence = float(
        test_analysis.get(
            "confidence",
            50
        )
    )

    test_ai_action = test_analysis.get(
        "recommended_action",
        "ESCALATE"
    )

    test_diagnosis = test_analysis.get(
        "failure_reason",
        "Unknown failure"
    )


    # -----------------------------------------------------
    # RECOVERY STRATEGY
    # -----------------------------------------------------

    test_strategy = recommend_recovery_strategy(
        failure_reason=test_reason,
        failure_description=test_description,
        amount=test_amount,
        previous_attempts=test_attempts,
        risk_level="LOW",
        confidence=test_confidence
    )


    # -----------------------------------------------------
    # SAFETY ENGINE
    # -----------------------------------------------------

    safety_candidate = test_strategy["strategy"]

    # Keep RETRY as the candidate for temporary failures
    # with exhausted retry attempts so the deterministic
    # safety engine can explicitly BLOCK the retry.

    if (
        test_reason == "temporary"
        and test_attempts >= 2
    ):
        safety_candidate = "RETRY"

    (
        test_final_action,
        test_safety_status,
        test_safety_reasons,
        test_risk_level,
        test_risk_score
    ) = evaluate_action(
        recommended_action=safety_candidate,
        amount=test_amount,
        previous_attempts=test_attempts,
        payment_status="failed"
    )


    # -----------------------------------------------------
    # AI DECISION
    # -----------------------------------------------------

    st.markdown("### 🤖 AI Decision")

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:

        st.metric(
            "AI Recommendation",
            test_ai_action
        )

    with result_col2:

        st.metric(
            "Recovery Strategy",
            test_strategy["strategy"]
        )

    with result_col3:

        st.metric(
            "Final Action",
            test_final_action
        )


    # -----------------------------------------------------
    # SAFETY DECISION
    # -----------------------------------------------------

    st.markdown("### 🛡️ Safety Decision")

    if test_safety_status == "APPROVED":

        st.success(
            f"✅ Action APPROVED: "
            f"{test_final_action}"
        )

    else:

        st.error(
            f"🛑 Candidate Action BLOCKED: "
            f"{safety_candidate}"
        )

        st.success(
            f"Final Action: "
            f"{test_final_action}"
        )


    # -----------------------------------------------------
    # PAYMENT DETAILS
    # -----------------------------------------------------

    st.write(
        "**Customer:**",
        test_customer
    )

    st.write(
        "**Amount:**",
        f"₹{test_amount:,.0f}"
    )

    st.write(
        "**Diagnosis:**",
        test_diagnosis
    )

    st.write(
        "**Confidence:**",
        f"{test_confidence:.1f}%"
    )

    st.write(
        "**Risk Level:**",
        test_risk_level
    )

    st.write(
        "**Risk Score:**",
        test_risk_score
    )


    # -----------------------------------------------------
    # SAFETY CHECKS
    # -----------------------------------------------------

    st.markdown("### 📋 Safety Checks")

    for reason in test_safety_reasons:

        st.write(
            "•",
            reason
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "PayRecover AI | Synthetic payment data | "
    "AI recommendations are controlled by deterministic "
    "safety rules | No real payments are processed"
)