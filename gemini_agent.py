"""
PayRecover AI - Gemini Agent

Gemini recommends.
The deterministic safety engine controls the final action.

If Gemini is unavailable because of quota, network failure,
or an invalid response, a clearly labelled local fallback
analysis is used.

IMPORTANT:
- Synthetic/demo data only.
- No real payments are processed.
- Fallback analysis is NOT presented as Gemini output.
"""

import os
import json

from google import genai

from safety_engine import evaluate_action


# ---------------------------------------------------------
# GEMINI CLIENT
# ---------------------------------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please check your Windows environment variable."
    )

client = genai.Client(
    api_key=api_key
)


# ---------------------------------------------------------
# ALLOWED ACTIONS
# ---------------------------------------------------------

ALLOWED_ACTIONS = {
    "RETRY",
    "REMINDER",
    "UPDATE PAYMENT METHOD",
    "ESCALATE"
}


# ---------------------------------------------------------
# LOCAL FALLBACK ANALYSIS
# ---------------------------------------------------------

def local_fallback_analysis(
    payment_description,
    amount,
    previous_attempts
):
    """
    Deterministic local fallback used when Gemini is
    unavailable.

    This is NOT a Gemini-generated response.

    It is intentionally simple, transparent and bounded.
    """

    text = str(
        payment_description
    ).lower()


    # -----------------------------------------------------
    # TEMPORARY / INFRASTRUCTURE FAILURE
    # -----------------------------------------------------

    temporary_keywords = [
        "temporary",
        "temporarily",
        "timeout",
        "timed out",
        "network",
        "gateway",
        "server unavailable",
        "service unavailable",
        "currently unavailable",
        "bank server",
        "bank service",
        "payment gateway",
        "connection"
    ]

    if any(
        keyword in text
        for keyword in temporary_keywords
    ):

        failure_reason = (
            "Temporary payment infrastructure failure"
        )

        if previous_attempts >= 2:

            action = "ESCALATE"

            reason = (
                "The failure appears temporary, but the "
                "retry history is already high. Further "
                "automatic retries should be stopped."
            )

        else:

            action = "RETRY"

            reason = (
                "The failure appears temporary and the "
                "retry history is still within the controlled "
                "recovery range."
            )

        return {
            "failure_reason":
                failure_reason,

            "confidence":
                82,

            "recommended_action":
                action,

            "reason":
                reason,

            "safety_concern":
                (
                    "Verify payment status and use "
                    "idempotency protection before any retry."
                ),

            "analysis_source":
                "LOCAL FALLBACK"
        }


    # -----------------------------------------------------
    # INSUFFICIENT FUNDS
    # -----------------------------------------------------

    insufficient_keywords = [
        "insufficient",
        "not enough",
        "balance is too low",
        "does not have enough",
        "funds",
        "low balance"
    ]

    if any(
        keyword in text
        for keyword in insufficient_keywords
    ):

        return {
            "failure_reason":
                "Insufficient customer funds",

            "confidence":
                88,

            "recommended_action":
                "REMINDER",

            "reason":
                (
                    "The payment cannot reasonably be "
                    "retried until sufficient funds are available."
                ),

            "safety_concern":
                (
                    "Repeated retries may fail without "
                    "customer action."
                ),

            "analysis_source":
                "LOCAL FALLBACK"
        }


    # -----------------------------------------------------
    # EXPIRED PAYMENT METHOD
    # -----------------------------------------------------

    expired_keywords = [
        "expired card",
        "card has expired",
        "credit card has expired",
        "debit card has expired",
        "expired",
        "payment method expired"
    ]

    if any(
        keyword in text
        for keyword in expired_keywords
    ):

        return {
            "failure_reason":
                "Expired payment method",

            "confidence":
                94,

            "recommended_action":
                "UPDATE PAYMENT METHOD",

            "reason":
                (
                    "The payment method appears to be "
                    "expired and requires customer intervention."
                ),

            "safety_concern":
                (
                    "Do not repeatedly retry an expired "
                    "payment method."
                ),

            "analysis_source":
                "LOCAL FALLBACK"
        }


    # -----------------------------------------------------
    # UNKNOWN FAILURE
    # -----------------------------------------------------

    return {
        "failure_reason":
            "Unclassified payment failure",

        "confidence":
            45,

        "recommended_action":
            "ESCALATE",

        "reason":
            (
                "The failure could not be confidently "
                "classified using the local fallback rules."
            ),

        "safety_concern":
            (
                "Manual investigation is safer than "
                "automatic recovery."
            ),

        "analysis_source":
            "LOCAL FALLBACK"
    }


