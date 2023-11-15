import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.write('Sudestada Forecast')

@st.cache_data
def load_data():
    df = pd.read_excel('data_for_presentation.xlsx')
    df['ds'] = pd.to_datetime(df['ds'])
    return df
df = load_data()

# Dropdown selection for sku_name
sku_names = df['sku_name'].unique()
selected_sku = st.selectbox('Select SKU', sku_names)

# Filter data based on selected SKU
filtered_by_sku = df[df['sku_name'] == selected_sku]

# Dropdown selection for department_id_name
departments = filtered_by_sku['department_id_name'].unique()
selected_department = st.selectbox('Select Department', departments)

# Filter data based on selected department
filtered_by_department = filtered_by_sku[filtered_by_sku['department_id_name'] == selected_department]

# Dropdown selection for category_id_name
categories = filtered_by_department['category_id_name'].unique()
selected_category = st.selectbox('Select Category', categories)

# Filter data based on selected category
filtered_by_category = filtered_by_department[filtered_by_department['category_id_name'] == selected_category]

# Dropdown selection for item_id_name
items = filtered_by_category['item_id_name'].unique()
selected_item = st.selectbox('Select Item', items)

# Filter data based on selected item
filtered_data = filtered_by_category[filtered_by_category['item_id_name'] == selected_item]

# Split data into actual and forecasted
actual_data = filtered_data[filtered_data['status'] == 'actual']
forecasted_data = filtered_data[filtered_data['status'] == 'forecast']

# Plotting the actual and forecasted data
if not (actual_data.empty or forecasted_data.empty):
	st.plotly_chart(px.line(filtered_data, x="ds" ,y='y', color='status'), use_container_width=True) 
else:
    st.warning('No data available for the selected item.')
