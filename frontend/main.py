import streamlit as st
from add_update_ui import add_update
from analytics_by_category_ui import get_analytics
from analytics_by_month_ui import get_analytics_by_month

st.set_page_config(page_title="Expense Tracking System", page_icon="../images/EPS.png")
st.image("../images/EPS.png",use_container_width=True)


tab1,tab2,tab3 = st.tabs(["Add/Update",'Analytics By Category','Analytics By Month'])


with tab1:
    add_update()

with tab2:
    get_analytics()

with tab3:
    st.subheader('Expense breakdown by Month')
    get_analytics_by_month()
