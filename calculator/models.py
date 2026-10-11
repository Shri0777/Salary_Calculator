from django.db import models
from decimal import Decimal


class SalaryCalculation(models.Model):
    """
    Model to store salary calculation history.

    This model captures a snapshot of salary inputs and calculated results
    at a point in time. Historical records remain unchanged even if the
    calculation logic is updated in future versions.
    """

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when this calculation was created"
    )
    label = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Optional descriptive label for this calculation",
    )

    # Input values - Earnings
    basic_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Monthly basic salary",
    )
    hra = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="House Rent Allowance",
    )
    other_allowances = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Other monthly allowances",
    )
    bonus_overtime = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Bonus and overtime pay",
    )

    # Input values - Deductions
    pf_deduction = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Provident Fund deduction",
    )
    professional_tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Professional tax deduction",
    )
    income_tax_estimate = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Estimated income tax deduction",
    )
    other_deductions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Other deductions",
    )

    # Calculated values (snapshot)
    gross_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Calculated gross salary (snapshot)",
    )
    total_deductions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Calculated total deductions (snapshot)",
    )
    net_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Calculated net salary (snapshot)",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Salary Calculation"
        verbose_name_plural = "Salary Calculations"

    def __str__(self):
        """Return a readable string representation."""
        if self.label:
            return f"{self.label} - ₹{self.net_salary} (created {self.created_at.strftime('%Y-%m-%d')})"
        return f"Salary Calculation - ₹{self.net_salary} (created {self.created_at.strftime('%Y-%m-%d')})"

