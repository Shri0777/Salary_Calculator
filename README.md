# Smart Salary Calculator

A Django-based salary calculation tool designed for college compensation class demonstrations. This application performs precise salary calculations using Decimal arithmetic and provides a professional web interface with green-and-white design.

## Project Status

**Phase 1 Complete**: Core calculation engine, forms, models, and comprehensive testing.
**Phase 2 Complete**: Professional browser interface with dashboard, calculator form, results page, and responsive CSS.

## Technology Stack

- Python 3.14.7
- Django 5.0.14
- SQLite (development database)
- Django Forms
- Django ORM
- Django Testing Framework

**JavaScript is prohibited** throughout this project.

## Project Structure

```
Salary_Calculator/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── config/                      # Django project settings
│   ├── __init__.py
│   ├── settings.py             # Main settings (templates & static configured)
│   ├── urls.py                 # URL routing (dashboard, calculator)
│   ├── asgi.py                 # ASGI config
│   └── wsgi.py                 # WSGI config
├── calculator/                  # Salary calculator app
│   ├── __init__.py
│   ├── admin.py                # Admin interface registration
│   ├── apps.py                 # App configuration
│   ├── forms.py                # Salary input form with validation
│   ├── models.py               # SalaryCalculation model
│   ├── services.py             # Calculation business logic
│   ├── views.py                # Dashboard and calculator views
│   ├── tests.py                # Comprehensive test suite (23 tests)
│   └── migrations/             # Database migrations
│       └── 0001_initial.py
├── templates/                   # Django templates
│   ├── base.html               # Base template with sidebar navigation
│   └── calculator/
│       ├── dashboard.html      # Landing page with overview
│       ├── calculator_form.html # Salary input form
│       └── result.html         # Calculation results
├── static/                      # Static assets
│   └── css/
│       └── style.css           # Green-and-white design system
├── venv/                        # Virtual environment (not in Git)
└── db.sqlite3                   # SQLite database (created after migration)
```

## Features Implemented

### Phase 1: Core Calculation Engine

#### 1. Salary Calculation Service (`calculator/services.py`)

- **Precise Decimal arithmetic** for all monetary calculations
- Calculates gross salary, total deductions, net salary
- Computes annualized estimates (gross and net)
- Handles edge cases: zero values, negative net salary
- Flags when deductions exceed gross salary

**Supported Earnings:**
- Basic salary (required)
- House Rent Allowance (HRA)
- Other allowances
- Bonus and overtime

**Supported Deductions:**
- Provident Fund (PF) deduction
- Professional tax
- Income tax estimate
- Other deductions

**Mandatory Formulas:**
```
Gross Salary = Basic + HRA + Other Allowances + Bonus/Overtime
Total Deductions = PF + Professional Tax + Income Tax + Other Deductions
Net Salary = Gross Salary - Total Deductions
Annualized Gross = Gross Salary × 12
Annualized Net = Net Salary × 12
```

### 2. Input Form (`calculator/forms.py`)

- Django Form with comprehensive validation
- All fields use `DecimalField` for precise monetary values
- Server-side validation (source of truth)
- Validates: required fields, non-negative amounts, max 2 decimal places
- Normalizes blank optional inputs to `Decimal("0.00")`
- Sensible maximum values to prevent overflow

### 3. Database Model (`calculator/models.py`)

- `SalaryCalculation` model for storing calculation history
- Stores snapshot of inputs and calculated results
- Automatically records creation timestamp
- Optional descriptive label field
- Ordered by creation date (newest first)
- Registered in Django admin interface

### 4. Comprehensive Test Suite (`calculator/tests.py`)

**23 automated tests covering:**

**Calculation Service Tests (11 tests):**
- Gross salary calculation
- Total deductions calculation
- Net salary calculation
- Annualized estimates
- All-zero inputs
- Blank optional values
- Decimal arithmetic precision
- Deductions equal to gross
- Deductions exceeding gross
- Negative net salary flagging
- Input normalization

**Form Tests (8 tests):**
- Valid input acceptance
- Missing basic salary rejection
- Negative amount rejection
- Invalid numeric rejection
- Too many decimal places rejection
- Blank optional values normalization
- Maximum field limit enforcement
- Zero values acceptance

**Model Tests (4 tests):**
- Creation of salary calculations
- Retrieval of records
- String representation
- Ordering by creation date

### 5. Admin Interface

- SalaryCalculation model registered in Django admin
- List display: label, basic salary, gross, net, created date
- Filtering by creation date
- Search by label
- Date hierarchy navigation

### Phase 2: Professional Browser Interface

#### 1. Dashboard Landing Page (`templates/calculator/dashboard.html`)

- Professional header with app title and description
- Call-to-action button linking to calculator
- Three overview cards explaining salary components:
  - **Gross Salary**: Total monthly earnings before deductions
  - **Deductions**: Statutory and voluntary deductions
  - **Net Salary**: Take-home pay after deductions
