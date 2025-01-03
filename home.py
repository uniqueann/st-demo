import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide")

# 读取data.json文件
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 转换为DataFrame
df = pd.DataFrame(data)

# 配置列
column_config = {
    "name": "名称",
    "url": st.column_config.LinkColumn("链接"),
    "desc": "描述"
}

# 展示数据
st.title("资源分类展示")

# 按tag分组展示
for tag, group in df.groupby('tag'):
    st.subheader(f"{tag}")
    st.dataframe(
        group,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
        column_order=["name", "url", "desc"],
        width=1800
    )
