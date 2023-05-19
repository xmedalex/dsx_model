import streamlit as st
import plotly.graph_objects as go

from gos.fte import tax_condition
from online.online_adv import create_online_source_section, online_source
from online.online_conversion import create_conversion_section
from online.online_fte import create_online_fte_section, online_salary_condition

st.set_page_config(layout="wide")

# контейнер с блоком ввода переменных
with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        create_online_fte_section()

    with col2:
        create_online_source_section()

    coverage = [st.session_state[i] for i in st.session_state if 'coverage' in i]
    total_coverage = int(sum(coverage))
    conversion = [st.session_state[i] for i in st.session_state if 'conversion' in i]
    total_conversion = int(sum([x * y / 100 for x, y in zip(coverage, conversion)]))

    with col3:
        create_conversion_section(total_coverage, total_conversion)

final_salary, final_bonus = [], []
for i in st.session_state.chosen_fte:
    shortname = online_salary_condition[i]['shortname']
    tax_chosen = st.session_state[f'{shortname}_tax_type']
    tax = tax_condition[tax_chosen]

    salary = st.session_state[f'{shortname}_salary_gross']
    bonus = st.session_state[f'{shortname}_bonus']

    gross_salary = salary / (1 - tax / 100)
    gross_bonus = gross_salary * bonus / 100 * (1 - tax / 100)

    final_salary.append(gross_salary)
    final_bonus.append(gross_bonus)
salary = int(sum(final_salary)/1_000)
bonus = int(sum(final_bonus)/1_000)

final_adv = []
for i in st.session_state.chosen_online_source:
    shortname = online_source[i]['shortname']
    gross = st.session_state[f'{shortname}_online_monthly_cost']
    final_adv.append(gross)
adv_gross = int(sum(final_adv)/1_000)

packs = total_conversion * \
        st.session_state.home_to_drug / 100 * \
        st.session_state.drug_to_specialist / 100 * \
        st.session_state.drug_to_buy / 100

st.header(f"Всего упаковок: {int(packs)}")
revenue = int((packs * 3_500)/1_000)
COGS = int(packs * 1_500 / 1_000)
profit = revenue - COGS - salary - bonus - adv_gross

fig = go.Figure(go.Waterfall(
            name="20", orientation="v",
            measure=["absolute",
                     "relative", "relative", "relative", 'relative',
                     # "total",
                     ],
            x=['revenue',
               'COGS', 'salary', 'bonus', 'adv_gross'
               # 'profit'
               ],
            textposition="outside",
            text=[revenue,
                  -COGS, -salary, -bonus, -adv_gross,
                  # profit
                  ],
            y=[revenue,
               -COGS, -salary, -bonus, -adv_gross,
               # profit
               ],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))

title_dir = "Общая прибыль" if profit > 0 else "Общий убыток"
sum_a = f"{profit:,}".replace(',', ' ')
title = f"{title_dir}:   {sum_a} тыс. руб"
st.subheader(title)
min_b = 2 * min(revenue, -COGS, -salary, -adv_gross, profit)
max_b = 2 * max(revenue, -COGS, -salary, -adv_gross, profit)
fig.update_layout(
    title="P&L за один месяц",
    yaxis_range=[min_b, max_b],
    showlegend=False)
st.plotly_chart(fig, use_container_width=False)