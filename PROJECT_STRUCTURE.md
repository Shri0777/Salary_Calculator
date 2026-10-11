# Smart Salary Calculator - Project Structure

Generated: Sunday, October 11, 2026

## Directory Tree

```
Salary_Calculator/
├── manage.py                           # Django management command
├── requirements.txt                    # Python dependencies (Django 5.2.18)
├── db.sqlite3                          # SQLite database (created after migrate)
│
├── README.md                           # Main documentation
├── QUICKSTART.md                       # Quick start guide
├── PHASE2_COMPLETE.md                  # Phase 2 completion summary
├── PROJECT_STRUCTURE.md                # This file
├── verify_phase2.py                    # Manual verification script
│
├── config/                             # Django project configuration
│   ├── __init__.py
│   ├── settings.py                     # Main settings (TEMPLATES, STATICFILES configured)
│   ├── urls.py                         # Root URL configuration
│   ├── asgi.py                         # ASGI entry point
│   └── wsgi.py                         # WSGI entry point
│
├── calculator/                         # Salary calculator app
│   ├── __init__.py
│   ├── admin.py                        # Admin interface (SalaryCalculation registered)
│   ├── apps.py                         # App configuration
│   ├── models.py                       # SalaryCalculation model
│   ├── forms.py                        # SalaryCalculatorForm with validation
│   ├── services.py                     # Calculation business logic (Decimal arithmetic)
│   ├── views.py                        # Dashboard and calculator views
│   ├── tests.py                        # Test suite (23 Phase 1 + 5 Phase 2 tests)
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py             # Initial migration
│
├── templates/                          # Django templates
│   ├── base.html                       # Base layout with sidebar navigation
│   └── calculator/
│       ├── dashboard.html              # Landing page with overview cards
│       ├── calculator_form.html        # Salary input form
│       └── result.html                 # Calculation results display
│
├── static/                             # Static assets
│   └── css/
│       └── style.css                   # Green-and-white design system (561 lines)
│
└── venv/                               # Virtual environment (not in Git)
    └── ...                             # Python 3.14.7 + Django 5.2.18
```

## File Sizes and Line Counts

### Configuration Files
- `requirements.txt` - 1 direct dependency (Django; its required dependencies are installed transitively)
- `config/settings.py` - ~130 lines
- `config/urls.py` - ~30 lines

### Application Code
- `calculator/models.py` - ~30 lines (SalaryCalculation model)
- `calculator/forms.py` - ~60 lines (8-field form with validation)
- `calculator/services.py` - ~100 lines (calculation engine)
- `calculator/views.py` - 68 lines (dashboard + calculator views)
- `calculator/admin.py` - ~20 lines
- `calculator/tests.py` - ~380 lines (28 tests total)

### Templates
- `templates/base.html` - 82 lines
- `templates/calculator/dashboard.html` - 68 lines
- `templates/calculator/calculator_form.html` - 255 lines
- `templates/calculator/result.html` - 143 lines
- **Total template lines**: 548 lines

### Static Assets
- `static/css/style.css` - 561 lines

### Documentation
- `README.md` - ~400 lines (comprehensive documentation)
- `QUICKSTART.md` - 140 lines (quick start guide)
- `PHASE2_COMPLETE.md` - 269 lines (completion summary)
- `PROJECT_STRUCTURE.md` - This file

### Testing & Verification
- `verify_phase2.py` - 163 lines (manual test script)

## Total Project Statistics

**Application Code:**
- Python files: ~658 lines (excluding tests)
- Test code: ~380 lines
- Templates: 548 lines
- CSS: 561 lines
- **Total code**: ~2,147 lines

**Documentation:**
- ~809 lines across 3 markdown files

## Key Files Explained

### Phase 1 (Core Engine)

**calculator/services.py**
- Pure calculation logic using Decimal arithmetic
- `calculate_salary()` function with 8 parameters
- Returns dictionary with 11 keys (inputs + calculated values)
- Handles edge cases: zero values, negative net salary

**calculator/forms.py**
- Django Form with 8 DecimalField inputs
- Server-side validation (required, non-negative, max decimals)
- Normalizes blank optional fields to Decimal("0.00")
- Maximum value limits to prevent overflow

**calculator/models.py**
- `SalaryCalculation` model for database persistence
- Stores snapshot of inputs and results
- Optional label field for identification
- Auto-timestamp on creation
- Ordered by creation date (newest first)

