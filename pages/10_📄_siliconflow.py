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
    tab1,tab2,tab3,tab4 = st.tabs(['文本生成', '图像生成', '视频生成', '语音生成'])
    st.write(tab1)
    
    with tab1:
        st.header(tab1)
    with tab2:
        st.header(tab2)

if __name__ == "__main__":
    main()
