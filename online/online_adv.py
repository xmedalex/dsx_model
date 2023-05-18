import streamlit as st

online_source = {
    'Yandex': {
        'monthly_cost': 100_000,
        'audience_coverage': 10_000,
        'conversion': 10,
        'fullname': '',
        'fullname_rus': 'Yandex',
        'shortname': 'yandex',
    },
    'VK': {
        'monthly_cost': 100_000,
        'audience_coverage': 10_000,
        'conversion': 10,
        'fullname': '',
        'fullname_rus': 'Вконтакте',
        'shortname': 'vk',
    },
    'OK': {
        'monthly_cost': 100_000,
        'audience_coverage': 10_000,
        'conversion': 10,
        'fullname': '',
        'fullname_rus': 'Одноклассники',
        'shortname': 'ok',
    },
    'Instagram': {
        'monthly_cost': 100_000,
        'audience_coverage': 10_000,
        'conversion': 10,
        'fullname': '',
        'fullname_rus': 'Инстаграмм (экстремистская орг.)',
        'shortname': 'insta',
    },
    'Youtube': {
        'monthly_cost': 100_000,
        'audience_coverage': 10_000,
        'conversion': 10,
        'fullname': '',
        'fullname_rus': 'Youtube',
        'shortname': 'youtube',
    }
}


def create_online_source_card(card: dict):
    with st.expander(card['fullname_rus']):
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.number_input(label="Ежемес. стоимость",
                                value=card['monthly_cost'], format='%d',
                                min_value=0, step=10_000,
                                help='',
                                key=f"{card['shortname']}_online_monthly_cost")
            with col2:
                st.number_input(label='Охват',
                                value=card['audience_coverage'], format='%d',
                                min_value=0, step=1_000,
                                help='',
                                key=f"{card['shortname']}_online_coverage")
        with st.container():
            st.slider(label='Конверсия в переходы на сайт, %', min_value=0, max_value=100,
                      value=card['conversion'], step=1,
                      format='%d%%', key=f"{card['shortname']}_online_conversion")


def create_online_source_section():
    st.header('Размещение рекламы')
    with st.expander(label='Выберите площадку', expanded=False):
        st.multiselect(label='Выбрано',
                       options=(i for i in online_source),
                       default=(i for i in online_source if i not in ('Youtube', 'Instagram')),
                       key='chosen_online_source')
    for num, i in enumerate(st.session_state.chosen_online_source):
        create_online_source_card(online_source[i])
