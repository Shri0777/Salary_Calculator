from decimal import Decimal
from django.test import TestCase
from calculator.services import calculate_salary
from calculator.forms import SalaryCalculatorForm
from calculator.models import SalaryCalculation


class SalaryCalculationServiceTests(TestCase):
    """Test cases for the salary calculation service."""

    def test_gross_salary_calculation(self):
        """Test that gross salary is calculated correctly."""
        result = calculate_salary(
            basic_salary=Decimal("25000.00"),
            hra=Decimal("10000.00"),
            other_allowances=Decimal("5000.00"),
            bonus_overtime=Decimal("0.00"),
        )
        self.assertEqual(result["gross_salary"], Decimal("40000.00"))

    def test_total_deductions_calculation(self):
        """Test that total deductions are calculated correctly."""
        result = calculate_salary(
            basic_salary=Decimal("25000.00"),
            pf_deduction=Decimal("3000.00"),
            professional_tax=Decimal("200.00"),
            income_tax_estimate=Decimal("0.00"),
            other_deductions=Decimal("0.00"),
        )
        self.assertEqual(result["total_deductions"], Decimal("3200.00"))

    def test_net_salary_calculation(self):
        """Test that net salary is calculated correctly."""
        result = calculate_salary(
            basic_salary=Decimal("25000.00"),
            hra=Decimal("10000.00"),
            other_allowances=Decimal("5000.00"),
            bonus_overtime=Decimal("0.00"),
            pf_deduction=Decimal("3000.00"),
            professional_tax=Decimal("200.00"),
            income_tax_estimate=Decimal("0.00"),
            other_deductions=Decimal("0.00"),
        )
        self.assertEqual(result["net_salary"], Decimal("36800.00"))

    def test_annualized_estimates(self):
        """Test that annualized estimates are calculated correctly."""
        result = calculate_salary(
            basic_salary=Decimal("25000.00"),
            hra=Decimal("10000.00"),
            other_allowances=Decimal("5000.00"),
            bonus_overtime=Decimal("0.00"),
            pf_deduction=Decimal("3000.00"),
            professional_tax=Decimal("200.00"),
            income_tax_estimate=Decimal("0.00"),
            other_deductions=Decimal("0.00"),
        )
        self.assertEqual(result["annualized_gross"], Decimal("480000.00"))
        self.assertEqual(result["annualized_net"], Decimal("441600.00"))

    def test_all_zero_inputs(self):
        """Test calculation with all zero inputs."""
        result = calculate_salary(
            basic_salary=Decimal("0.00"),
            hra=Decimal("0.00"),
            other_allowances=Decimal("0.00"),
            bonus_overtime=Decimal("0.00"),
            pf_deduction=Decimal("0.00"),
            professional_tax=Decimal("0.00"),
            income_tax_estimate=Decimal("0.00"),
            other_deductions=Decimal("0.00"),
        )
        self.assertEqual(result["gross_salary"], Decimal("0.00"))
        self.assertEqual(result["total_deductions"], Decimal("0.00"))
        self.assertEqual(result["net_salary"], Decimal("0.00"))
        self.assertEqual(result["annualized_gross"], Decimal("0.00"))
        self.assertEqual(result["annualized_net"], Decimal("0.00"))
        self.assertFalse(result["is_negative"])

    def test_blank_optional_values(self):
        """Test that default values work correctly when optional values are omitted."""
        result = calculate_salary(basic_salary=Decimal("25000.00"))
        self.assertEqual(result["gross_salary"], Decimal("25000.00"))
        self.assertEqual(result["total_deductions"], Decimal("0.00"))
        self.assertEqual(result["net_salary"], Decimal("25000.00"))

    def test_decimal_arithmetic_precision(self):
        """Test that decimal arithmetic maintains precision."""
        result = calculate_salary(
            basic_salary=Decimal("25000.33"),
            hra=Decimal("10000.67"),
            other_allowances=Decimal("5000.50"),
            pf_deduction=Decimal("3000.25"),
            professional_tax=Decimal("200.75"),
        )
        # Gross: 25000.33 + 10000.67 + 5000.50 = 40001.50
        # Deductions: 3000.25 + 200.75 = 3201.00
        # Net: 40001.50 - 3201.00 = 36800.50
        self.assertEqual(result["gross_salary"], Decimal("40001.50"))
        self.assertEqual(result["total_deductions"], Decimal("3201.00"))
        self.assertEqual(result["net_salary"], Decimal("36800.50"))

    def test_deductions_equal_to_gross(self):
        """Test when deductions exactly equal gross salary."""
        result = calculate_salary(
            basic_salary=Decimal("25000.00"),
            hra=Decimal("10000.00"),
            pf_deduction=Decimal("35000.00"),
        )
        self.assertEqual(result["gross_salary"], Decimal("35000.00"))
        self.assertEqual(result["total_deductions"], Decimal("35000.00"))
        self.assertEqual(result["net_salary"], Decimal("0.00"))
        self.assertFalse(result["is_negative"])

    def test_deductions_exceed_gross(self):
        """Test when deductions exceed gross salary (negative net)."""
        result = calculate_salary(
            basic_salary=Decimal("25000.00"),
            hra=Decimal("10000.00"),
            pf_deduction=Decimal("40000.00"),
        )
        self.assertEqual(result["gross_salary"], Decimal("35000.00"))
        self.assertEqual(result["total_deductions"], Decimal("40000.00"))
        self.assertEqual(result["net_salary"], Decimal("-5000.00"))
        self.assertTrue(result["is_negative"])

    def test_negative_net_salary_flagged(self):
        """Test that negative net salary is correctly flagged."""
        result = calculate_salary(
            basic_salary=Decimal("10000.00"), pf_deduction=Decimal("15000.00")
        )
        self.assertTrue(result["is_negative"])
        self.assertEqual(result["net_salary"], Decimal("-5000.00"))

    def test_input_normalization(self):
        """Test that all input values are normalized to 2 decimal places."""
        result = calculate_salary(basic_salary=Decimal("25000"))
        self.assertEqual(result["basic_salary"], Decimal("25000.00"))
        self.assertEqual(result["hra"], Decimal("0.00"))