**calculator/admin.py**
- Registers SalaryCalculation in Django admin
- Custom list display with key fields
- Filtering and search capabilities

### Phase 2 (Browser Interface)

**templates/base.html**
- Base template with sidebar navigation
- Header with app title and subtitle
- Main content area with messages display
- Footer with copyright
- Responsive layout structure

**templates/calculator/dashboard.html**
- Welcome section with call-to-action button
- Three overview cards explaining components
- "How It Works" explanation section
- Educational disclaimer
- Links to calculator

**templates/calculator/calculator_form.html**
- Two-section form layout
- Monthly Earnings section (4 fields)
- Monthly Deductions section (4 fields)
- Currency input styling
- Form validation error display
- Submit and reset buttons

**templates/calculator/result.html**
- Prominent net salary display
- Three summary cards (Net, Gross, Deductions)
- Earnings breakdown table
- Deductions breakdown table
- Annualized estimates section
- Warning banner for negative net salary
- Action buttons (Calculate Again, Dashboard)

**static/css/style.css**
- CSS custom properties for color scheme
- Sidebar navigation (250px fixed width)
- Card component styling
- Form input styling with proper spacing
- Button variants (primary, secondary)
- Result display components
- Table styling
- Message and warning banners
- Mobile responsive breakpoints (768px, 480px)
- Accessibility features (focus states)

**calculator/views.py**
- `dashboard(request)` - GET only, renders landing page
- `calculator(request)` - GET shows form, POST validates and calculates
- Django messages integration (with graceful fallback)
- Form error handling
- Calculation result display

### Configuration

**config/settings.py** (Key Settings)
```python
TEMPLATES = [{
    'DIRS': [BASE_DIR / 'templates'],
    # ...
}]

STATICFILES_DIRS = [BASE_DIR / 'static']
```

**config/urls.py** (URL Patterns)
```python
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('calculator/', views.calculator, name='calculator'),
    path('admin/', admin.site.urls),
]
```

## Testing Structure

### Phase 1 Tests (23 tests) - All Passing ✅

**SalaryCalculationServiceTests** (11 tests)
- Basic calculation tests
- Edge case handling
- Decimal precision
- Negative salary detection

**SalaryCalculatorFormTests** (8 tests)
- Valid input acceptance
- Field validation (required, negative, decimals)
- Optional field normalization
- Maximum value enforcement

**SalaryCalculationModelTests** (4 tests)
- Model creation
- Data retrieval
- String representation
- Ordering

### Phase 2 View Tests (5 tests) - Automated and Passing

**ViewTests** (5 tests)
- Dashboard GET
- Calculator form GET
- Calculator POST with valid data
- Calculator POST with invalid data
- Negative net salary warning

**Note**: The earlier Python 3.14 / Django 5.0.14 test-client issue is resolved by upgrading to Django 5.2.18. The full 28-test suite passes.

## Dependencies

### Python Packages (requirements.txt)
```
Django==5.2.18
sqlparse==0.5.2
```

### System Requirements
- Python 3.14.7 (or compatible)
- SQLite 3 (bundled with Python)
- No external JavaScript libraries
- No frontend build tools

## Design System

### Color Palette
```css
--primary-green: #2E7D32
--dark-green: #1B4332
--very-dark-green: #172B24
--background: #F5F7F6
--white: #FFFFFF
--text-primary: #333333
--text-secondary: #666666
--border-color: #D1D5DB
--error-red: #DC2626
--warning-yellow: #F59E0B
--success-green: #10B981
```

### Layout Breakpoints
- Desktop: > 768px (sidebar + main content)
- Tablet: 768px - 480px (responsive adjustments)
- Mobile: < 480px (stacked layout)

### Typography
- Font: system-ui, -apple-system, Segoe UI, Roboto, sans-serif
- Base size: 16px (1rem)
- Line height: 1.5 (body), 1.2 (headings)

## Database Schema

