import streamlit as st
from datetime import datetime
import requests
import pandas as pd

URL = 'http://localhost:8000'

def get_analytics():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date',datetime(2024,8,1))
    with col2:
        end_date = st.date_input('End Date',datetime(2024,8,5))

    button = st.button('Get Analytics')
    if button:
        payload={
            'start_date':start_date.strftime("%Y-%m-%d"),
            'end_date':end_date.strftime("%Y-%m-%d")
        }

        response=requests.post(f'{URL}/analytics',json=payload)
        response=response.json()

        data = {
            "Category":list(response.keys()),
            "Total":[response[category]['total'] for category in response],
            "Percentage": [response[category]['percentage'] for category in response]
        }

        df = pd.DataFrame(data)
        sorted_df = df.sort_values(by='Percentage',ascending=False)
        st.subheader('Expense breakdown by Category')

        st.bar_chart(data=sorted_df.set_index("Category")['Percentage'],x_label='Category',y_label='Percentage %',width=0,height=0,use_container_width=True)

        sorted_df['Total']=sorted_df['Total'].map("{:.2f}".format)
        sorted_df['Percentage'] = sorted_df['Percentage'].map("{:.2f}".format)

        st.table(sorted_df)
