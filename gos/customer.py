from dataclasses import dataclass

import streamlit as st
import pandas as pd

columns = ['districts', 'accounts_number']
districts_data = [
    ['ВАО', 14],
    ['ЗАО', 14],
    ['САО', 11],
    ['СВАО', 14],
    ['СЗАО', 6],
    ['ЦАО', 10],
    ['ЮВАО', 24],
    ['ЮЗАО', 16],
    ['ЮАО', 20]
]


@dataclass
class CustomerInitialValue:
    initiation: int = 150_000
    support: int = 30_000
    agency_fee: int = 10
    packs_per_week: int = 4
    monthly_growth = 10


customer = CustomerInitialValue()


def customer_container():
    @st.cache_data
    def load_districts_data() -> pd.DataFrame:
        return pd.DataFrame(districts_data, columns=columns)

    districts = load_districts_data()

    st.header('B2B-клиенты')
    with st.expander('**Территория:**'):
        st.multiselect(label=f'Выберите округа для расчета:',
                       options=districts['districts'].tolist(),
                       default=districts['districts'].tolist(),
                       key='selected_districts')

        col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            counts_sum = districts.loc[
                districts['districts'].isin(st.session_state.selected_districts), 'accounts_number'].sum()
            st.slider("Активных учреждений в промоции", 1, int(counts_sum), int((counts_sum * 0.1)),
                      key='active_accounts_number',
                      help='Выберите из общего количества учреждений те, которые будут находиться в активной работе')

    with st.expander('**OPEX на одно учреждение**'):
        with st.container():
            col_initiation, col_support = st.columns([1, 1])
            with col_initiation:
                st.number_input(label='Инициация', min_value=1,
                                value=customer.initiation,
                                step=10000,
                                key='initial_event',
                                help='ОПЕКС начального мероприятия, руб. с НДС. В первом квартале, один раз')
            with col_support:
                st.number_input(label='Поддержание', min_value=1,
                                value=customer.support,
                                step=1000,
                                key='supporting_OPEX',
                                help='OPEX поддерживающих активностей, руб. с НДС. Каждый квартал Q2-Q4, 3 в год')
    with st.expander('**Поддерживающие расходы**'):
        with st.container():
            col1, col2, col3 = st.columns([1, 8, 1])
            with col2:
                st.slider(label='Поддержание, %', min_value=1, max_value=30,
                          value=customer.agency_fee,
                          step=1,
                          format='%d%%', key='agency_fee')
    # sliders with pack per account and pack growth
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.slider(label="Упак. в нед. в одном ЛПУ",
                      min_value=1,  max_value=24,
                      value=customer.packs_per_week,
                      step=1,
                      key='patients_per_one_account_per_week',
                      help='В одном ЛПУ 8 врачей в две смены (4 по 2), часть из них работает в обе смены.'
                           'Среднее количество врачей для расчета - 6. В первый месяц - 25% от выбранного кол-ва, '
                           'второй - 50%, третий - 75%. Со второго квартала - 100% от планового кол-ва.')
        with col2:
            st.slider("Прирост упак. (мес-к-мес)", min_value=0, max_value=50,
                      value=customer.monthly_growth,
                      key='pack_growth',
                      help='Расчетный прирост продаж со второго квартала, каждый последующий месяц',
                      format='%d%%')

    with st.container():
        packs_per_month = st.session_state.active_accounts_number * \
                          st.session_state.patients_per_one_account_per_week * \
                          4
        packs_jan_to_apr = [int(packs_per_month / 4), int(packs_per_month / 2),
                            int(packs_per_month / 4 * 3), int(packs_per_month)]
        packs_apr_to_dec = [
            int(packs_per_month * (1 + st.session_state.pack_growth / 100) ** i) for i in range(4, 12)
        ]
        packs = packs_jan_to_apr + packs_apr_to_dec
        packs_sum = sum(packs)
        sum_a = f"{packs_sum:,}".replace(',', ' ')
        st.write(f"Всего упаковок за год: {sum_a}")

    return packs
