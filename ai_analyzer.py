"""
PayRecover AI - AI Analysis Engine

Combines:
1. Gemini AI / Local Fallback
2. Recovery Strategy Engine
3. Deterministic Safety Engine
4. Recovery Simulation

IMPORTANT:
- All payment data is synthetic.
- No real payments are processed.
- AI recommends actions.
- Safety rules control final authorization.
"""

import pandas as pd

from gemini_agent import ask_gemini
from safety_engine import evaluate_action
from recovery_strategy import recommend_recovery_strategy


# =========================================================
# RECOVERY SIMULATION
# =========================================================

def simulate_recovery(payment_id, action, amount):

    recovery_rates = {
        "RETRY": 0.70,
        "REMINDER": 0.50,
        "UPDATE PAYMENT METHOD": 0.60,
        "ESCALATE": 0.00
    }

    rate = recovery_rates.get(action, 0.00)

    try:
        payment_number = int(str(payment_id)[1:])
    except Exception:
        payment_number = 0

    recovered = (
        payment_number % 10
    ) < (
        rate * 10
    )

    if recovered:
        return "RECOVERED", float(amount)

    return "NOT RECOVERED", 0.0


# =========================================================
# OPPORTUNITY SCORE
# =========================================================

def calculate_opportunity_score(
    failure_reason,
    failure_description,
    amount,
    previous_attempts,
    risk_level,
    confidence
):

    text = (
        str(failure_reason)
        + " "
        + str(failure_description)
    ).lower()

    score = 50

    retry_keywords = [
        "temporary",
        "temporarily",
        "network",
        "gateway",
        "server",
        "timeout",
        "timed out",
        "service unavailable"
    ]

    if any(
        keyword in text
        for keyword in retry_keywords
    ):
        score += 20

    if previous_attempts == 0:
        score += 15

    elif previous_attempts == 1:
        score += 8

    elif previous_attempts >= 2:
        score -= 15

    if float(amount) >= 20000:
        score += 5

    if risk_level == "HIGH":
        score -= 25

    elif risk_level == "MEDIUM":
        score -= 10

    if float(confidence) >= 80:
        score += 5

    elif float(confidence) < 50:
        score -= 5

    return max(
        0,
        min(
            int(score),
            100
        )
    )


# =========================================================
# PROCESS ONE PAYMENT
# =========================================================

