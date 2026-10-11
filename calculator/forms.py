"""
Django forms for salary calculation input.

This module provides form validation for salary-related inputs
using Decimal fields for precise monetary calculations.
"""

from decimal import Decimal, InvalidOperation
from django import forms


class SalaryCalculatorForm(forms.Form):
    """
    Form for entering salary calculation inputs.

    All monetary fields use DecimalField with validation to ensure:
    - Non-negative values
    - Maximum 2 decimal places
    - Reasonable maximum values to prevent overflow
    - Server-side validation as the source of truth
    """

    # Earnings
    basic_salary = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        max_value=Decimal("9999999999.99"),
        required=True,
        label="Basic Salary",
        help_text="Monthly basic salary (required)",
        widget=forms.NumberInput(
            attrs={
                "step": "0.01",
                "min": "0",
                "placeholder": "25000.00",
                "class": "form-control",
            }
        ),
    )

    hra = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        max_value=Decimal("9999999999.99"),
        required=False,
        label="House Rent Allowance (HRA)",
        help_text="Monthly HRA (optional)",
        widget=forms.NumberInput(
            attrs={
                "step": "0.01",
                "min": "0",
                "placeholder": "0.00",
                "class": "form-control",
            }
        ),
    )

    other_allowances = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        max_value=Decimal("9999999999.99"),
        required=False,
        label="Other Allowances",
        help_text="Other monthly allowances (optional)",
        widget=forms.NumberInput(
            attrs={
                "step": "0.01",
                "min": "0",
                "placeholder": "0.00",
                "class": "form-control",
            }
        ),
    )

    bonus_overtime = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        max_value=Decimal("9999999999.99"),
        required=False,
        label="Bonus & Overtime",
        help_text="Bonus and overtime pay (optional)",
        widget=forms.NumberInput(
            attrs={
                "step": "0.01",
                "min": "0",
                "placeholder": "0.00",
                "class": "form-control",
            }
        ),
    )

    # Deductions
    pf_deduction = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        max_value=Decimal("9999999999.99"),
        required=False,
        label="PF Deduction",
        help_text="Provident Fund deduction (optional)",
        widget=forms.NumberInput(
            attrs={
                "step": "0.01",
                "min": "0",
                "placeholder": "0.00",
                "class": "form-control",
            }
        ),
    )

    professional_tax = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        max_value=Decimal("9999999999.99"),
        required=False,
        label="Professional Tax",
        help_text="Professional tax deduction (optional)",
        widget=forms.NumberInput(
            attrs={
                "step": "0.01",
                "min": "0",
                "placeholder": "0.00",
                "class": "form-control",
            }
        ),
    )

    income_tax_estimate = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        max_value=Decimal("9999999999.99"),
        required=False,
        label="Income Tax Estimate",
        help_text="Estimated income tax deduction (optional)",
        widget=forms.NumberInput(
            attrs={
                "step": "0.01",
                "min": "0",
                "placeholder": "0.00",
                "class": "form-control",
            }
        ),
    )

    other_deductions = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        max_value=Decimal("9999999999.99"),
        required=False,
        label="Other Deductions",
        help_text="Other deductions (optional)",
        widget=forms.NumberInput(
            attrs={
                "step": "0.01",
                "min": "0",
                "placeholder": "0.00",
                "class": "form-control",
            }
        ),
    )

    def clean(self):
        """
        Normalize optional fields to Decimal('0.00') when blank.

        This ensures that blank optional inputs are treated as zero
        in calculations rather than causing errors.
        """
        cleaned_data = super().clean()

        # List of optional fields that should default to zero
        optional_fields = [
            "hra",
            "other_allowances",
            "bonus_overtime",
            "pf_deduction",
            "professional_tax",
            "income_tax_estimate",
            "other_deductions",
        ]

        # Normalize blank optional fields to Decimal('0.00')
        for field in optional_fields:
            if cleaned_data.get(field) is None:
                cleaned_data[field] = Decimal("0.00")

        return cleaned_data

    def clean_basic_salary(self):
        """Validate basic salary is provided and positive."""
        basic_salary = self.cleaned_data.get("basic_salary")
        if basic_salary is None:
            raise forms.ValidationError("Basic salary is required.")
        if basic_salary < 0:
            raise forms.ValidationError("Basic salary cannot be negative.")
        return basic_salary
