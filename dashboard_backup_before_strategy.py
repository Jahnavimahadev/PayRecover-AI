"""
PayRecover AI
Intelligent Revenue Recovery Agent

Professional demonstration dashboard.

IMPORTANT:
- Synthetic payment data only.
- No real payments are processed.
- Gemini recommends.
- Deterministic safety engine controls final actions.
- Recovery results are simulated.
"""

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
# CUSTOM STYLING
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .architecture {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #ddd;
        text-align: center;
        font-weight: 600;
        background: #fafafa;
    }

    .source-card {
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #ddd;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🤖 PayRecover AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Intelligent Revenue Recovery Agent'
    '</div>',
    unsafe_allow_html=True
)

st.success(
    "🟢 AI Agent Online — Controlled Recovery Mode"
)


# =========================================================
# ARCHITECTURE
# =========================================================

st.subheader(
    "🏗️ Agent Architecture"
)

st.markdown(
    """
    <div class="architecture">

    Payment Failure
    →
    Gemini AI Diagnosis
    →
    Recovery Recommendation
    →
    Deterministic Safety Engine
    →
    Final Controlled Action
    →
    Recovery Simulation
    →
    Revenue & Audit Tracking

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

try:

    results = analyze_payments()

except Exception as error:

    st.error(
        f"Unable to load PayRecover AI: {error}"
    )

    st.stop()


# =========================================================
# EXECUTIVE METRICS
# =========================================================

st.subheader(
    "📊 Executive Recovery Metrics"
)

total_at_risk = float(
    results["amount"].sum()
)

total_recovered = float(
    results["Recovered Amount"].sum()
)

recovery_rate = (
    total_recovered / total_at_risk * 100
    if total_at_risk > 0
    else 0
)

payments_recovered = int(
    (
        results["Outcome"]
        == "RECOVERED"
    ).sum()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Revenue at Risk",
    f"₹{total_at_risk:,.0f}"
)

col2.metric(
    "💵 Revenue Recovered",
    f"₹{total_recovered:,.0f}"
)

col3.metric(
    "📈 Recovery Rate",
    f"{recovery_rate:.1f}%"
)

col4.metric(
    "✅ Payments Recovered",
    payments_recovered
)


# =========================================================
# SAFETY & RISK
# =========================================================

st.subheader(
    "🛡️ Safety & Risk Controls"
)

escalated = int(
    (
        results["Recovery Action"]
        == "ESCALATE"
    ).sum()
)

amount_escalated = float(
    results.loc[
        results["Recovery Action"]
        == "ESCALATE",
        "amount"
    ].sum()
)

high_risk = int(
    (
        results["Risk Level"]
        == "HIGH"
    ).sum()
)

safety_blocked = int(
    (
        results["Safety Status"]
        == "BLOCKED"
    ).sum()
)

average_confidence = float(
    results["AI Confidence"].mean()
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "🚨 Escalated",
    escalated
)

col2.metric(
    "💸 Amount Escalated",
    f"₹{amount_escalated:,.0f}"
)

col3.metric(
    "🔴 High Risk",
    high_risk
)

col4.metric(
    "🛑 Safety Blocked",
    safety_blocked
)

col5.metric(
    "📊 Avg Analysis Confidence",
    f"{average_confidence:.1f}%"
)


# =========================================================
# ANALYSIS SOURCE TRANSPARENCY
# =========================================================

st.subheader(
    "🔎 Analysis Source Transparency"
)

gemini_count = int(
    (
        results["Analysis Source"]
        == "GEMINI"
    ).sum()
)

fallback_count = int(
    (
        results["Analysis Source"]
        == "LOCAL FALLBACK"
    ).sum()
)

failsafe_count = int(
    (
        results["Analysis Source"]
        == "FAIL-SAFE"
    ).sum()
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "🤖 Gemini",
    gemini_count
)

col2.metric(
    "🟡 Local Fallback",
    fallback_count
)

col3.metric(
    "🔴 Fail-Safe",
    failsafe_count
)


if fallback_count > 0:

    st.info(
        "🟡 Gemini quota/service was unavailable for "
        "some analyses. PayRecover AI used a transparent "
        "local fallback instead of pretending the result "
        "came from Gemini."
    )


if failsafe_count > 0:

    st.warning(
        "🔴 Some records entered fail-safe mode. "
        "Automatic recovery was blocked."
    )


# =========================================================
# ANALYSIS LEGEND
# =========================================================

st.caption(
    "🤖 Gemini = external AI analysis | "
    "🟡 Local Fallback = deterministic backup analysis | "
    "🔴 Fail-Safe = automatic recovery blocked"
)


# =========================================================
# AI INTELLIGENCE
# =========================================================

st.subheader(
    "🧠 AI Intelligence"
)

col1, col2 = st.columns(2)


with col1:

    st.write(
        "**AI Recommendation Distribution**"
    )

    recommendation_counts = (
        results[
            "Gemini Recommendation"
        ]
        .value_counts()
    )

    st.bar_chart(
        recommendation_counts
    )


with col2:

    st.write(
        "**Final Agent Action Distribution**"
    )

    action_counts = (
        results[
            "Recovery Action"
        ]
        .value_counts()
    )

    st.bar_chart(
        action_counts
    )


# =========================================================
# RECOVERY OPPORTUNITY
# =========================================================

st.subheader(
    "🎯 Recovery Opportunity Intelligence"
)

st.write(
    "A transparent 0–100 score used to prioritize "
    "failed payments for controlled recovery."
)

top_opportunities = (
    results[
        [
            "payment_id",
            "customer",
            "amount",
            "Recovery Opportunity Score",
            "Risk Level",
            "Recovery Action",
            "Outcome"
        ]
    ]
    .sort_values(
        "Recovery Opportunity Score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_opportunities,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# RECOVERY OUTCOMES
# =========================================================

st.subheader(
    "💰 Recovery Outcomes"
)

col1, col2 = st.columns(2)


with col1:

    st.write(
        "**Recovery Outcome Distribution**"
    )

    outcome_counts = (
        results["Outcome"]
        .value_counts()
    )

    st.bar_chart(
        outcome_counts
    )


with col2:

    st.write(
        "**Failure Diagnosis Distribution**"
    )

    failure_counts = (
        results["AI Prediction"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(
        failure_counts
    )


# =========================================================
# SINGLE PAYMENT INTELLIGENCE
# =========================================================

st.subheader(
    "🔍 Single Payment Intelligence Console"
)

payment_ids = results[
    "payment_id"
].tolist()

selected_payment_id = st.selectbox(
    "Select a payment to inspect",
    payment_ids
)

selected_payment = results[
    results["payment_id"]
    == selected_payment_id
].iloc[0]


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Payment",
    selected_payment["payment_id"]
)

col2.metric(
    "Amount",
    f"₹{selected_payment['amount']:,.0f}"
)

col3.metric(
    "Opportunity Score",
    selected_payment[
        "Recovery Opportunity Score"
    ]
)

col4.metric(
    "Analysis Confidence",
    f"{selected_payment['AI Confidence']:.0f}%"
)


# =========================================================
# SOURCE DISPLAY
# =========================================================

st.write(
    "**Analysis Source**"
)

if selected_payment[
    "Analysis Source"
] == "GEMINI":

    st.success(
        "🤖 GEMINI"
    )

elif selected_payment[
    "Analysis Source"
] == "LOCAL FALLBACK":

    st.warning(
        "🟡 LOCAL FALLBACK"
    )

else:

    st.error(
        "🔴 FAIL-SAFE"
    )


# =========================================================
# AI DIAGNOSIS
# =========================================================

st.write(
    "### 🤖 Payment Diagnosis"
)

st.write(
    selected_payment[
        "AI Prediction"
    ]
)

st.write(
    "**Analysis reasoning:**"
)

st.info(
    selected_payment[
        "AI Reason"
    ]
)

st.write(
    "**Safety concern:**"
)

st.warning(
    selected_payment[
        "AI Safety Concern"
    ]
)


if selected_payment[
    "Fallback Reason"
]:

    st.caption(
        "Fallback/service detail:"
    )

    st.caption(
        selected_payment[
            "Fallback Reason"
        ]
    )


# =========================================================
# AGENT DECISION PIPELINE
# =========================================================

st.write(
    "### ⚙️ Agent Decision Pipeline"
)

col1, col2, col3 = st.columns(3)


with col1:

    st.write(
        "**AI Recommendation**"
    )

    st.info(
        selected_payment[
            "Gemini Recommendation"
        ]
    )


with col2:

    st.write(
        "**Safety Decision**"
    )

    if selected_payment[
        "Safety Status"
    ] == "BLOCKED":

        st.error(
            "🛑 BLOCKED"
        )

    else:

        st.success(
            "✅ "
            + selected_payment[
                "Safety Status"
            ]
        )


with col3:

    st.write(
        "**Final Agent Action**"
    )

    if selected_payment[
        "Recovery Action"
    ] == "ESCALATE":

        st.warning(
            "🚨 "
            + selected_payment[
                "Recovery Action"
            ]
        )

    else:

        st.success(
            "✅ "
            + selected_payment[
                "Recovery Action"
            ]
        )


# =========================================================
# RISK ASSESSMENT
# =========================================================

st.write(
    "### ⚠️ Risk Assessment"
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Risk Level",
        selected_payment[
            "Risk Level"
        ]
    )

with col2:

    st.metric(
        "Risk Score",
        f"{selected_payment['Risk Score']}/100"
    )


st.write(
    "**Safety checks:**"
)

st.info(
    selected_payment[
        "Safety Checks"
    ]
)


# =========================================================
# RECOVERY RESULT
# =========================================================

st.write(
    "### 💵 Recovery Result"
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Outcome",
        selected_payment[
            "Outcome"
        ]
    )

with col2:

    st.metric(
        "Recovered Amount",
        f"₹{selected_payment['Recovered Amount']:,.0f}"
    )


# =========================================================
# PAYMENT DETAILS
# =========================================================

st.subheader(
    "📋 Payment Recovery Details"
)

display_columns = [
    "payment_id",
    "customer",
    "amount",
    "AI Prediction",
    "AI Confidence",
    "Analysis Source",
    "Gemini Recommendation",
    "previous_attempts",
    "Recovery Opportunity Score",
    "Risk Level",
    "Risk Score",
    "Safety Status",
    "Recovery Action",
    "Outcome",
    "Recovered Amount"
]

st.dataframe(
    results[
        display_columns
    ],
    use_container_width=True,
    hide_index=True
)


# =========================================================
# AUDIT TRAIL
# =========================================================

st.subheader(
    "🧾 Agent Audit Trail"
)

audit_columns = [
    "payment_id",
    "amount",
    "AI Prediction",
    "AI Confidence",
    "Analysis Source",
    "Gemini Recommendation",
    "Recovery Opportunity Score",
    "Risk Level",
    "Risk Score",
    "Safety Status",
    "Safety Checks",
    "Recovery Action",
    "Outcome",
    "Recovered Amount"
]

st.dataframe(
    results[
        audit_columns
    ],
    use_container_width=True,
    hide_index=True
)


# =========================================================
# SAFETY OVERRIDES
# =========================================================

st.subheader(
    "🚨 Safety Overrides"
)

overrides = results[
    results["Gemini Recommendation"]
    != results["Recovery Action"]
]

if len(overrides) == 0:

    st.success(
        "No AI recommendations were changed by "
        "the deterministic safety engine for this batch."
    )

else:

    st.warning(
        f"{len(overrides)} payment(s) had their AI "
        "recommendation changed by safety controls."
    )

    st.dataframe(
        overrides[
            [
                "payment_id",
                "amount",
                "Gemini Recommendation",
                "Risk Level",
                "Risk Score",
                "Safety Status",
                "Safety Checks",
                "Recovery Action"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# RECOVERY SIMULATION
# =========================================================

st.subheader(
    "🔄 Recovery Simulation"
)

st.write(
    "These outcomes are generated by a deterministic "
    "synthetic simulator and do not represent real "
    "payment transactions."
)

st.caption(
    "Simulation rates: RETRY 70% | "
    "REMINDER 50% | "
    "UPDATE PAYMENT METHOD 60% | "
    "ESCALATE 0%"
)


# =========================================================
# DISCLAIMER
# =========================================================

st.markdown("---")

st.caption(
    "🔒 PayRecover AI is a prototype demonstration. "
    "All payment records, recovery results and revenue "
    "figures are synthetic. No real payments are processed. "
    "Gemini provides recommendations while deterministic "
    "safety controls govern final actions."
)