def process_payment(row, category_analysis):

    payment_id = row["payment_id"]

    customer = row["customer"]

    amount = float(row["amount"])

    failure_reason = row["failure_reason"]

    failure_description = row[
        "failure_description"
    ]

    previous_attempts = int(
        row["previous_attempts"]
    )

    payment_status = row.get(
        "status",
        "failed"
    )

    # =====================================================
    # AI ANALYSIS
    # =====================================================

    analysis = category_analysis

    source = analysis.get(
        "analysis_source",
        analysis.get(
            "source",
            "UNKNOWN"
        )
    )

    fallback_reason = analysis.get(
        "fallback_reason",
        ""
    )

    diagnosis = analysis.get(
        "failure_reason",
        analysis.get(
            "diagnosis",
            "Unknown payment failure"
        )
    )

    confidence = float(
        analysis.get(
            "confidence",
            50
        )
    )

    ai_reason = analysis.get(
        "reason",
        ""
    )

    safety_concern = analysis.get(
        "safety_concern",
        ""
    )

    ai_recommendation = analysis.get(
        "recommended_action",
        "ESCALATE"
    )

    # =====================================================
    # RECOVERY STRATEGY
    # =====================================================

    strategy_result = recommend_recovery_strategy(
        failure_reason=failure_reason,
        failure_description=failure_description,
        amount=amount,
        previous_attempts=previous_attempts,
        risk_level="LOW",
        confidence=confidence
    )

    strategy = strategy_result["strategy"]

    strategy_priority = strategy_result[
        "priority"
    ]

    strategy_score = strategy_result[
        "score"
    ]

    strategy_reason = strategy_result[
        "reason"
    ]

    customer_action_required = (
        strategy_result[
            "customer_action_required"
        ]
    )

    retryable = strategy_result[
        "retryable"
    ]

    # =====================================================
    # SAFETY CANDIDATE
    # =====================================================
    #
    # For temporary failures with 2+ previous attempts,
    # deliberately send RETRY to the safety engine.
    #
    # The safety engine must then block it.
    #

    text = (
        str(failure_reason)
        + " "
        + str(failure_description)
    ).lower()

    retry_failure = any(
        keyword in text
        for keyword in [
            "temporary",
            "temporarily",
            "timeout",
            "timed out",
            "network",
            "gateway",
            "server unavailable",
            "service unavailable",
            "connection"
        ]
    )

    safety_recommended_action = strategy

    if (
        retry_failure
        and previous_attempts >= 2
    ):
        safety_recommended_action = "RETRY"

    # =====================================================
    # DETERMINISTIC SAFETY ENGINE
    # =====================================================

    try:

        (
            final_action,
            safety_status,
            safety_checks,
            risk_level,
            risk_score
        ) = evaluate_action(
            recommended_action=
                safety_recommended_action,

            amount=amount,

            previous_attempts=
                previous_attempts,

            payment_status=
                payment_status
        )

    except Exception as error:

        final_action = "ESCALATE"

        safety_status = "FAIL-SAFE"

        safety_checks = [
            "Safety engine error occurred.",
            "Automatic recovery blocked.",
            "Manual review required."
        ]

        risk_level = "HIGH"

        risk_score = 100

        safety_concern = str(error)

    # =====================================================
    # RECOVERY SIMULATION
    # =====================================================

    outcome, recovered_amount = simulate_recovery(
        payment_id,
        final_action,
        amount
    )

    # =====================================================
    # SAFETY OVERRIDE
    # =====================================================

    safety_override = (
        safety_recommended_action
        != final_action
    )

    # =====================================================
    # OPPORTUNITY SCORE
    # =====================================================

    opportunity_score = calculate_opportunity_score(
        failure_reason=failure_reason,
        failure_description=failure_description,
        amount=amount,
        previous_attempts=previous_attempts,
        risk_level=risk_level,
        confidence=confidence
    )

    # =====================================================
    # FINAL RESULT
    # =====================================================

    return {

        "payment_id":
            payment_id,

        "customer":
            customer,

        "amount":
            amount,

        "failure_reason":
            failure_reason,

        "failure_description":
            failure_description,

        "Previous Attempts":
            previous_attempts,

        "Analysis Source":
            source,

        "Fallback Reason":
            fallback_reason,

        "Diagnosis":
            diagnosis,

        "Confidence":
            confidence,

        "AI Reason":
            ai_reason,

        "AI Safety Concern":
            safety_concern,

        "AI Recommendation":
            ai_recommendation,

        "Recommended Strategy":
            strategy,

        "Strategy Priority":
            strategy_priority,

        "Strategy Score":
            strategy_score,

        "Strategy Reason":
            strategy_reason,

        "Customer Action Required":
            customer_action_required,

        "Retryable":
            retryable,

        "Safety Recommended Action":
            safety_recommended_action,

        "Risk Level":
            risk_level,

        "Risk Score":
            risk_score,

        "Safety Status":
            safety_status,

        "Safety Checks":
            " | ".join(
                safety_checks
            ),

        "Recovery Action":
            final_action,

        "Safety Override":
            safety_override,

        "Outcome":
            outcome,

        "Recovered Amount":
            recovered_amount,

        "Opportunity Score":
            opportunity_score
    }


# =========================================================
# ANALYZE ALL PAYMENTS
# =========================================================

def analyze_payments(
    file_path="payments.csv"
):

    df = pd.read_csv(file_path)

    results = []

    category_analysis = {}

    # =====================================================
    # ANALYZE EACH FAILURE CATEGORY
    # =====================================================

    for failure_reason in (
        df["failure_reason"]
        .dropna()
        .unique()
    ):

        category_rows = df[
            df["failure_reason"]
            == failure_reason
        ]

        first_row = category_rows.iloc[0]

        category_analysis[
            failure_reason
        ] = ask_gemini(

            payment_description=
                first_row[
                    "failure_description"
                ],

            amount=float(
                first_row["amount"]
            ),

            previous_attempts=int(
                first_row[
                    "previous_attempts"
                ]
            )
        )

    # =====================================================
    # PROCESS PAYMENTS
    # =====================================================

    for _, row in df.iterrows():

        failure_reason = row[
            "failure_reason"
        ]

        analysis = category_analysis.get(
            failure_reason
        )

        if analysis is None:

            analysis = {
                "analysis_source":
                    "FAIL-SAFE",

                "fallback_reason":
                    "No analysis available.",

                "failure_reason":
                    "Unknown failure.",

                "confidence":
                    0,

                "reason":
                    "No analysis available.",

                "safety_concern":
                    "Manual review required.",

                "recommended_action":
                    "ESCALATE"
            }

        result = process_payment(
            row,
            analysis
        )

        results.append(result)

    return pd.DataFrame(results)