### SalaryCalculation Table
```sql
CREATE TABLE calculator_salarycalculation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label VARCHAR(200) NULL,
    basic_salary DECIMAL(10, 2) NOT NULL,
    hra DECIMAL(10, 2) NOT NULL,
    other_allowances DECIMAL(10, 2) NOT NULL,
    bonus_overtime DECIMAL(10, 2) NOT NULL,
    pf_deduction DECIMAL(10, 2) NOT NULL,
    professional_tax DECIMAL(10, 2) NOT NULL,
    income_tax_estimate DECIMAL(10, 2) NOT NULL,
    other_deductions DECIMAL(10, 2) NOT NULL,
    gross_salary DECIMAL(10, 2) NOT NULL,
    total_deductions DECIMAL(10, 2) NOT NULL,
    net_salary DECIMAL(10, 2) NOT NULL,
    created_at DATETIME NOT NULL
);
```

## URL Routes

| URL | View | Name | Method | Purpose |
|-----|------|------|--------|---------|
| `/` | `dashboard` | `dashboard` | GET | Landing page |
| `/calculator/` | `calculator` | `calculator` | GET, POST | Form and results |
| `/admin/` | Django admin | - | GET, POST | Admin interface |

## Data Flow

### Calculation Flow
```
User Input (Form)
    ↓
SalaryCalculatorForm (validation)
    ↓
calculate_salary() (services.py)
    ↓
Result Dictionary
    ↓
Template Rendering (result.html)
    ↓
Browser Display
```

### Request Flow
```
Browser Request
    ↓
URL Routing (urls.py)
    ↓
View Function (views.py)
    ↓
Form Processing / Calculation
    ↓
Template Rendering
    ↓
HTTP Response
```

## Feature Matrix

| Feature | Phase 1 | Phase 2 | Phase 3+ |
|---------|---------|---------|----------|
| Calculation Engine | ✅ | ✅ | ✅ |
| Form Validation | ✅ | ✅ | ✅ |
| Database Model | ✅ | ✅ | ✅ |
| Admin Interface | ✅ | ✅ | ✅ |
| Dashboard UI | ❌ | ✅ | ✅ |
| Calculator Form UI | ❌ | ✅ | ✅ |
| Results Page UI | ❌ | ✅ | ✅ |
| Responsive Design | ❌ | ✅ | ✅ |
| Negative Salary Warning | ✅ | ✅ | ✅ |
| History Viewing | ❌ | ❌ | 🔮 |
| PDF Generation | ❌ | ❌ | 🔮 |
| Charts/Graphs | ❌ | ❌ | 🔮 |
| User Auth | ❌ | ❌ | 🔮 |
| API Endpoints | ❌ | ❌ | 🔮 |

Legend: ✅ Implemented | ❌ Not implemented | 🔮 Future

## Git Ignore Recommendations

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Django
*.log
db.sqlite3
db.sqlite3-journal
/media
/static/admin/

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

## Deployment Checklist (Future)

- [ ] Update SECRET_KEY
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up production database (PostgreSQL recommended)
- [ ] Configure static file serving (Whitenoise or CDN)
- [ ] Set up HTTPS
- [ ] Configure email backend
- [ ] Add security middleware
- [ ] Set up monitoring and logging
- [ ] Create deployment documentation

## Maintenance Notes

### Regular Tasks
- Run tests before deploying changes
- Keep dependencies updated (security patches)
- Review and clean test database periodically
- Monitor for Django security advisories

### Code Quality
- All monetary calculations use Decimal
- Server-side validation is source of truth
- No JavaScript allowed (project constraint)
- Follow Django best practices
- Write tests for new features

### Known Limitations
- Earlier Python 3.14 / Django 5.0.14 test-client incompatibility (resolved by Django 5.2.18 upgrade)
- No real-time validation (form submits for validation)
- No JavaScript-based interactivity
- Educational tool, not production payroll system
- No automatic tax calculations

## Support and Resources

### Documentation
- README.md - Main documentation
- QUICKSTART.md - Getting started guide
- PHASE2_COMPLETE.md - Implementation details

### Testing
- `python manage.py test calculator` - Run Phase 1 tests
- `python verify_phase2.py` - Manual Phase 2 verification

### Development Server
- `python manage.py runserver` - Start at http://127.0.0.1:8000/

## Version History

**Phase 1** (Complete)
- Core calculation engine
- Form validation
- Database model
- Admin interface
- 23 unit tests

**Phase 2** (Complete)
- Dashboard landing page
- Calculator form UI
- Results display page
- Green-and-white design system
- Responsive CSS
- View integration
- 5 view tests (manual verification)

**Phase 3** (Future)
- To be determined based on requirements

---

Last Updated: Sunday, October 11, 2026
Project Status: Phase 2 Complete ✅
