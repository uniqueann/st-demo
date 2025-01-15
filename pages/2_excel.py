import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder,AgGrid

st.write('仅读取第一个sheet表')
uploaded_file = st.file_uploader('请上传 XLSX 文件',type=['xlsx'])

if uploaded_file is None:
    st.stop()

@st.cache_data
def load_data(file):
    return pd.read_excel(uploaded_file)

df = load_data(uploaded_file)
st.data_editor(df)

dfs = load_data(uploaded_file)

