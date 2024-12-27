import streamlit as st
import openai
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()
openai.api_key = os.getenv('SILICONFLOW_API_KEY')

def main():
    st.title("🎯 SiliconFlow AI Studio")
    
    # 创建标签页
    tabs = st.tabs(['文本生成', '图像生成', '视频生成', '语音生成'])
    st.write(tabs[0])
    
    with tabs[0]:
        st.header(tabs[0])
    with tabs[1]:
        st.header(tabs[1])
    with tabs[2]:
        st.header(tabs[2])
    with tabs[3]:
        st.header(tabs[3])

if __name__ == "__main__":
    main()
