import io

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from gos.customer import customer_container
from gos.drug import drug_container
from gos.fte import fte_container, ftes_salary_conditions, tax_condition
from text_msg import month_name

st.set_page_config(layout="wide")

# контейнер с блоком ввода переменных
with st.container():
    col1, col2, col3 = st.columns([1, 2, 2])

    with col1:
        drug_container()

    with col2:
        fte_container()

    with col3:
        packs = customer_container()


def calculate_salary() -> list:
    # make dictionary with FTE salary, bonuses and compensations
    ftes_salary_final = {}
    for fte_role in st.session_state.chosen_fte:
        fte_shortname = ftes_salary_conditions[fte_role]['shortname']
        fte_salary_monthly = st.session_state.get(f"{fte_shortname}_salary_gross")
        fte_tax_type = st.session_state.get(f"{fte_shortname}_tax_type")
        fte_tax = tax_condition.get(fte_tax_type)

        ftes = 1 if fte_shortname != 'mr' else st.session_state.medreps_number
        ftes_salary_final[fte_role] = {}

        # salary calculation
        salary = [fte_salary_monthly / (1 - fte_tax / 100) for i in range(12)]
        if fte_shortname == 'mr':
            salary = [i * ftes for i in salary]
        ftes_salary_final[fte_role]['salary'] = salary

        # compensation calculation
        compensation_monthly = st.session_state.get(f"{fte_shortname}_compensation") / (1 - fte_tax / 100)
        compensation = [compensation_monthly * ftes for i in range(12)]
        ftes_salary_final[fte_role]['compensation'] = compensation

        # quarter bonus calculation
        quarter_bonus = st.session_state.get(f"{fte_shortname}_quarter_bonus")
        bonus_quarter = fte_salary_monthly * 3 * (quarter_bonus / 100) / (1 - fte_tax / 100)
        bonus_quarter_total = []
        for i in range(12):
            if i == 2 or i == 5 or i == 8 or i == 11:
                bonus_quarter_total.append(bonus_quarter * ftes)
            else:
                bonus_quarter_total.append(0)
        ftes_salary_final[fte_role]['bonus_quarter'] = bonus_quarter_total

        # year bonus calculation
        year_bonus = st.session_state.get(f"{fte_shortname}_year_bonus")
        bonus_year = fte_salary_monthly * 12 * (year_bonus / 100) / (1 - fte_tax / 100)
        bonus_year_total = []
        for i in range(12):
            if i == 11:
                bonus_year_total.append(bonus_year * ftes)
            else:
                bonus_year_total.append(0)
        ftes_salary_final[fte_role]['bonus_year'] = bonus_year_total

    salary_arr = np.array([0.0])
    compensation_arr = np.array([0] * 12)
    bonus_quarter_arr = np.array([0] * 12)
    bonus_year_arr = np.array([0] * 12)

    for i in ftes_salary_final:
        salary_arr = salary_arr + np.array(ftes_salary_final[i]['salary'])
        compensation_arr = compensation_arr + np.array(ftes_salary_final[i]['compensation'])
        bonus_quarter_arr = bonus_quarter_arr + np.array(ftes_salary_final[i]['bonus_quarter'])
        bonus_year_arr = bonus_year_arr + np.array(ftes_salary_final[i]['bonus_year'])
    return [salary_arr, compensation_arr, bonus_quarter_arr, bonus_year_arr]


salary_arr, compensation_arr, bonus_quarter_arr, bonus_year_arr = calculate_salary()

# calculation of drug cost
price_cor_coef = (1 + st.session_state.pack_price_pharmacy_change / 100)
revenue_without_VAT_list = [i * st.session_state.pack_price_owner * price_cor_coef for i in packs]
cogs_without_VAT_list = [i * st.session_state.pack_price_manufacturer for i in packs]
# Customers OPEX
agency_fee_list = [st.session_state.pack_price_pharmacy * price_cor_coef * i * st.session_state.agency_fee / 100 for i
                   in packs]

initial_event_total = st.session_state.initial_event * st.session_state.active_accounts_number
initial_per_month = initial_event_total / 3
initial_event_OPEX_list = [int(initial_per_month) for i in range(3)] + [0 for i in range(3, 12)]

supporting_OPEX_total = st.session_state.supporting_OPEX * st.session_state.active_accounts_number
supporting_OPEX_monthly = supporting_OPEX_total / 9
supporting_OPEX_list = [0 for i in range(3)] + [int(supporting_OPEX_monthly) for i in range(3, 12)]


def transform_list(a: list, reverse_sign: bool = True, kilo_view: bool = True) -> list:
    divider = 1000 if kilo_view else 1
    return [-int(i / divider) for i in a] if reverse_sign else [int(i / divider) for i in a]


df = pd.DataFrame({'date': pd.date_range(start='1/1/2024', freq='M', periods=12),
                   'packs': transform_list(packs, reverse_sign=False, kilo_view=False),
                   'revenue': transform_list(revenue_without_VAT_list, reverse_sign=False),
                   'COGS': transform_list(cogs_without_VAT_list),
                   'salary': transform_list(salary_arr),
                   'repr_exp': transform_list(compensation_arr),
                   'bonus_Q': transform_list(bonus_quarter_arr),
                   'bonus_Y': transform_list(bonus_year_arr),
                   'support_fee': transform_list(agency_fee_list),
                   'initial_event': transform_list(initial_event_OPEX_list),
                   'supporting_opex': transform_list(supporting_OPEX_list)}
                  )

df['date'] = df['date'].dt.date
df['expenses'] = df['COGS'] + df['salary'] + df['repr_exp'] + df['bonus_Q'] \
                 + df['bonus_Y'] + df['initial_event'] + df['support_fee'] + df['supporting_opex']
