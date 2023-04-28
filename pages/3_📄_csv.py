import streamlit as st
import pandas as pd
import chardet
from st_aggrid import GridOptionsBuilder,AgGrid


uploaded_file = st.sidebar.file_uploader('请上传 CSV 文件',type=['csv'])

if uploaded_file is None:
    st.stop()

encoding_text = st.text('Detecting file coding...')

rawdata = uploaded_file.read()
encoding = chardet.detect(rawdata)['encoding']
uploaded_file.seek(0)

encoding_text.text(f'The file coding is {encoding}')

@st.cache_data
def load_data(file,encoding): 
    return pd.read_csv(file,encoding=encoding)

df = load_data(uploaded_file,encoding)
# df.columns = [col.encode('latin1').decode('gb2312') for col in df.columns]
# st.write(df)
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
gridOptions = gb.build()
# df.columns = [col.encode('latin1').decode(coding) for col in df.columns]
AgGrid(
    pd.DataFrame(df, columns=df.columns),
    gridOptions=gridOptions,
    fit_columns_on_grid_load=True,
    height=900,
    editable=True,
    enable_enterprise_modules=True
)