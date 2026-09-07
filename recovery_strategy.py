"""
PayRecover AI - Recovery Strategy Engine

The strategy engine recommends a candidate action.
The deterministic safety engine decides whether that
candidate action is actually allowed.

IMPORTANT:
- No real payments are processed.
- All data is synthetic.
- Strategy recommendation is NOT authorization.
- Safety engine has final control.
"""

ALLOWED_STRATEGIES = {
    "RETRY",
    "REMINDER",
    "UPDATE PAYMENT METHOD",
    "ESCALATE"
}


def recommend_recovery_strategy(
    failure_reason,
    failure_description,
    amount,
    previous_attempts,
    risk_level="LOW",
    confidence=80,
    historical_success_rate=None
):

    reason = str(
        failure_reason
    ).lower().strip()

    description = str(
        failure_description
    ).lower().strip()

    text = reason + " " + description

    amount = float(amount)

    previous_attempts = int(
        previous_attempts
    )

    risk_level = str(
        risk_level
    ).upper().strip()

    confidence = float(
        confidence
    )

    # -----------------------------------------------------
    # DEFAULT VALUES
    # -----------------------------------------------------

    strategy = "ESCALATE"

    score = 50

    priority = "MEDIUM"

    customer_action_required = False

    retryable = False

    reasons = []

    # -----------------------------------------------------
    # TEMPORARY / NETWORK / GATEWAY FAILURE
    # -----------------------------------------------------

    if any(
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
            "connection",
            "bank server",
            "bank service",
            "payment gateway"
        ]
    ):

        # IMPORTANT:
        # Keep RETRY as the candidate strategy.
        # The safety engine will block it when
        # the retry limit has been reached.

        strategy = "RETRY"

        retryable = (
            previous_attempts < 2
        )

        score += 20

        reasons.append(
            "Failure appears temporary or infrastructure-related."
        )

        reasons.append(
            "A controlled retry may recover the payment."
        )

        # -------------------------------------------------
        # RETRY LIMIT INFORMATION
        # -------------------------------------------------

        if previous_attempts == 0:

            score += 15

            priority = "HIGH"

            reasons.append(
                "No previous retry attempt has been made."
            )

        elif previous_attempts == 1:

            score += 5

            priority = "MEDIUM"

            reasons.append(
                "One previous retry attempt exists."
            )

        elif previous_attempts >= 2:

            priority = "HIGH"

            reasons.append(
                f"Retry limit reached: {previous_attempts} previous attempts."
            )

            reasons.append(
                "RETRY remains the candidate action so the safety engine can enforce the retry limit."
            )

    # -----------------------------------------------------
    # INSUFFICIENT FUNDS
    # -----------------------------------------------------

    elif any(
        keyword in text
        for keyword in [
            "insufficient",
            "not enough",
            "low balance",
            "balance is too low",
            "does not have enough"
        ]
    ):

        strategy = "REMINDER"

        customer_action_required = True

        score += 10

        priority = "MEDIUM"

        reasons.append(
            "Payment failure appears related to insufficient funds."
        )

        reasons.append(
            "Customer action may be required before another payment attempt."
        )

    # -----------------------------------------------------
    # EXPIRED PAYMENT METHOD
    # -----------------------------------------------------

    elif any(
        keyword in text
        for keyword in [
            "expired",
            "expiry",
            "expiration",
            "card has expired"
        ]
    ):

        strategy = "UPDATE PAYMENT METHOD"

        customer_action_required = True

        score += 15

        priority = "HIGH"

        reasons.append(
            "Payment method appears to be expired."
        )

        reasons.append(
            "Customer should update the payment method."
        )

    # -----------------------------------------------------
    # UNKNOWN FAILURE
    # -----------------------------------------------------

    else:

        strategy = "ESCALATE"

        score -= 10

        priority = "HIGH"

        reasons.append(
            "Failure reason is not confidently classified."
        )

        reasons.append(
            "Manual investigation is recommended."
        )

    # -----------------------------------------------------
    # HIGH VALUE TRANSACTION
    # -----------------------------------------------------

    if amount >= 20000:

        score += 5

        reasons.append(
            f"High-value transaction detected: ₹{amount:,.0f}."
        )

        if strategy == "RETRY":

            priority = "HIGH"

            reasons.append(
                "High-value retry requires additional caution."
            )

    # -----------------------------------------------------
    # RISK LEVEL
    # -----------------------------------------------------

    if risk_level == "HIGH":

        score -= 15

        priority = "HIGH"

        reasons.append(
            "High risk level detected."
        )

        if strategy == "RETRY":

            strategy = "ESCALATE"

            retryable = False

            reasons.append(
                "Automatic retry replaced with escalation because of high risk."
            )

    elif risk_level == "MEDIUM":

        score -= 5

        reasons.append(
            "Medium risk level detected."
        )

    # -----------------------------------------------------
    # CONFIDENCE
    # -----------------------------------------------------

    if confidence >= 85:

        score += 5

        reasons.append(
            "High analysis confidence supports the recommendation."
        )

    elif confidence < 50:

        score -= 10

        reasons.append(
            "Low analysis confidence increases uncertainty."
        )

        if strategy == "RETRY":

            strategy = "ESCALATE"

            retryable = False

            priority = "HIGH"

            reasons.append(
                "Low-confidence retry recommendation escalated for safety."
            )

    # -----------------------------------------------------
    # HISTORICAL PERFORMANCE
    # -----------------------------------------------------

    if historical_success_rate is not None:

        historical_success_rate = float(
            historical_success_rate
        )

        if historical_success_rate >= 70:

            score += 10

            reasons.append(
                "Historical synthetic results show strong performance for this strategy."
            )

        elif historical_success_rate < 30:

            score -= 10

            reasons.append(
                "Historical synthetic results show weak performance for this strategy."
            )

    # -----------------------------------------------------
    # SCORE LIMIT
    # -----------------------------------------------------

    score = max(
        0,
        min(
            int(score),
            100
        )
    )

    # -----------------------------------------------------
    # PRIORITY
    # -----------------------------------------------------

    if score >= 75:

        priority = "HIGH"

    elif score >= 50:

        if priority != "HIGH":
            priority = "MEDIUM"

    else:

        if priority != "HIGH":
            priority = "LOW"

    # -----------------------------------------------------
    # VALIDATE STRATEGY
    # -----------------------------------------------------

    if strategy not in ALLOWED_STRATEGIES:

        strategy = "ESCALATE"

        retryable = False

        priority = "HIGH"

        reasons.append(
            "Invalid strategy detected; defaulting to escalation."
        )

    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    return {

        "strategy":
            strategy,

        "priority":
            priority,

        "score":
            score,

        "reason":
            " ".join(reasons),

        "customer_action_required":
            customer_action_required,

        "retryable":
            retryable
    }