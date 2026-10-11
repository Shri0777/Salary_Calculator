# Quick Start Guide

## Starting the Application

```bash
# Navigate to project directory
cd /home/shri/Development/Salary_Calculator

# Activate virtual environment
source venv/bin/activate

# Start the development server
python manage.py runserver

# Access the application
# Open browser to: http://127.0.0.1:8000/
```

## Using the Calculator

### 1. Dashboard (http://127.0.0.1:8000/)
- Landing page with overview of salary components
- Click **"Calculate Salary"** button to proceed

### 2. Calculator Form (http://127.0.0.1:8000/calculator/)

**Monthly Earnings:**
- Basic Salary (required) - e.g., 25000.00
- HRA (optional) - e.g., 10000.00
- Other Allowances (optional) - e.g., 5000.00
- Bonus and Overtime (optional) - e.g., 0.00

**Monthly Deductions:**
- PF Deduction (optional) - e.g., 3000.00
- Professional Tax (optional) - e.g., 200.00
- Income Tax Estimate (optional) - e.g., 0.00
- Other Deductions (optional) - e.g., 0.00

Click **"Calculate Salary"** to see results.

### 3. Results Page
- View net salary (take-home pay)
- See detailed breakdown of earnings and deductions
- Check annualized estimates (yearly projections)
- If deductions exceed gross, a warning is displayed

## Example Calculation

**Input:**
```
Basic Salary: 25000.00
HRA: 10000.00
Other Allowances: 5000.00
Bonus/Overtime: 0.00
PF Deduction: 3000.00
Professional Tax: 200.00
Income Tax: 0.00
Other Deductions: 0.00
```

**Output:**
```
Gross Salary: ₹40,000.00
Total Deductions: ₹3,200.00
Net Salary: ₹36,800.00
Annualized Gross: ₹4,80,000.00
Annualized Net: ₹4,41,600.00
```

## Testing

### Run Phase 1 Tests
```bash
source venv/bin/activate
python manage.py test calculator.tests.SalaryCalculationServiceTests calculator.tests.SalaryCalculatorFormTests calculator.tests.SalaryCalculationModelTests
```

Expected: **Ran 23 tests ... OK**

### Run Phase 2 Manual Verification
```bash
source venv/bin/activate
python verify_phase2.py
```

Expected: **ALL MANUAL TESTS PASSED ✓**

## Troubleshooting

### Port Already in Use
If port 8000 is busy, use a different port:
```bash
python manage.py runserver 8001
```

### Virtual Environment Not Found
Recreate the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database Issues
Reset the database (development only):
```bash
rm db.sqlite3
python manage.py migrate
```

## Features

✅ Dashboard landing page  
✅ Professional calculator form  
✅ Detailed results display  
✅ Negative salary warnings  
✅ Mobile-responsive design  
✅ No JavaScript (CSS-only)  
✅ Form validation with errors  
✅ Clean green-and-white design  

## Navigation

- **Dashboard**: http://127.0.0.1:8000/
- **Calculator**: http://127.0.0.1:8000/calculator/
- **Admin**: http://127.0.0.1:8000/admin/

## Notes

- All monetary values use Decimal precision (no floating-point errors)
- The application is for educational purposes only
- This is NOT a statutory payroll compliance tool
- Tax calculations must be entered manually
- Annualized estimates assume constant monthly salary

## Project Status

**Phase 1**: ✅ Complete - Core calculation engine  
**Phase 2**: ✅ Complete - Browser interface  
**Phase 3**: ⏳ Future - Additional features
