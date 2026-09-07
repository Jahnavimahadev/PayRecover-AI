"""
PayRecover AI - Strategy Performance Engine

Analyzes how each recovery strategy performs
using the synthetic recovery results.

IMPORTANT:
- Results are simulated.
- No real payments are processed.
"""


import pandas as pd


# =========================================================
# STRATEGY PERFORMANCE
# =========================================================

def calculate_strategy_performance(results):
    """
    Calculate performance metrics for every recovery action.

    Returns a DataFrame containing:

    - Strategy
    - Payments
    - Recovered Payments
    - Recovery Rate
    - Revenue at Risk
    - Revenue Recovered
    """

    strategies = [
        "RETRY",
        "REMINDER",
        "UPDATE PAYMENT METHOD",
        "ESCALATE"
    ]

    rows = []

    for strategy in strategies:

        strategy_data = results[
            results["Recovery Action"]
            == strategy
        ]

        payments = len(
            strategy_data
        )

        recovered_payments = int(
            (
                strategy_data["Outcome"]
                == "RECOVERED"
            ).sum()
        )

        revenue_at_risk = float(
            strategy_data["amount"].sum()
        )

        revenue_recovered = float(
            strategy_data[
                "Recovered Amount"
            ].sum()
        )

        if payments > 0:

            recovery_rate = (
                recovered_payments
                / payments
                * 100
            )

        else:

            recovery_rate = 0.0

        rows.append(
            {
                "Strategy": strategy,

                "Payments": payments,

                "Recovered Payments":
                    recovered_payments,

                "Recovery Rate":
                    round(
                        recovery_rate,
                        1
                    ),

                "Revenue at Risk":
                    revenue_at_risk,

                "Revenue Recovered":
                    revenue_recovered
            }
        )

    return pd.DataFrame(
        rows
    )


# =========================================================
# BEST STRATEGY
# =========================================================

def get_best_strategy(
    strategy_results
):
    """
    Identify the strategy with the highest
    recovered revenue.

    Escalation is included for completeness but
    should not normally win because it performs
    no automatic recovery.
    """

    if strategy_results.empty:

        return None

    best_row = strategy_results.loc[
        strategy_results[
            "Revenue Recovered"
        ].idxmax()
    ]

    return {
        "strategy":
            best_row["Strategy"],

        "revenue_recovered":
            best_row["Revenue Recovered"],

        "recovery_rate":
            best_row["Recovery Rate"],

        "payments":
            best_row["Payments"]
    }


# =========================================================
# STRATEGY SUMMARY
# =========================================================

def create_strategy_summary(
    strategy_results
):
    """
    Create a human-readable summary of
    strategy performance.
    """

    best = get_best_strategy(
        strategy_results
    )

    if best is None:

        return (
            "No recovery strategy data is available."
        )

    return (
        f"Best-performing strategy: "
        f"{best['strategy']} | "
        f"Revenue recovered: "
        f"₹{best['revenue_recovered']:,.0f} | "
        f"Recovery rate: "
        f"{best['recovery_rate']:.1f}% | "
        f"Payments handled: "
        f"{best['payments']}"
    )