df['profit'] = df['revenue'] + df['expenses']
df['rolling_profit'] = df['profit'].cumsum()

packs_sum = df['packs'].sum()
revenue_sum = df['revenue'].sum()
COGS_sum = df['COGS'].sum()
salary_sum = df['salary'].sum()
compensation_sum = df['repr_exp'].sum()
bonus_quarter_sum = df['bonus_Q'].sum()
bonus_year_sum = df['bonus_Y'].sum()
agency_fee_sum = df['support_fee'].sum()
initial_event_sum = df['initial_event'].sum()
supporting_opex_sum = df['supporting_opex'].sum()
profit_sum = df['profit'].sum()

st.write('---')
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = go.Figure(go.Waterfall(
            name="20", orientation="v",
            measure=["absolute",
                     "relative", "relative", "relative", "relative",
                     "relative", "relative", "relative", "relative",
                     "total",
                     ],
            x=['revenue',
               'COGS', 'salary', 'repr_exp', 'bonus_Q', 'bonus_Y',
               'support_fee', 'initial_event', 'supporting_opex', 'profit'],
            textposition="outside",
            text=[revenue_sum, COGS_sum, salary_sum, compensation_sum, bonus_quarter_sum, bonus_year_sum,
                  agency_fee_sum, initial_event_sum, supporting_opex_sum, profit_sum],
            y=[revenue_sum, COGS_sum, salary_sum, compensation_sum, bonus_quarter_sum, bonus_year_sum,
               agency_fee_sum, initial_event_sum, supporting_opex_sum, profit_sum],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))

        title_dir = "Общая прибыль" if profit_sum > 0 else "Общий убыток"
        sum_a = f"{profit_sum:,}".replace(',', ' ')
        title = f"{title_dir}:   {sum_a} тыс. руб"
        st.subheader(title)
        min_b = -10000 if profit_sum > 0 else profit_sum * 1.8
        max_b = revenue_sum * 1.2
        fig.update_layout(
            title="P&L 2024",
            yaxis_range=[min_b, max_b],
            showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("По месяцам")
        rev_prof, prof, packs = st.tabs(['Выручка/прибыль', 'Прибыль', 'Упаковки'])
        with rev_prof:
            profit_list = df['profit'].tolist()

            x = month_name

            fig = go.Figure(go.Bar(x=x, y=profit_list, name='Profit'))
            fig.add_trace(go.Bar(x=x, y=transform_list(revenue_without_VAT_list, reverse_sign=False), name='Revenue'))

            markers, line = fig.data
            fig.data = line, markers

            min_a = min(profit_list) * 1, 5
            max_a = max(revenue_without_VAT_list) * 1, 5

            # fig.update_layout(barmode='stack')
            fig.update_layout(
                title="тыс. руб. без НДС",
                yaxis_range=[min_a, max_a],
                showlegend=False)
            st.plotly_chart(fig, use_container_width=False)
        with prof:
            fig = go.Figure(go.Waterfall(
                name="20", orientation="v",
                measure=["relative", "relative", "relative", "relative", "relative", 'relative',
                         "relative", "relative", "relative", "relative", "relative", "relative"
                                                                                     "total"],
                x=[*month_name, 'total'],
                textposition="outside",
                text=[*df['profit'].tolist(), profit_sum],
                y=[*df['profit'].tolist(), -profit_sum],
                # decreasing={"marker": {"color": "Maroon"}},
                # increasing={"marker": {"color": "Teal"}},
                # totals = {"marker":{"color":"red"}} if profit_sum < 0 else {"marker":{"color":"green"}},
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))

            # title_dir = "Общая прибыль" if profit_sum > 0 else "Общий убыток"
            # sum_a = f"{profit_sum:,}".replace(',', ' ')
            # title = f"{title_dir}:   {sum_a} тыс. руб"
            # st.subheader(title)

            fig.update_layout(
                # title="Прибыль по ме",
                yaxis_range=[min(df['profit']) * 4, max(df['profit']) * 4],
                showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with packs:
            packs_sum_str = f"{packs_sum:,}".replace(',', ' ')
            x = month_name

            fig = go.Figure(go.Bar(x=x, y=df['packs'].tolist(), name='Profit',
                                   text=df['packs'].tolist()))
            # fig.add_trace(go.Bar(x=x, y=transform_list(revenue_without_VAT_list, reverse_sign=False), name='Revenue'))

            # markers, line = fig.data
            # fig.data = line, markers

            min_a = -100
            max_a = max(df['packs']) * 1.3

            # fig.update_layout(barmode='stack')
            fig.update_layout(
                title=f'Всего упаковок: {packs_sum_str}',
                yaxis_range=[min_a, max_a],
                showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

st.write('---')
st.header('Исходные данные. Суммы указаны в тыс. рублей')

# df.loc['Column_Total']= df.sum(numeric_only=True, axis=0)


df.loc[df.shape[0]] = [np.nan for col_num in range(1, df.shape[1] + 1)]
df.iloc[df.shape[0] - 1,
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]] = df.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]].sum(axis=0)
df.at[12, 'rolling_profit'] = ''
df.at[12, 'date'] = 'Итого'
df = df.set_index('date')
# df.columns = ['дата', 'выручка', 'COGS', 'оклад', 'предст.расх.', 'бонус кв.', 'бонус год',
#                'поддерж. OPEX', 'initial_event', 'supporting_opex', 'прибыль', 'прибыль_']

st.write(df)

buffer = io.BytesIO()

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Sheet1')

st.download_button(label="Download Excel worksheets", data=buffer,
                   file_name="Model.xlsx", mime="application/vnd.ms-excel")
