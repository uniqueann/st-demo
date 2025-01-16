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
            pop_label = col
            pop = st.popover(pop_label)
            clear = pop.checkbox("清洗数据",False,key=f"{col}_1")
            if clear:
                pop_label = f"{col}: 清洗数据"
            pop.checkbox("展示为图片", False,key=f"{col}_2")
    display_df = df[display_columns]
    st.data_editor(display_df)
else:
    st.warning('请选择列名')