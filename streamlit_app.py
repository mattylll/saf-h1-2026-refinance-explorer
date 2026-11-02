import csv
import io
import pandas as pd
import streamlit as st
from model import calculate

REPORT = 'https://studentaccommodationfinance.co.uk/insights/h1-2026-student-accommodation-finance-report/'
METHOD = 'https://studentaccommodationfinance.co.uk/reports/h1-2026/methodology.md'
st.set_page_config(page_title='Student accommodation refinance explorer | SAF', page_icon='🧮', layout='wide')
st.caption('STUDENT ACCOMMODATION FINANCE  /  H1 2026 RESEARCH COMPANION')
st.title('When income and yield change together')
st.write('Explore how two valuation assumptions change the amount available to repay existing debt. Start with the report example, then change one assumption at a time.')
st.markdown(f'[Read the H1 2026 report]({REPORT}) · [Check the methodology]({METHOD})')
st.info('Educational scenarios only. The defaults are illustrative assumptions from the report, not current market yields, lender terms, a property valuation or a finance offer. Use hypothetical figures, not confidential property information.')

with st.sidebar:
    st.header('Scenario assumptions')
    st.caption('Amounts in GBP millions. Yield and LTV are percentages.')
    income_m = st.number_input('Annual net operating income (£m)', min_value=0.0, max_value=1000.0, value=0.9, step=0.05, format='%.2f')
    yield_pct = st.number_input('Capitalisation yield (%)', min_value=0.5, max_value=25.0, value=5.5, step=0.25)
    debt_m = st.number_input('Existing debt to repay (£m)', min_value=0.0, max_value=10000.0, value=12.0, step=0.5)
    cap_pct = st.number_input('Assumed maximum refinance LTV (%)', min_value=0.0, max_value=100.0, value=60.0, step=5.0)
    st.caption('These controls define a simplified scenario. The LTV limit is your assumption, not a lender commitment.')

result = calculate(income_m*1e6, yield_pct, debt_m*1e6, cap_pct)
base = calculate(1e6, 5.0, 12e6, 60.0)
money = lambda n: f'£{n/1e6:,.2f}m'
cols = st.columns(3)
cols[0].metric('Modelled property value', money(result['value']))
cols[1].metric('Refinance capacity at assumed LTV', money(result['capacity']))
cols[2].metric('Repayment gap before fees', money(result['gap']))
if result['ltv'] is None:
    st.write('At zero income the modelled value is zero. Existing-debt LTV is undefined.')
else:
    st.write(f"Existing debt / modelled value: **{result['ltv']:.1f}% LTV**.")
if result['headroom'] > 0:
    st.write(f"Capacity exceeds existing debt by **{money(result['headroom'])}** before costs. This is mathematical headroom, not approved cash release.")

st.subheader('Compare with the report baseline')
st.table(pd.DataFrame({
    'Measure':['Annual net operating income','Yield','Existing debt','Assumed refinance LTV','Modelled value','Refinance capacity','Repayment gap before fees'],
    'Report baseline':['£1.00m','5.0%','£12.00m','60.0%',money(base['value']),money(base['capacity']),money(base['gap'])],
    'Your scenario':[money(income_m*1e6),f'{yield_pct:.2f}%',money(debt_m*1e6),f'{cap_pct:.1f}%',money(result['value']),money(result['capacity']),money(result['gap'])]
}),hide_index=True)
st.caption('The report stress example uses £0.90m income and 5.5% yield: value £16.36m, existing-debt LTV 73.3%, capacity £9.82m and a £2.18m repayment gap at an assumed 60% LTV. Calculations use unrounded values.')

st.subheader('How sensitive is the gap to yield?')
st.write('This curve holds your income, debt and assumed LTV constant. It varies only the capitalisation yield over a deliberately illustrative range.')
yields = sorted(set([round(yield_pct*d,4) for d in [0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4]]))
curve=pd.DataFrame([{'Yield (%)':y,'Repayment gap (£m)':calculate(income_m*1e6,y,debt_m*1e6,cap_pct)['gap']/1e6} for y in yields])
st.line_chart(curve,x='Yield (%)',y='Repayment gap (£m)',color='#087f8c')
st.dataframe(curve,hide_index=True)

st.subheader('The calculation')
st.markdown('**Value = annual net operating income ÷ yield as a decimal.**\n\n**Refinance capacity = value × assumed LTV as a decimal.**\n\n**Repayment gap = maximum of zero and existing debt minus capacity.**')
st.write('Income falling and yield rising both reduce the modelled value. A lower value also reduces borrowing capacity when the assumed LTV is unchanged. This tool does not estimate income coverage constraints, fees, tax, amortisation, capital expenditure, lender reserves or transaction timing. Actual lending can be lower than the LTV-only capacity shown here.')

data = {'research_id':'SAF-H1-2026','model_version':'2026-11-02','annual_noi_gbp':income_m*1e6,'yield_pct':yield_pct,'existing_debt_gbp':debt_m*1e6,'assumed_refinance_ltv_pct':cap_pct,**result,'status':'Illustrative calculation, not lender terms','source':METHOD}
buf=io.StringIO(); writer=csv.writer(buf); writer.writerow(['field','value']); writer.writerows(data.items())
st.download_button('Download this scenario with assumptions (CSV)',buf.getvalue(),file_name='saf-illustrative-refinance-scenario.csv',mime='text/csv')
st.divider()
st.markdown(f'**Source and authorship.** Adapted from the illustrative valuation example in the [SAF-H1-2026 methodology]({METHOD}), published 12 September 2026. This interactive companion was prepared 2 November 2026; it adds no observed transactions or market forecasts.')
st.write('By Matt Lenzie for Student Accommodation Finance, with Construction Capital affiliation disclosed. This is commercially affiliated educational research. AI assisted implementation. Source report rights remain reserved. Inputs are processed by the hosted app to calculate the scenario; this code does not save them or request names, addresses or contact details.')

st.subheader('Keep scenarios and observed evidence separate')
st.markdown('For the report, data and presentation reading routes, use the [H1 research guide](https://sites.google.com/view/saf-h1-2026-research-guide/home). The [GitBook field reference](https://construction-capital.gitbook.io/student-accommodation-finance-data-reference/field-reference-and-exclusions) explains which observed measures can be compared. Neither resource turns this illustrative scenario into an observed loan or lender offer. These are companions to the same study, with common authorship and source evidence.')
