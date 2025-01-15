import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder,AgGrid


uploaded_file = st.file_uploader('请上传 XLSX 文件',type=['xlsx'])

if uploaded_file is None:
    st.stop()

@st.cache_data
def load_data(file):
    return pd.read_excel(uploaded_file,None)

dfs = load_data(uploaded_file)

names = list(dfs.keys())
with st.container():
    sheet_selects = st.multiselect('工作表',names)

    if len(sheet_selects)==0:
        st.stop()

tabs = st.tabs(sheet_selects)

with tabs[0]:
    st.dataframe(dfs[0])

# for tab,name in zip(tabs,sheet_selects):
#     with tab:
#         df = dfs[name]
#         gb = GridOptionsBuilder.from_dataframe(df)
#         gb.configure_side_bar()
#         gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
#         gridOptions = gb.build()
#         # st.dataframe(df)
#         AgGrid(
#             pd.DataFrame(df, columns=df.columns),
#             gridOptions=gridOptions,
#             fit_columns_on_grid_load=True,
#             height=800,
#             editable=True,
#             enable_enterprise_modules=True
#         )
