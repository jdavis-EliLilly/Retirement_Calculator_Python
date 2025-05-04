"""
retirement.py – Progressive‑tax retirement‐savings projection
Author : James Davis
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple


__all__ = [
    "Bracket",
    "calculate_annual_tax",
    "project_retirement_savings",
]


# ── Tax calculation ────────────────────────────────────────────────────────
@dataclass(frozen=True, slots=True)
class Bracket:
    """A single marginal‑tax bracket."""
    upper: float          # Inclusive upper limit of the bracket (use math.inf for the last)
    rate:  float          # Marginal rate expressed as 0.10 for 10 %


def calculate_annual_tax(income: float, brackets: List[Bracket]) -> float:
    """
    Compute total tax for a progressive system.

    Parameters
    ----------
    income
        Gross annual taxable income.
    brackets
        **Ascending** list of :class:`Bracket` objects.

    Returns
    -------
    float
        Total tax due.
    """
    tax_due, lower = 0.0, 0.0

    for bracket in brackets:
        if income <= lower:                            # nothing left to tax
            break

        taxable = min(income, bracket.upper) - lower   # dollars in this bracket
        tax_due += taxable * bracket.rate
        lower = bracket.upper

    return tax_due


# ── Retirement‑projection logic ────────────────────────────────────────────
def project_retirement_savings(
    *,
    initial_income: float,
    years: int,
    nominal_return: float,
    inflation: float,
    income_growth: float,
    max_401k: float,
    brackets: List[Bracket],
) -> Tuple[float, float]:
    """
    Grow 401(k) + after‑tax savings in real terms.

    All rates are decimals (e.g. 0.05 for 5 %).

    Returns
    -------
    tuple
        (future‑value_401k, future‑value_taxable)
    """
    real_return = nominal_return - inflation
    income      = initial_income
    bal_401k    = 0.0
    bal_taxable = 0.0

    for _ in range(years):
        tax   = calculate_annual_tax(income, brackets)
        net   = income - tax

        # 401(k) – paid from net income in the original logic
        contrib_401k = min(max_401k, net)
        bal_401k     = (bal_401k + contrib_401k) * (1 + real_return)

        # Any surplus goes to an after‑tax account
        surplus       = net - contrib_401k
        bal_taxable   = (bal_taxable + surplus) * (1 + real_return)

        # Next‑year salary bump
        income *= (1 + income_growth)

    return bal_401k, bal_taxable


# ── Example usage ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    BRACKETS_2024 = [
        Bracket(11_600, 0.10),
        Bracket(47_150, 0.12),
        Bracket(100_525, 0.22),
        Bracket(191_950, 0.24),
        Bracket(243_725, 0.32),
        Bracket(609_350, 0.35),
        Bracket(math.inf, 0.37),  # top bracket
    ]

    fv_401k, fv_taxable = project_retirement_savings(
        initial_income = 112_000,
        years          = 20,
        nominal_return = 0.05,
        inflation      = 0.03,
        income_growth  = 0.05,
        max_401k       = 23_000,
        brackets       = BRACKETS_2024,
    )

    print(f"Future 401(k) balance : ${fv_401k:,.0f}")
    print(f"Future taxable stash : ${fv_taxable:,.0f}")
