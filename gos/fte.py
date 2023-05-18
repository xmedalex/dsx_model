import streamlit as st

from text_msg import tm

ftes_salary_conditions = {
    'MedRep': {
        'salary': 100000,
        'tax_index': 0,
        'fullname': 'Medical Representative',
        'fullname_rus': 'Медицинский представитель',
        'shortname': 'mr',
        'bonus_quarter': 20,
        'bonus_year': 30,
        'compensation': 25000,
    },
    'ProdMan': {
        'salary': 1,
        'tax_index': 0,
        'fullname': 'Product Manager',
        'fullname_rus': 'Продакт Менеджер',
        'shortname': 'pm',
        'bonus_quarter': 1,
        'bonus_year': 1,
        'compensation': 1,
    },
    'ComDir': {
        'salary': 1,
        'tax_index': 0,
        'fullname': 'Commercial Director',
        'fullname_rus': 'Коммерческий директор',
        'shortname': 'cd',
        'bonus_quarter': 1,
        'bonus_year': 1,
        'compensation': 1,
    },
}

tax_condition = {
    'ФизЛицо': 15,
    'ЮрЛицо': 0,
}


# FTE section
def fte_container():
    def create_fte_card(fte_data: dict):
        with st.expander(fte_data['fullname_rus']):
            with st.container():
                col_salary, col_compensation = st.columns(2)
                with col_salary:
                    st.number_input(label=tm.salary_label,
                                    value=fte_data['salary'], format='%d',
                                    min_value=1, step=5000,
                                    help=tm.salary_help,
                                    key=f"{fte_data['shortname']}_salary_gross")
                with col_compensation:
                    st.number_input(label=tm.compensation_label,
                                    value=fte_data['compensation'], format='%d',
                                    min_value=1, step=1000,
                                    help=tm.compensation_help,
                                    key=f"{fte_data['shortname']}_compensation")
            with st.container():
                quarter_bonus_col, year_bonus_col, taxation_type_col = st.columns(3)
                with quarter_bonus_col:
                    st.number_input(label=tm.quarter_bonus_label,
                                    value=fte_data['bonus_quarter'], format='%d',
                                    min_value=1, step=5,
                                    help=tm.quarter_bonus_help,
                                    key=f"{fte_data['shortname']}_quarter_bonus")
                with year_bonus_col:
                    st.number_input(label=tm.year_bonus_label,
                                    value=fte_data['bonus_year'], format='%d',
                                    min_value=1, step=5,
                                    help=tm.year_bonus_help,
                                    key=f"{fte_data['shortname']}_year_bonus")
                with taxation_type_col:
                    st.selectbox(label=tm.tax_type_label,
                                 options=(i for i in tax_condition),
                                 index=fte_data['tax_index'],
                                 key=f"{fte_data['shortname']}_tax_type",
                                 help=tm.tax_type_help)

    st.header('FTE')
    with st.expander(label='Выберите ставки', expanded=False):
        st.multiselect(label='Выбрано',
                       options=(i for i in ftes_salary_conditions),
                       default=(i for i in ftes_salary_conditions if (i != 'ProdMan' and i != 'ComDir')),
                       key='chosen_fte')
    for num, i in enumerate(st.session_state.chosen_fte):
        create_fte_card(ftes_salary_conditions[i])
    with st.container():
        col_a, col_b, col_c = st.columns([1, 10, 1])
        with col_b:
            st.slider("Кол-во медицинских представителей", 1, 9, 1, 1,
                      key='medreps_number',
                      help='Выберите количество медицинских представителей в штате')
