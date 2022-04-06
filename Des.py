import streamlit as st
from conn import sqlite as d
import pandas as pd
import matplotlib.pyplot as plt
from model.finance import Record

st.set_page_config(layout="wide")

conn = d.create_connection()
cats = ['Lifestyle', 'Food', 'Rent', 'Utilities', 'Tech', 'Subscriptions']
st.title('Personal expense tracker')


col1, col2, col3 = st.columns(3)

with col1:
    with st.form('Delete record'):
        d.delete_record(conn, st.text_input(label='Delete record', placeholder='ID of a record for deletion'))
        if st.form_submit_button('Delete'):
            st.success('Record deleted!')
    with st.form(key='Update record'):
        st.write('Update record')
        d.update_amount(conn, st.number_input('ID', min_value=0, step=1), st.number_input('Amount', min_value=0))
        if st.form_submit_button('Submit'):
            st.success('Record updated!')
    with st.form(key='Create record'):
        st.write('New record')
        i_cat = st.selectbox('Which category would you like to view?', cats)
        i_amount = st.number_input('Amount', min_value = 0)
        record_1 = Record(i_cat, i_amount)
        if st.form_submit_button('Confirm creation'):
            d.create_record(conn, record_1)
            st.success('New record created!')

with col2:
    data = pd.DataFrame(d.cat_overview(conn))
    data = data.rename(columns={0: 'Category', 1: 'Share in total'})
    data_all = pd.DataFrame(d.get_all(conn))
    data_all = data_all.rename(columns={0: 'ID', 1: 'Category', 2: 'Share in total'})
    if st.button('Get Percentage'):
        st.table(data.sort_values(by='Share in total', ascending=False))
    if st.button('Get all records'):
        st.table(data_all)
    if st.button('Close tabular view'):
        st.write('')
    with st.form('Isolated view'):
        selected_cat = st.selectbox('Which category would you like to view?', cats)
        iso_data = data_all[data_all['Category'] == selected_cat]
        iso_data = iso_data.rename(columns = {'Share in total': 'Amount'})
        if st.form_submit_button('Confirm selection'):
            st.dataframe(iso_data)

with col3:
    fig, ax = plt.subplots(figsize=(10,10), dpi = 100)
    ax.pie(data['Share in total'], labels = data['Share in total'], textprops= {'fontsize': 12})
    plt.title('Expenditure pattern %', size=26)
    ax.legend(data['Category'], loc ='lower center', ncol=4)
    st.pyplot(fig)
