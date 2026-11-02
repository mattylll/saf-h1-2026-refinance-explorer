# SAF illustrative refinance explorer

Educational interactive companion to [SAF-H1-2026](https://studentaccommodationfinance.co.uk/insights/h1-2026-student-accommodation-finance-report/), published 12 September 2026. App prepared 2 November 2026 by Matt Lenzie for Student Accommodation Finance, with Construction Capital affiliation. AI assisted implementation.

The [source methodology](https://studentaccommodationfinance.co.uk/reports/h1-2026/methodology.md) supplies the illustrative baseline and stress example. This app adds scenario exploration, not new research observations or market forecasts.

Value = annual net operating income / yield. Refinance capacity = value × assumed LTV. Gap = max(0, existing debt minus capacity). It excludes income-coverage constraints, fees, tax, capital expenditure, amortisation and reserves. This is not a valuation, advice or a lender offer. Use hypothetical inputs.

Run with Python 3.12:

```sh
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The code does not save inputs or request personal information. Hosting still processes input values to run the app. Public source and report rights remain reserved; no general licence to reuse or adapt is granted by this publication. No private research records or secrets are included.
