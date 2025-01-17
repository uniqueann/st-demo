import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder,AgGrid

st.set_page_config(layout="wide")

uploaded_file = st.file_uploader('请上传 XLSX 文件,仅读取第一个sheet表',type=['xlsx'],label_visibility="visible")

if uploaded_file is None:
    st.stop()

@st.cache_data
def load_data(file):
    return pd.read_excel(uploaded_file)

df = load_data(uploaded_file)

column_names = df.columns.tolist()
with st.expander("列名集合", expanded=True, icon=":material/view_column:"):
    display_columns  = st.pills("列名",column_names, selection_mode='multi',default=column_names,label_visibility='hidden')

if display_columns :
    # st.markdown(f"{display_columns }")
    with st.expander("设置-Setting", expanded=False, icon=":material/settings:"):
        st.markdown("this is setting markdown")
        for col in display_columns:
            col1,col2,col3 = st.columns(3, vertical_alignment="center", border=True)
            with col1:
                st.html(f"<b>{col}</b>")
            with col2:
                st.checkbox("清洗数据", key=f"{col}_1")
            with col3:
                st.checkbox("展示为图片", key=f"{col}_2")

    display_df = df[display_columns]
    st.data_editor(display_df)
else:
    st.warning('请选择列名')