class SalaryCalculatorFormTests(TestCase):
    """Test cases for the SalaryCalculatorForm."""

    def test_valid_input_accepted(self):
        """Test that valid input is accepted."""
        form_data = {
            "basic_salary": "25000.00",
            "hra": "10000.00",
            "other_allowances": "5000.00",
            "pf_deduction": "3000.00",
            "professional_tax": "200.00",
        }
        form = SalaryCalculatorForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_basic_salary_rejected(self):
        """Test that missing basic salary is rejected."""
        form_data = {
            "hra": "10000.00",
        }
        form = SalaryCalculatorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("basic_salary", form.errors)

    def test_negative_amount_rejected(self):
        """Test that negative amounts are rejected."""
        form_data = {
            "basic_salary": "-5000.00",
        }
        form = SalaryCalculatorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("basic_salary", form.errors)

    def test_invalid_numeric_rejected(self):
        """Test that invalid numeric input is rejected."""
        form_data = {
            "basic_salary": "invalid",
        }
        form = SalaryCalculatorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("basic_salary", form.errors)

    def test_too_many_decimal_places_rejected(self):
        """Test that values with more than 2 decimal places are rejected."""
        form_data = {
            "basic_salary": "25000.123",
        }
        form = SalaryCalculatorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("basic_salary", form.errors)

    def test_blank_optional_values_become_zero(self):
        """Test that blank optional values are normalized to zero."""
        form_data = {
            "basic_salary": "25000.00",
            # All other fields left blank
        }
        form = SalaryCalculatorForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["hra"], Decimal("0.00"))
        self.assertEqual(form.cleaned_data["other_allowances"], Decimal("0.00"))
        self.assertEqual(form.cleaned_data["bonus_overtime"], Decimal("0.00"))
        self.assertEqual(form.cleaned_data["pf_deduction"], Decimal("0.00"))
        self.assertEqual(form.cleaned_data["professional_tax"], Decimal("0.00"))
        self.assertEqual(form.cleaned_data["income_tax_estimate"], Decimal("0.00"))
        self.assertEqual(form.cleaned_data["other_deductions"], Decimal("0.00"))

    def test_maximum_field_limit_enforced(self):
        """Test that maximum field limits are enforced."""
        # Test with a value at the limit
        # max_digits=12, decimal_places=2 means: max 10 integer digits + 2 decimal
        form_data = {
            "basic_salary": "9999999999.99",  # Valid: 10 integer + 2 decimal = 12 total
        }
        form = SalaryCalculatorForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Test exceeding the limit
        form_data = {
            "basic_salary": "99999999999.99",  # Invalid: 11 integer + 2 decimal = 13 total
        }
        form = SalaryCalculatorForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_zero_values_accepted(self):
        """Test that zero values are accepted for all fields."""
        form_data = {
            "basic_salary": "0.00",
            "hra": "0.00",
            "other_allowances": "0.00",
            "bonus_overtime": "0.00",
            "pf_deduction": "0.00",
            "professional_tax": "0.00",
            "income_tax_estimate": "0.00",
            "other_deductions": "0.00",
        }
        form = SalaryCalculatorForm(data=form_data)
        self.assertTrue(form.is_valid())


