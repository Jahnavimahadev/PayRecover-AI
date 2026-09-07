"""
PayRecover AI - Deterministic Safety Engine

Gemini recommends.
This module decides whether the recommendation
is safe to execute.

IMPORTANT:
- No real payments are processed.
- All data is synthetic.
- Safety decisions are deterministic.
- AI never directly executes a payment.
"""


# =========================================================
# ALLOWED ACTIONS
# =========================================================

ALLOWED_ACTIONS = {
    "RETRY",
    "REMINDER",
    "UPDATE PAYMENT METHOD",
    "ESCALATE"
}


# =========================================================
# MAIN SAFETY EVALUATION
# =========================================================

def evaluate_action(
    recommended_action,
    amount,
    previous_attempts,
    payment_status="failed"
):
    """
    Evaluate an AI recommendation using deterministic
    financial safety rules.

    Returns:

        final_action
        safety_status
        safety_reasons
        risk_level
        risk_score
    """

    # -----------------------------------------------------
    # NORMALIZE INPUTS
    # -----------------------------------------------------

    action = str(
        recommended_action
    ).upper().strip()

    amount = float(amount)

    previous_attempts = int(
        previous_attempts
    )

    payment_status = str(
        payment_status
    ).lower().strip()


    reasons = []

    risk_score = 0


    # =====================================================
    # RULE 1 — INVALID AI OUTPUT
    # =====================================================

    if action not in ALLOWED_ACTIONS:

        return (
            "ESCALATE",
            "BLOCKED",
            [
                "RULE 1: Unknown AI action.",
                "Automatic recovery blocked.",
                "Manual review required."
            ],
            "HIGH",
            100
        )


    # =====================================================
    # RULE 2 — PAYMENT STATUS VERIFICATION
    # =====================================================

    if payment_status != "failed":

        return (
            "ESCALATE",
            "BLOCKED",
            [
                "RULE 2: Payment status is not confirmed "
                "as failed.",
                "Recovery action blocked until payment "
                "status is verified."
            ],
            "HIGH",
            100
        )


    # =====================================================
    # RULE 3 — RETRY LIMIT PROTECTION
    # =====================================================

    if previous_attempts >= 2:

        risk_score += 50

        reasons.append(
            "RULE 3: Retry limit protection triggered."
        )

        reasons.append(
            f"Previous retry attempts: {previous_attempts}."
        )

        reasons.append(
            "Further automatic retries are blocked."
        )

        # Any retry recommendation must be stopped.

        if action == "RETRY":

            return (
                "ESCALATE",
                "BLOCKED",
                reasons,
                "HIGH",
                risk_score
            )


    # =====================================================
    # RULE 4 — HIGH-VALUE TRANSACTION PROTECTION
    # =====================================================

    if amount >= 20000:

        risk_score += 30

        reasons.append(
            "RULE 4: High-value transaction protection triggered."
        )

        reasons.append(
            f"Transaction amount: ₹{amount:,.0f}."
        )

        reasons.append(
            "Additional review is required before automatic retry."
        )

        if action == "RETRY":

            return (
                "ESCALATE",
                "BLOCKED",
                reasons,
                "HIGH",
                min(risk_score + 20, 100)
            )


    # =====================================================
    # RULE 5 — RETRY IDEMPOTENCY PROTECTION
    # =====================================================

    if action == "RETRY":

        risk_score += 20

        reasons.append(
            "RULE 5: Retry requires transaction-status "
            "verification."
        )

        reasons.append(
            "Idempotency protection is required to reduce "
            "duplicate-charge risk."
        )


    # =====================================================
    # RULE 6 — CUSTOMER INTERVENTION
    # =====================================================

    if action in {
        "REMINDER",
        "UPDATE PAYMENT METHOD"
    }:

        risk_score += 10

        reasons.append(
            "RULE 6: Customer intervention may be required."
        )


    # =====================================================
    # RULE 7 — EXPLICIT ESCALATION
    # =====================================================

    if action == "ESCALATE":

        reasons.append(
            "RULE 7: Escalation selected."
        )

        reasons.append(
            "Automatic recovery stopped."
        )

        return (
            "ESCALATE",
            "SAFE",
            reasons,
            "LOW",
            min(risk_score, 100)
        )


    # =====================================================
    # FINAL RISK CLASSIFICATION
    # =====================================================

    if risk_score >= 60:

        risk_level = "HIGH"

    elif risk_score >= 30:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"


    # =====================================================
    # APPROVED ACTION
    # =====================================================

    reasons.append(
        "All deterministic safety checks passed."
    )

    return (
        action,
        "APPROVED",
        reasons,
        risk_level,
        min(risk_score, 100)
    )