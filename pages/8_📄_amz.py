import streamlit as st
import time 
from bs4 import BeautifulSoup
import requests

def get_page_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string
        return title
    except requests.exceptions.HTTPError:
        return "HTTP Error"
    except requests.exceptions.RequestException:
        return "Connection Error"

st.title("Amazon 产品信息爬取")

expander = st.expander('爬取某一品类链接下产品信息 了解更多')
with expander:
    st.write('输入合规url后点击爬取，系统会自动爬取当前品类url下面第一页产品信息以表格的形式展示。')

url = st.text_input("请输入URL")

if st.button('开始爬取'):
    if url:
        spider_state = st.text('开始爬取产品信息...')
        st.write(get_page_info(url))
        spider_state.text('结束爬取产品信息 结果如下：')

    else:
        spider_state = st.text('url不能为空')