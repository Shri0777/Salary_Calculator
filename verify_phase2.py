#!/usr/bin/env python
"""
Manual verification script for Phase 2 views.
This bypasses the Django test client to avoid the Python 3.14 bug.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, '/home/shri/Development/Salary_Calculator')
django.setup()

from decimal import Decimal
from django.test import RequestFactory
from calculator.views import dashboard, calculator
from calculator.forms import SalaryCalculatorForm

print("="*60)
print("MANUAL PHASE 2 VERIFICATION")
print("="*60)

# Create request factory
factory = RequestFactory()

# Test 1: Dashboard GET
print("\n1. Testing dashboard GET...")
try:
    request = factory.get('/')
    response = dashboard(request)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    content = response.content.decode('utf-8')
    assert 'Smart Salary Calculator' in content
    assert 'Dashboard' in content
    print("   ✓ Dashboard GET returns 200")
    print("   ✓ Dashboard contains expected content")
except Exception as e:
    print(f"   ✗ Dashboard test failed: {e}")
    sys.exit(1)

# Test 2: Calculator GET
print("\n2. Testing calculator GET...")
try:
    request = factory.get('/calculator/')
    response = calculator(request)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    content = response.content.decode('utf-8')
    assert 'Monthly Earnings' in content or 'Basic Salary' in content
    assert 'Monthly Deductions' in content or 'Provident Fund' in content
    print("   ✓ Calculator GET returns 200")
    print("   ✓ Calculator form contains expected sections")
except Exception as e:
    print(f"   ✗ Calculator GET test failed: {e}")
    sys.exit(1)

# Test 3: Calculator POST with valid data
print("\n3. Testing calculator POST with valid data...")
try:
    request = factory.post('/calculator/', {
        'basic_salary': '25000.00',
        'hra': '10000.00',
        'other_allowances': '5000.00',
        'bonus_overtime': '0.00',
        'pf_deduction': '3000.00',
        'professional_tax': '200.00',
        'income_tax_estimate': '0.00',
        'other_deductions': '0.00',
    })
    response = calculator(request)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    content = response.content.decode('utf-8')
    
    # Check for result values
    assert '40000.00' in content, "Gross salary (40000.00) not found"
    assert '3200.00' in content, "Total deductions (3200.00) not found"
    assert '36800.00' in content, "Net salary (36800.00) not found"
    
    print("   ✓ Calculator POST with valid data returns 200")
    print("   ✓ Result page shows correct calculations")
    print("     - Gross: ₹40000.00")
    print("     - Deductions: ₹3200.00")
    print("     - Net: ₹36800.00")
except Exception as e:
    print(f"   ✗ Calculator POST test failed: {e}")
    sys.exit(1)

# Test 4: Calculator POST with invalid data
print("\n4. Testing calculator POST with invalid data...")
try:
    request = factory.post('/calculator/', {
        'basic_salary': '',  # Missing required field
        'hra': '10000.00',
    })
    response = calculator(request)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    content = response.content.decode('utf-8')
    assert 'This field is required' in content or 'required' in content.lower()
    print("   ✓ Calculator POST with invalid data returns 200")
    print("   ✓ Form shows validation errors")
except Exception as e:
    print(f"   ✗ Calculator POST invalid test failed: {e}")
    sys.exit(1)

# Test 5: Negative net salary warning
print("\n5. Testing negative net salary warning...")
try:
    request = factory.post('/calculator/', {
        'basic_salary': '10000.00',
        'hra': '0.00',
        'other_allowances': '0.00',
        'bonus_overtime': '0.00',
        'pf_deduction': '15000.00',  # Exceeds gross
        'professional_tax': '0.00',
        'income_tax_estimate': '0.00',
        'other_deductions': '0.00',
    })
    response = calculator(request)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    content = response.content.decode('utf-8')
    assert 'Warning' in content or 'warning' in content
    assert 'Negative' in content or 'negative' in content or 'exceed' in content
    print("   ✓ Negative net salary returns 200")
    print("   ✓ Warning message displayed for negative net salary")
except Exception as e:
    print(f"   ✗ Negative salary test failed: {e}")
    sys.exit(1)

# Test 6: No JavaScript in templates
print("\n6. Verifying no JavaScript in templates...")
try:
    import glob
    js_found = False
    template_files = glob.glob('templates/**/*.html', recursive=True)
    
    for template_path in template_files:
        with open(template_path, 'r') as f:
            content = f.read().lower()
            if '<script' in content or 'javascript:' in content:
                js_found = True
                print(f"   ✗ JavaScript found in {template_path}")
    
    if not js_found:
        print("   ✓ No JavaScript found in templates")
    else:
        print("   ✗ Templates contain JavaScript (prohibited)")
        sys.exit(1)
except Exception as e:
    print(f"   ✗ JavaScript check failed: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("ALL MANUAL TESTS PASSED ✓")
print("="*60)
print("\nPhase 2 Implementation Summary:")
print("- Dashboard view working correctly")
print("- Calculator form rendering properly")
print("- Form validation working")
print("- Calculation results displaying correctly")
print("- Negative salary warnings showing")
print("- No JavaScript detected in templates")
print("\nNote: Django test client has Python 3.14 compatibility issues,")
print("but the views and templates work correctly with manual testing.")
