from dataclasses import dataclass

import streamlit as st

from text_msg import tm


@dataclass
class DrugInitialValue:
    pharmacy_price: int = 5000
    owner_to_pharmacy_price: int = 3500
    manufacturer_to_owner_price = 1500


drug = DrugInitialValue()


def drug_container():
    st.header('Упаковка')
    pharmacy_price = drug.pharmacy_price
    if 'pack_price_pharmacy' in st.session_state:
        pharmacy_price = (1 + st.session_state.pack_price_pharmacy_change / 100) * pharmacy_price
    st.number_input(label=tm.pack_price_pharmacy_label,
                    value=int(pharmacy_price),
                    min_value=1, step=100, format='%d',
                    help=tm.pack_price_pharmacy_help,
                    key='pack_price_pharmacy')

    owner_to_pharmacy_price = drug.owner_to_pharmacy_price
    if 'pack_price_owner' in st.session_state:
        owner_to_pharmacy_price = (1 + st.session_state.pack_price_pharmacy_change / 100) * owner_to_pharmacy_price
    st.number_input(label=tm.pack_price_owner_label,
                    value=int(owner_to_pharmacy_price),
                    min_value=1, step=100, format='%d',
                    help=tm.pack_price_owner_help,
                    key='pack_price_owner')

    man_to_own_price = drug.manufacturer_to_owner_price
    st.number_input(label=tm.pack_price_manufacturer_label,
                    value=man_to_own_price,
                    min_value=1, step=100, format='%d',
                    help=tm.pack_price_manufacturer_help,
                    key='pack_price_manufacturer')

    st.slider(label=tm.pack_price_change_label,
              value=0,
              min_value=-30, max_value=30, step=5, format='%d%%',
              help=tm.pack_price_change_help,
              key='pack_price_pharmacy_change')
