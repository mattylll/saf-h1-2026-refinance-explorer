"""Illustrative income-capitalisation model from SAF-H1-2026; no lender criteria."""
import math


def calculate(income, yield_pct, debt, cap_pct):
    values = (income, yield_pct, debt, cap_pct)
    if not all(math.isfinite(x) for x in values):
        raise ValueError('Inputs must be finite')
    if income < 0 or yield_pct <= 0 or debt < 0 or not 0 <= cap_pct <= 100:
        raise ValueError('Invalid assumption')
    value = income / (yield_pct / 100)
    capacity = value * cap_pct / 100
    return dict(value=value, capacity=capacity, gap=max(0, debt-capacity),
                headroom=max(0, capacity-debt), ltv=debt/value*100 if value else None)