# ---------------------------------------------------------
# GEMINI ANALYSIS
# ---------------------------------------------------------

def ask_gemini(
    payment_description,
    amount,
    previous_attempts
):
    """
    Ask Gemini to diagnose a failed payment.

    If Gemini is unavailable, safely use the local fallback.

    Gemini only recommends an action.
    It never executes the payment.
    """

    prompt = f"""
You are PayRecover AI, an intelligent revenue recovery agent.

Analyze this failed payment:

Payment failure:
{payment_description}

Payment amount:
₹{amount}

Previous retry attempts:
{previous_attempts}

Your task is to diagnose the failure and recommend ONE
appropriate recovery action.

Allowed actions:

RETRY
REMINDER
UPDATE PAYMENT METHOD
ESCALATE

Consider:

1. Likely cause of the failure.
2. Whether the failure appears temporary or persistent.
3. Number of previous retry attempts.
4. Payment amount.
5. Risk of duplicate charging.
6. Whether customer intervention is required.
7. Whether the situation should be escalated.

Important safety requirements:

- Never claim that a real payment was processed.
- This is synthetic demonstration data.
- Gemini only recommends an action.
- A separate deterministic safety engine makes the
  final authorization decision.
- If uncertain or potentially unsafe, recommend ESCALATE.
- Do not invent customer information.
- Do not expose payment credentials.

Return ONLY valid JSON in exactly this structure:

{{
    "failure_reason": "short diagnosis",
    "confidence": 0,
    "recommended_action": "RETRY",
    "reason": "why this action was recommended",
    "safety_concern": "main risk to consider"
}}

Confidence must be a number from 0 to 100.

The recommended_action MUST be exactly one of:

RETRY
REMINDER
UPDATE PAYMENT METHOD
ESCALATE
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        text = response.text

        if not text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        text = text.strip()


        # Remove Markdown code fences if Gemini returns them

        if text.startswith("```"):

            text = text.replace(
                "```json",
                ""
            )

            text = text.replace(
                "```",
                ""
            )

            text = text.strip()


        result = json.loads(
            text
        )


        # -------------------------------------------------
        # VALIDATE REQUIRED FIELDS
        # -------------------------------------------------

        required_fields = [
            "failure_reason",
            "confidence",
            "recommended_action",
            "reason",
            "safety_concern"
        ]

        for field in required_fields:

            if field not in result:

                raise ValueError(
                    f"Gemini response is missing field: {field}"
                )


        # -------------------------------------------------
        # VALIDATE ACTION
        # -------------------------------------------------

        action = str(
            result["recommended_action"]
        ).upper().strip()

        result[
            "recommended_action"
        ] = action

        if action not in ALLOWED_ACTIONS:

            raise ValueError(
                f"Invalid Gemini action: {action}"
            )


        # -------------------------------------------------
        # VALIDATE CONFIDENCE
        # -------------------------------------------------

        try:

            confidence = float(
                result["confidence"]
            )

        except (
            TypeError,
            ValueError
        ):

            confidence = 0

        confidence = max(
            0,
            min(100, confidence)
        )

        result[
            "confidence"
        ] = confidence


        # -------------------------------------------------
        # SOURCE TRANSPARENCY
        # -------------------------------------------------

        result[
            "analysis_source"
        ] = "GEMINI"


        return result


    # -----------------------------------------------------
    # GEMINI FAILURE → LOCAL FALLBACK
    # -----------------------------------------------------

    except Exception as error:

        fallback = local_fallback_analysis(
            payment_description,
            amount,
            previous_attempts
        )

        fallback[
            "fallback_reason"
        ] = str(error)

        return fallback


# ---------------------------------------------------------
# SAFETY ENGINE WRAPPER
# ---------------------------------------------------------

def apply_safety_rules(
    recommended_action,
    previous_attempts,
    amount,
    payment_status="failed"
):
    """
    Compatibility wrapper for the application.

    The actual safety decision is performed by
    safety_engine.py.
    """

    (
        final_action,
        safety_status,
        safety_reasons,
        risk_level,
        risk_score
    ) = evaluate_action(
        recommended_action,
        amount,
        previous_attempts,
        payment_status
    )

    explanation = (
        f"Status: {safety_status} | "
        f"Risk: {risk_level} ({risk_score}/100) | "
        f"{' '.join(safety_reasons)}"
    )

    return (
        final_action,
        explanation
    )