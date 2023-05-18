import streamlit as st

from gos.fte import tax_condition
from text_msg import tm

online_salary_condition = {
    'MarketingSp': {
        'salary': 150_000,
        'bonus': 30,
        'tax_index': 1,
        'fullname': 'Marketing Specialist',
        'fullname_rus': 'Маркетолог',
        'shortname': 'online_ms'},
    'PRT_Dir': {
        'salary': 500_000,
        'bonus': 0,
        'tax_index': 1,
        'fullname': 'PRT Direct',
        'fullname_rus': 'PRT - Директ',
        'shortname': 'online_prt_dir'},
    'PRT_Dev': {
        'salary': 300_000,
        'bonus': 0,
        'tax_index': 1,
        'fullname': 'PRT Development Specialist',
        'fullname_rus': 'PRT - Разработка и поддержание сайта',
        'shortname': 'online_prt_dev'},
    'Reputation': {
        'salary': 0,
        'bonus': 0,
        'tax_index': 1,
        'fullname': 'Reputation',
        'fullname_rus': 'Репутация',
        'shortname': 'online_rep'},
}


def create_online_fte_card(fte_data: dict):
    with st.expander(fte_data['fullname_rus']):
        col_salary, col_bonus = st.columns(2)
        with col_salary:
            st.number_input(label=tm.salary_label,
                            value=fte_data['salary'], format='%d',
                            min_value=0, step=5000,
                            help=tm.salary_help,
                            key=f"{fte_data['shortname']}_salary_gross")
        with col_bonus:
            st.number_input(label=tm.year_bonus_label,
                            value=fte_data['bonus'], format='%d',
                            min_value=0, step=1000,
                            help=tm.year_bonus_help,
                            key=f"{fte_data['shortname']}_bonus")
        with st.container():
            st.selectbox(label=tm.tax_type_label,
                         options=(i for i in tax_condition),
                         index=fte_data['tax_index'],
                         key=f"{fte_data['shortname']}_tax_type",
                         help=tm.tax_type_help)


def create_online_fte_section():
    st.header('FTE')
    with st.expander(label='Выберите ставки', expanded=False):
        st.multiselect(label='Выбрано',
                       options=(i for i in online_salary_condition),
                       default=(i for i in online_salary_condition if (i != 'Reputation')),
                       key='chosen_fte')
    for num, i in enumerate(st.session_state.chosen_fte):
        create_online_fte_card(online_salary_condition[i])
