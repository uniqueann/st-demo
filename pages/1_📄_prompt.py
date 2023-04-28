import streamlit as st
import pandas as pd
import numpy as np


# Add several radios to the sidebar, including Programming, Interview, Thesis, and Translation, 
# and click to display different secondary titles
radio_selection = st.sidebar.radio("Select a radio", ["人工智能","编程", "面试", "论文", "翻译"])


st.title('Prompt')

st.subheader('让生产力加倍的Prompt')
if radio_selection == "人工智能":
    st.text_area('Python专家','你现在是以为Python专家，专攻AI方向，我现在有这方面的问题咨询你。问题如下：')
    st.text_area('.NET专家','你现在是以为Python专家，专攻AI方向，我现在有这方面的问题咨询你。问题如下：')
    st.text_area('VUE.js专家','你现在是以为Python专家，专攻AI方向，我现在有这方面的问题咨询你。问题如下：')
elif radio_selection == "编程":
    st.text_area('Python专家','你现在是以为Python专家，专攻AI方向，我现在有这方面的问题咨询你。问题如下：')
    st.text_area('.NET专家','你现在是以为Python专家，专攻AI方向，我现在有这方面的问题咨询你。问题如下：')
    st.text_area('VUE.js专家','你现在是以为Python专家，专攻AI方向，我现在有这方面的问题咨询你。问题如下：')
elif radio_selection == "面试":
    st.write("Secondary title for Interview")
elif radio_selection == "论文":
    st.write("Secondary title for Thesis")
elif radio_selection == "翻译":
    st.write("Secondary title for Translation")
