from django.contrib import admin
from .models import SalaryCalculation


@admin.register(SalaryCalculation)
class SalaryCalculationAdmin(admin.ModelAdmin):
    """Admin interface for SalaryCalculation model."""

    list_display = [
        "label",
        "basic_salary",
        "gross_salary",
        "net_salary",
        "created_at",
    ]
    list_filter = ["created_at"]
    search_fields = ["label"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"
