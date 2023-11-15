import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

st. set_page_config(layout="wide")
st.title('Sudestada Forecast')

@st.cache_data
def load_data():
    df = pd.read_excel('data_for_presentation.xlsx')
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.rename(columns={'ds': 'date', 'y': 'quantity'})
    return df

def calculate_accuracy(actual, predicted):
    mask = actual != 0  # avoid divide by zero errors
    return 100 - np.mean(np.abs((actual - predicted)[mask] / actual[mask])) * 100

df = load_data()
_1_column, _2_column, _3_column, _4_column = st.columns(4)

# Dropdown selection for sku_name
sku_names = df['sku_name'].unique()
with _1_column:
	selected_sku = st.selectbox('SKU', sku_names)

# Filter data based on selected SKU
filtered_by_sku = df[df['sku_name'] == selected_sku]

# Dropdown selection for department_id_name
departments = filtered_by_sku['department_id_name'].unique()
with _2_column:
	selected_department = st.selectbox('Department', departments)

# Filter data based on selected department
filtered_by_department = filtered_by_sku[filtered_by_sku['department_id_name'] == selected_department]

# Dropdown selection for category_id_name
categories = filtered_by_department['category_id_name'].unique()
with _3_column:
	selected_category = st.selectbox('Category', categories)

# Filter data based on selected category
filtered_by_category = filtered_by_department[filtered_by_department['category_id_name'] == selected_category]

# Dropdown selection for item_id_name
items = filtered_by_category['item_id_name'].unique()
with _4_column:
	selected_item = st.selectbox('Item', items)

# Filter data based on selected item
filtered_data = filtered_by_category[filtered_by_category['item_id_name'] == selected_item]

# Split data into actual and forecasted
actual_data = filtered_data[filtered_data['status'] == 'actual']
forecasted_data = filtered_data[filtered_data['status'] == 'forecast']

# Plotting the actual and forecasted data
if not (actual_data.empty or forecasted_data.empty):
	merged = pd.merge(actual_data, forecasted_data, on=['date'], suffixes=('_actual', '_forecast'), how='inner')
	accuracy = calculate_accuracy(
		merged['quantity_actual'].values.reshape(-1),
		merged['quantity_forecast'].values.reshape(-1),
	)	
	fig = px.line(
			filtered_data, x="date" ,y='quantity', color='status', 
			color_discrete_sequence=["green", "orange"],
			title="Model: {}; \t Accuracy: {} %".format(filtered_data.iloc[0]['model_name'], round(accuracy, 2))
		)
	st.plotly_chart(fig, use_container_width=True)

else:
    st.warning('No data available for the selected item.')
