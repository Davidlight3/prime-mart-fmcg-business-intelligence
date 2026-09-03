"""
=========================================================
PrimeMart FMCG Analytics Platform
Business Validation Utilities
=========================================================
"""

from __future__ import annotations

import pandas as pd


def validate_employee_roles(
    df: pd.DataFrame,
    employees: pd.DataFrame,
    eligible_titles: list[str],
    employee_column: str = "EmployeeID",
) -> None:
    """
    Ensure only authorized employees appear
    in a fact table.
    """

    employee_title = (
        employees
        .set_index("EmployeeID")["JobTitle"]
    )

    invalid = (
        ~df[employee_column]
        .map(employee_title)
        .isin(eligible_titles)
    )

    if invalid.any():

        raise ValueError(
            "Unauthorized employee found."
        )


def log_negative_profit(
    df: pd.DataFrame,
    logger,
) -> None:
    """
    Log the number of
    loss-making transactions.
    """

    negative_profit = (
        df["ProfitAmount"] < 0
    ).sum()

    logger.info(
        f"Negative Profit Transactions : "
        f"{negative_profit:,}"
    )

    logger.info(
        f"Negative Profit Rate : "
        f"{negative_profit / len(df) * 100:.2f}%"
    )