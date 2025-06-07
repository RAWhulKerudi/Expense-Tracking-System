import streamlit as st
from datetime import datetime
import requests

URL = 'http://localhost:8000'

categories = ['Shopping','Rent','Food','Entertainment','Other']

def add_update():
    selected_date = st.date_input('Enter date',datetime(2024,8,1),label_visibility='collapsed')
    response = requests.get(f'{URL}/expenses/{selected_date}')
    if response.status_code == 200:
        expenses=response.json()
    else:
        st.error('Failed to retrieve')
        expenses=[]

    with st.form('expense_form'):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Amount')
        with col2:
            st.subheader('Category')
        with col3:
            st.subheader('Notes')

        new_expenses = []
        for i in range(5):
            # col1,col2,col3 = st.columns(3)
            if i < len(expenses):
                amount = expenses[i]['amount']
                category = expenses[i]['category']
                notes = expenses[i]['notes']
            else:
                amount = 0.0
                category = 'Shopping'
                notes = ''
            with col1:
                num_input = st.number_input(label='Enter',min_value=0.0,step=1.0,value=amount,label_visibility='collapsed',key=f'amount_{i}')
            with col2:
                cat_input = st.selectbox(label='Category',options=categories,index=categories.index(category),key=f'category_{i}',label_visibility='collapsed')
            with col3:
                note_input = st.text_input(label='Notes',key=f'notes_{i}',value=notes,label_visibility='collapsed')

            new_expenses.append({
                'amount': num_input,
                'category': cat_input,
                'notes': note_input
            }
            )

        submit = st.form_submit_button('Submit')
        if submit:
            filtered_expenses=[exp for exp in new_expenses if exp['amount']>0]
            response = requests.post(f'{URL}/expenses/{selected_date}',json=filtered_expenses)

            if response.status_code==200:
                st.success('Data inserted successfully')
            else:
                st.error('Error occurred...')