class SalaryCalculationModelTests(TestCase):
    """Test cases for the SalaryCalculation model."""

    def test_create_salary_calculation(self):
        """Test that a salary calculation can be created."""
        calc = SalaryCalculation.objects.create(
            basic_salary=Decimal("25000.00"),
            hra=Decimal("10000.00"),
            other_allowances=Decimal("5000.00"),
            pf_deduction=Decimal("3000.00"),
            professional_tax=Decimal("200.00"),
            gross_salary=Decimal("40000.00"),
            total_deductions=Decimal("3200.00"),
            net_salary=Decimal("36800.00"),
        )
        self.assertIsNotNone(calc.id)
        self.assertIsNotNone(calc.created_at)

    def test_retrieve_salary_calculation(self):
        """Test that a salary calculation can be retrieved."""
        calc = SalaryCalculation.objects.create(
            label="Test Calculation",
            basic_salary=Decimal("25000.00"),
            hra=Decimal("10000.00"),
            gross_salary=Decimal("35000.00"),
            total_deductions=Decimal("3000.00"),
            net_salary=Decimal("32000.00"),
        )
        retrieved = SalaryCalculation.objects.get(id=calc.id)
        self.assertEqual(retrieved.label, "Test Calculation")
        self.assertEqual(retrieved.basic_salary, Decimal("25000.00"))
        self.assertEqual(retrieved.net_salary, Decimal("32000.00"))

    def test_string_representation(self):
        """Test that the string representation is correct."""
        calc = SalaryCalculation.objects.create(
            label="Monthly Salary",
            basic_salary=Decimal("25000.00"),
            gross_salary=Decimal("35000.00"),
            total_deductions=Decimal("3000.00"),
            net_salary=Decimal("32000.00"),
        )
        str_repr = str(calc)
        self.assertIn("Monthly Salary", str_repr)
        self.assertIn("32000.00", str_repr)

    def test_ordering(self):
        """Test that calculations are ordered by creation time (newest first)."""
        calc1 = SalaryCalculation.objects.create(
            basic_salary=Decimal("20000.00"),
            gross_salary=Decimal("20000.00"),
            total_deductions=Decimal("0.00"),
            net_salary=Decimal("20000.00"),
        )
        calc2 = SalaryCalculation.objects.create(
            basic_salary=Decimal("25000.00"),
            gross_salary=Decimal("25000.00"),
            total_deductions=Decimal("0.00"),
            net_salary=Decimal("25000.00"),
        )
        calculations = list(SalaryCalculation.objects.all())
        self.assertEqual(calculations[0].id, calc2.id)
        self.assertEqual(calculations[1].id, calc1.id)




class ViewTests(TestCase):
    """Test cases for calculator views."""

    def test_dashboard_get(self):
        """Test that dashboard view returns 200 on GET."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator/dashboard.html')
        self.assertContains(response, 'Smart Salary Calculator')

    def test_calculator_get(self):
        """Test that calculator view returns 200 on GET and shows form."""
        response = self.client.get('/calculator/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator/calculator_form.html')
        self.assertContains(response, 'Monthly Earnings')
        self.assertContains(response, 'Monthly Deductions')

    def test_calculator_post_valid(self):
        """Test that valid POST shows results."""
        response = self.client.post('/calculator/', {
            'basic_salary': '25000.00',
            'hra': '10000.00',
            'other_allowances': '5000.00',
            'bonus_overtime': '0.00',
            'pf_deduction': '3000.00',
            'professional_tax': '200.00',
            'income_tax_estimate': '0.00',
            'other_deductions': '0.00',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator/result.html')
        self.assertContains(response, '40000.00')  # Gross salary
        self.assertContains(response, '3200.00')   # Total deductions
        self.assertContains(response, '36800.00')  # Net salary

    def test_calculator_post_invalid(self):
        """Test that invalid POST shows form with errors."""
        response = self.client.post('/calculator/', {
            'basic_salary': '',  # Missing required field
            'hra': '10000.00',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator/calculator_form.html')
        self.assertContains(response, 'This field is required')

    def test_calculator_negative_net_salary_warning(self):
        """Test that negative net salary shows warning."""
        response = self.client.post('/calculator/', {
            'basic_salary': '10000.00',
            'hra': '0.00',
            'other_allowances': '0.00',
            'bonus_overtime': '0.00',
            'pf_deduction': '15000.00',  # Exceeds gross
            'professional_tax': '0.00',
            'income_tax_estimate': '0.00',
            'other_deductions': '0.00',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator/result.html')
        self.assertContains(response, 'Warning: Negative Net Salary')
        self.assertContains(response, 'exceed your gross salary')
