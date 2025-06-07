import streamlit as st
import requests
import pandas as pd

URL = 'http://localhost:8000'

def get_analytics_by_month():
    response = requests.get(f'{URL}/month_analytics/')

    if response.status_code==200:
        data=response.json()
        df = pd.DataFrame({
            "Month_Num":[x['month_number'] for x in data],
            "Month_Name":[x['month_name'] for x in data],
            "Total":[x['total'] for x in data]
        })

        st.bar_chart(data=df.set_index("Month_Name")['Total'],x_label='Month',y_label='Total ₹ INR',width=0,height=0,use_container_width=True)
        # st.bar_chart(data=df,x="Month_Name",y='Total', color=(215, 150, 0), y_label='Total INR', width=0,
        #              height=0, use_container_width=True)

        df['Total']=df['Total'].map("{:.2f}".format)
        st.table(data=df.set_index("Month_Num"))


    else:
        st.error('Failed to retrieve')