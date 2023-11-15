import streamlit as st
import pandas as pd

st.write('Sudestada Forecast')

@st.cache_data
def load_data():
    df = pd.read_excel('data_for_presentation.xlsx')
    return df
df = load_data()
st.dataframe(df)