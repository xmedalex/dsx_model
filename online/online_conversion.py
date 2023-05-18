import streamlit as st


def create_conversion_section(total_coverage: int, total_conversion: int):
    st.header('Воронка')
    col1, col2 = st.columns(2)
    with col1:
        st.write('Покрытие')
    with col2:
        st.write(str(total_coverage))

    col1, col2 = st.columns(2)
    with col1:
        st.write('Перешли на сайт')
    with col2:
        st.write(str(total_conversion))

    st.slider(label='Переход на препарат', min_value=0, max_value=100,
              value=80, step=5, format='%d%%', key=f"home_to_drug")

    st.slider(label='Запись к врачу', min_value=0, max_value=100,
              value=40, step=5, format='%d%%', key=f"drug_to_specialist")

    st.slider(label='Покупка', min_value=0, max_value=100,
              value=10, step=5, format='%d%%', key=f"drug_to_buy")