- "How It Works" section with calculation explanation
- Disclaimer about educational purpose
- Responsive sidebar navigation

#### 2. Salary Calculator Form (`templates/calculator/calculator_form.html`)

- Two-section form layout:
  - **Monthly Earnings**: Basic salary, HRA, other allowances, bonus/overtime
  - **Monthly Deductions**: PF, professional tax, income tax estimate, other deductions
- Professional form styling with currency input fields
- Server-side validation with error display
- Submit and reset buttons
- Help text for required fields
- Mobile-responsive design

#### 3. Calculation Results Page (`templates/calculator/result.html`)

- Prominent net salary display with visual highlighting
- Summary cards showing:
  - Net Salary (take-home pay)
  - Gross Salary (total earnings)
  - Total Deductions
- Detailed earnings breakdown table
- Detailed deductions breakdown table
- Annualized estimates (12-month projections)
- Warning banner for negative net salary (when deductions exceed gross)
- "Calculate Again" and "Back to Dashboard" action buttons
- Educational disclaimer

#### 4. Design System (`static/css/style.css`)

- **Color Palette**: Professional green-and-white theme
  - Primary green: #2E7D32 (buttons, highlights)
  - Dark green: #1B4332 (sidebar)
  - Background: #F5F7F6 (subtle off-white)
- **Layout**: Desktop sidebar + main content area
- **Components**: Cards, forms, buttons, tables, messages
- **Typography**: System font stack with readable sizes
- **Responsive**: Mobile breakpoints at 768px and 480px
- **Accessibility**: Focus states, ARIA-compatible structure
- **No JavaScript**: Pure CSS-only interactions

#### 5. Views (`calculator/views.py`)

- **dashboard**: Renders landing page (GET only)
- **calculator**: Handles form display and calculation
  - GET: Shows empty form
  - POST: Validates input, calculates salary, displays results
  - Invalid input: Redisplays form with errors
  - Success/error messages via Django messages framework

#### 6. URL Configuration

- `/` - Dashboard landing page (named: 'dashboard')
- `/calculator/` - Calculator form and results (named: 'calculator')
- `/admin/` - Django admin interface

## Setup Instructions

### 1. Prerequisites

- Python 3.14.7 (or compatible version)
- pip (Python package manager)

### 2. Initial Setup

```bash
# Navigate to project directory
cd /home/shri/Development/Salary_Calculator

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Create database tables
python manage.py migrate

# (Optional) Create superuser for admin access
python manage.py createsuperuser
```

### 4. Verify Installation

```bash
# Run Django system checks
python manage.py check

# Run test suite
python manage.py test calculator
```

Expected output: `Ran 23 tests ... OK`

### 5. Start Development Server

```bash
# Start the Django development server
python manage.py runserver

# Access at: http://127.0.0.1:8000/
# Admin interface at: http://127.0.0.1:8000/admin/
```

### 6. Accessing Phase 3 Features

After starting the development server, these new routes are available:

- **Dashboard**: `http://127.0.0.1:8000/` — Summary stats, link to calculator
- **Calculator**: `http://127.0.0.1:8000/calculator/` — Enter salary inputs and calculate
- **Save Calculation**: After computing results, click "Save Calculation" to store a snapshot
- **History**: `http://127.0.0.1:8000/history/` — List all saved calculations, newest first
- **History Detail**: `http://127.0.0.1:8000/calculation/{id}/` — View complete breakdown of a saved record
- **Payslip Preview**: `http://127.0.0.1:8000/calculation/{id}/payslip/` — Printable HTML payslip with disclaimer
- **Delete Calculation**: Use the Delete action on any history record confirmation page

### 6. Usage Example

1. Start the server: `python manage.py runserver`
2. Visit `http://127.0.0.1:8000/` for the dashboard
3. Go to `http://127.0.0.1:8000/calculator/` to enter salary inputs
4. Review the results page and click "Save Calculation"
5. Visit `http://127.0.0.1:8000/history/` to see all saved records
6. Click "View Details" on any record for the full breakdown
7. Use "Open Payslip Preview" for a printable HTML version
8. Use "Delete" to remove individual records (confirmed via POST)

### 7. Known URLs

| Feature | URL | Notes |
|---|---|---|
| Dashboard | `/` | Default landing page |
| Calculator | `/calculator/` | Form submission required |
| Save Calculation | `/calculation/save/` | POST only, from results page |
| History List | `/history/` | Search by label, pagination |
| History Detail | `/calculation/{id}/` | `get_object_or_404` for missing IDs |
| Payslip Preview | `/calculation/{id}/payslip/` | Print-optimized HTML |
| Delete Confirmation | `/calculation/{id}/delete/` | GET shows confirmation, POST deletes |

## Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all calculator tests
python manage.py test calculator

# Run specific test class
python manage.py test calculator.tests.SalaryCalculationServiceTests

