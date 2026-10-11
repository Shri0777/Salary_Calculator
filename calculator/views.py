from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_protect
from decimal import Decimal

from .forms import SalaryCalculatorForm
from .services import calculate_salary
from .models import SalaryCalculation


def dashboard(request):
    """
    Dashboard landing page with overview and navigation.
    
    GET: Renders the dashboard template with statistics about saved calculations.
    """
    calculations = SalaryCalculation.objects.all()
    num_calculations = calculations.count()
    
    latest_calculation = calculations.first()
    
    context = {
        'num_calculations': num_calculations,
        'latest_calculation': latest_calculation,
    }
    
    if latest_calculation:
        context['latest_gross'] = latest_calculation.gross_salary
        context['latest_net'] = latest_calculation.net_salary
    else:
        context['latest_gross'] = Decimal('0.00')
        context['latest_net'] = Decimal('0.00')
    
    return render(request, 'calculator/dashboard.html', context)


def calculator(request):
    """
    Salary calculator form and result handler.
    
    GET: Displays the salary calculator form.
    POST: Validates form data, calculates salary, and displays results.
    """
    if request.method == 'POST':
        form = SalaryCalculatorForm(request.POST)
        
        if form.is_valid():
            # Get cleaned data from form
            cleaned_data = form.cleaned_data
            
            # Calculate salary using the service
            result = calculate_salary(**cleaned_data)
            
            # Add success message (if messages framework is available)
            if hasattr(request, '_messages'):
                messages.success(request, 'Salary calculated successfully!')
                
                # If negative net salary, add a warning message
                if result['is_negative']:
                    messages.warning(
                        request,
                        'Warning: Total deductions exceed gross salary, resulting in negative net pay.'
                    )
            
            # Render result page with calculation results
            return render(request, 'calculator/result.html', {
                'result': result,
            })
        else:
            # Form has validation errors
            if hasattr(request, '_messages'):
                messages.error(
                    request,
                    'Please correct the errors below and try again.'
                )
    else:
        # GET request - show empty form
        form = SalaryCalculatorForm()
    
    return render(request, 'calculator/calculator_form.html', {
        'form': form,
    })


@require_POST
@csrf_protect
def save_calculation(request):
    """
    Save the current calculation to history.
    
    POST: Validates inputs, recalculates, and saves a SalaryCalculation snapshot.
    Redirects to the saved record's detail page on success.
    Uses POST/Redirect/Get pattern to prevent resubmission on refresh.
    """
    form = SalaryCalculatorForm(request.POST)
    
    if form.is_valid():
        # Get cleaned data from form - re-validate and recalculate
        cleaned_data = form.cleaned_data
        
        # Calculate salary using the service (recomputes from input values)
        result = calculate_salary(**cleaned_data)
        
        # Create a SalaryCalculation snapshot with the computed results
        calc = SalaryCalculation.objects.create(
            basic_salary=result['basic_salary'],
            hra=result['hra'],
            other_allowances=result['other_allowances'],
            bonus_overtime=result['bonus_overtime'],
            pf_deduction=result['pf_deduction'],
            professional_tax=result['professional_tax'],
            income_tax_estimate=result['income_tax_estimate'],
            other_deductions=result['other_deductions'],
            gross_salary=result['gross_salary'],
            total_deductions=result['total_deductions'],
            net_salary=result['net_salary'],
            label=cleaned_data.get('label', ''),
        )
        
        # Display success message
        messages.success(request, 'Calculation saved successfully to history!')
        
        # Redirect to the saved record's detail page using POST/Redirect/Get
        return redirect('history_detail', calc_id=calc.id)
    else:
        # Form validation failed - should not happen since we checked is_valid()
        messages.error(request, 'Error saving calculation. Please check the form data.')
        return redirect('calculator')


def history(request):
    """
    Salary history page that lists saved salary calculations.
    
    GET: Displays a paginated list of all saved calculations, sorted newest first.
    Supports optional search by calculation label via GET parameter.
    """
    query = request.GET.get('q', '')
    
    calculations = SalaryCalculation.objects.all().order_by('-created_at')
    
    # Optional search by label
    if query:
        calculations = calculations.filter(label__icontains=query)
    
    # Simple pagination: show 10 per page
    paginator = Paginator(calculations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'calculator/history.html', {
        'page_obj': page_obj,
        'search_query': query,
    })


def history_detail(request, calc_id):
    """
    Individual calculation detail page for a saved calculation.
    
    GET: Displays the complete original salary breakdown for the selected record.
    Shows earnings, deductions, annualized estimates, and provides a payslip preview link.
    """
    calc = get_object_or_404(SalaryCalculation, id=calc_id)
    
    # Compute annualized values from the saved snapshot
    monthly_gross = calc.gross_salary
    monthly_net = calc.net_salary
    
    annualized_gross = monthly_gross * 12
    annualized_net = monthly_net * 12
    
    # Calculate percentages for analysis
    if monthly_gross > 0:
        total_deductions_pct = (monthly_net / monthly_gross) * 100
        # Net percentage of gross
        net_pct_of_gross = (calc.net_salary / calc.gross_salary) * 100
    else:
        total_deductions_pct = Decimal('0.00')
        net_pct_of_gross = Decimal('0.00')
    
    is_negative = calc.net_salary < 0
    
    context = {
        'calc': calc,
        'annualized_gross': annualized_gross,
        'annualized_net': annualized_net,
        'total_deductions_pct': total_deductions_pct,
        'net_pct_of_gross': net_pct_of_gross,
        'is_negative': is_negative,
    }
    
    return render(request, 'calculator/history_detail.html', context)


def delete_calculation(request, calc_id):
    """
    Delete a specific saved calculation.
    
    POST: Deletes the selected SalaryCalculation record.
    GET: Displays a confirmation page (never deletes on GET).
    Redirects to history page with confirmation message.
    """
    calc = get_object_or_404(SalaryCalculation, id=calc_id)
    
    if request.method == 'POST':
        calc.delete()
        messages.success(request, 'Calculation deleted successfully.')
        return redirect('history')
    
    # GET request - show confirmation page
    return render(request, 'calculator/delete_confirmation.html', {
        'calc': calc,
    })


@csrf_protect
def payslip_preview(request, calc_id):
    """
    Professional, printable payslip preview for a saved calculation.
    
    GET: Renders a clean, print-friendly HTML payslip page.
    Uses @media print CSS to hide navigation and action buttons.
    Provides browser print instructions instead of JavaScript printing.
    """
    calc = get_object_or_404(SalaryCalculation, id=calc_id)
    
    # Compute annualized values from the saved snapshot
    monthly_gross = calc.gross_salary
    monthly_net = calc.net_salary
    
    annualized_gross = monthly_gross * 12
    annualized_net = monthly_net * 12
    
    context = {
        'calc': calc,
        'annualized_gross': annualized_gross,
        'annualized_net': annualized_net,
    }
    
    return render(request, 'calculator/payslip.html', context)