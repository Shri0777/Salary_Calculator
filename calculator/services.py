"""
Salary calculation business logic.

This module provides the core salary calculation functionality
using Decimal arithmetic for precise monetary calculations.
"""

from decimal import Decimal
from typing import Dict, Any


def calculate_salary(
    basic_salary: Decimal,
    hra: Decimal = Decimal("0.00"),
    other_allowances: Decimal = Decimal("0.00"),
    bonus_overtime: Decimal = Decimal("0.00"),
    pf_deduction: Decimal = Decimal("0.00"),
    professional_tax: Decimal = Decimal("0.00"),
    income_tax_estimate: Decimal = Decimal("0.00"),
    other_deductions: Decimal = Decimal("0.00"),
) -> Dict[str, Any]:
    """
    Calculate salary components including gross, net, and annualized estimates.

    This function performs precise decimal arithmetic on salary components
    and returns a comprehensive breakdown of the calculation.

    Args:
        basic_salary: Base monthly salary (required)
        hra: House Rent Allowance
        other_allowances: Other monthly allowances
        bonus_overtime: Bonus and overtime pay
        pf_deduction: Provident Fund deduction
        professional_tax: Professional tax deduction
        income_tax_estimate: Estimated income tax deduction
        other_deductions: Other deductions

    Returns:
        A dictionary containing:
            - All input values (normalized)
            - gross_salary: Sum of all earnings
            - total_deductions: Sum of all deductions
            - net_salary: Gross minus deductions
            - annualized_gross: Gross salary * 12
            - annualized_net: Net salary * 12
            - is_negative: True if net salary is negative
    """
    # Ensure all inputs are Decimal
    basic_salary = Decimal(str(basic_salary))
    hra = Decimal(str(hra))
    other_allowances = Decimal(str(other_allowances))
    bonus_overtime = Decimal(str(bonus_overtime))
    pf_deduction = Decimal(str(pf_deduction))
    professional_tax = Decimal(str(professional_tax))
    income_tax_estimate = Decimal(str(income_tax_estimate))
    other_deductions = Decimal(str(other_deductions))

    # Calculate gross salary
    gross_salary = basic_salary + hra + other_allowances + bonus_overtime

    # Calculate total deductions
    total_deductions = (
        pf_deduction + professional_tax + income_tax_estimate + other_deductions
    )

    # Calculate net salary
    net_salary = gross_salary - total_deductions

    # Calculate annualized estimates (assuming same monthly structure)
    annualized_gross = gross_salary * 12
    annualized_net = net_salary * 12

    # Check if net salary is negative
    is_negative = net_salary < 0

    # Normalize to 2 decimal places
    def normalize(value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"))

    return {
        # Input values (normalized)
        "basic_salary": normalize(basic_salary),
        "hra": normalize(hra),
        "other_allowances": normalize(other_allowances),
        "bonus_overtime": normalize(bonus_overtime),
        "pf_deduction": normalize(pf_deduction),
        "professional_tax": normalize(professional_tax),
        "income_tax_estimate": normalize(income_tax_estimate),
        "other_deductions": normalize(other_deductions),
        # Calculated values
        "gross_salary": normalize(gross_salary),
        "total_deductions": normalize(total_deductions),
        "net_salary": normalize(net_salary),
        "annualized_gross": normalize(annualized_gross),
        "annualized_net": normalize(annualized_net),
        "is_negative": is_negative,
    }