# Run with verbose output
python manage.py test calculator --verbosity=2
```

Expected output: `Ran 23 tests ... OK`

## Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all calculator tests
python manage.py test calculator

# Run specific test class
python manage.py test calculator.tests.SalaryCalculationServiceTests

# Run with verbose output
python manage.py test calculator --verbosity=2
```

## Usage Example

### Using the Calculation Service

```python
from decimal import Decimal
from calculator.services import calculate_salary

# Example calculation
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

print(f"Gross Salary: ₹{result['gross_salary']}")
print(f"Total Deductions: ₹{result['total_deductions']}")
print(f"Net Salary: ₹{result['net_salary']}")
print(f"Annualized Gross: ₹{result['annualized_gross']}")
print(f"Annualized Net: ₹{result['annualized_net']}")
print(f"Is Negative: {result['is_negative']}")
```

### Using the Form

```python
from calculator.forms import SalaryCalculatorForm

form_data = {
    'basic_salary': '25000.00',
    'hra': '10000.00',
    'other_allowances': '5000.00',
    'pf_deduction': '3000.00',
    'professional_tax': '200.00',
}

form = SalaryCalculatorForm(data=form_data)
if form.is_valid():
    # Access cleaned data
    cleaned = form.cleaned_data
    # Pass to calculation service
    result = calculate_salary(**cleaned)
```

## Important Notes

### Decimal Precision
All monetary calculations use Python's `Decimal` type to avoid floating-point precision errors. Values are normalized to 2 decimal places.

### Negative Net Salary
If deductions exceed gross salary, the calculation service:
- Returns the mathematically correct negative net salary
- Sets `is_negative: True` flag
- Does NOT clamp or hide the negative value

This allows the UI to display appropriate warnings in future phases.

### No Tax Calculations
This application does NOT calculate:
- Income tax based on slabs
- PF percentages
- Professional tax rates

Users must enter deduction amounts manually. This is NOT a statutory payroll compliance tool.

### Annualized Estimates
Annualized values assume the same monthly salary structure throughout the year. They are estimates, not guaranteed annual earnings.

## Testing Notes

### Phase 1 Tests (23 tests)

All Phase 1 tests pass successfully:

```bash
python manage.py test calculator.tests.SalaryCalculationServiceTests calculator.tests.SalaryCalculatorFormTests calculator.tests.SalaryCalculationModelTests
```

**Test Coverage:**
- 11 calculation service tests
- 8 form validation tests
- 4 model tests

### Phase 2 Tests

Phase 2 view tests are written but encounter a Python 3.14 compatibility issue with Django 5.0.14's test client (AttributeError in context copying). This is a known Django framework bug, not an issue with the application code.

**Manual Verification:**
A manual verification script (`verify_phase2.py`) confirms all Phase 2 functionality works correctly:
- Dashboard view rendering
- Calculator form display
- Form validation
- Calculation results
- Negative salary warnings
- No JavaScript in templates

The application works correctly when accessed via the development server.

## Known Issues

### Python 3.14 + Django 5.0.14 Compatibility

Django's test client has a compatibility issue with Python 3.14 related to the `super()` object changes. This affects only the test infrastructure, not the actual application. The views and templates work correctly when accessed through the browser or direct view calls.

**Impact**: View tests using Django's test client fail with `AttributeError: 'super' object has no attribute 'dicts'`.

**Workaround**: Use manual verification script or test via development server.

## Phase 2 Limitations

**Not Implemented (Future Phases):**
- Salary history persistence and viewing
- Payslip PDF generation
- Charts or visualizations  
- User authentication/authorization
- Multi-user support
- API endpoints
- Deployment configuration

Phase 2 focuses on the browser interface with no-JavaScript requirement.

## Development Guidelines

### Code Quality
- Use Decimal for all monetary values
- Write tests for new features
- Follow Django best practices
- Keep business logic in services.py
- Validate on server-side

### Testing
- Run tests before committing changes
- Maintain test coverage
- Test edge cases (zero, negative, boundary values)

### Dependencies
- Minimize external dependencies
- Document version requirements
- Use virtual environment

## Troubleshooting

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database Issues
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
```

### Test Failures
```bash
# Run with verbose output
python manage.py test calculator --verbosity=2

# Run specific failing test
python manage.py test calculator.tests.TestClassName.test_method_name
```

## Version Information

- Django: 5.0.14
- Python: 3.14.7
- Database: SQLite 3 (bundled with Python)

## Next Steps (Phase 3 and Beyond)

Future phases could add:
1. Salary history persistence and viewing
2. Payslip PDF generation
3. Charts and data visualizations
4. User authentication and authorization
5. Multi-user support
6. REST API endpoints
7. Deployment configuration

## License

Educational project for college demonstration purposes.

## Support

This is a Phase 2 implementation. Refer to this README for setup and usage instructions.
