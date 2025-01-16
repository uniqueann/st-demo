import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder,AgGrid

st.set_page_config(layout="wide")

st.subheader('仅读取第一个sheet表',divider=True)
uploaded_file = st.file_uploader('请上传 XLSX 文件',type=['xlsx'])

if uploaded_file is None:
    st.stop()

@st.cache_data
def load_data(file):
    return pd.read_excel(uploaded_file)

df = load_data(uploaded_file)

column_names = df.columns.tolist()
st.write(column_names)

st.data_editor(df)


