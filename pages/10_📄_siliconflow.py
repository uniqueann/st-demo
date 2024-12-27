import streamlit as st
import openai
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()
openai.api_key = os.getenv('SILICONFLOW_API_KEY')


st.title("🎯 SiliconFlow AI Studio")

def display_chat():
    # 对话历史
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 对话展示样式
    def user_message(content):
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
            <div style="
                background-color: #DCF8C6; 
                max-width: 70%; 
                padding: 10px; 
                border-radius: 10px; 
                margin-left: 30%;
                text-align: right;
            ">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)

    def ai_message(content):
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
            <div style="
                background-color: #FFFFFF; 
                max-width: 70%; 
                padding: 10px; 
                border-radius: 10px; 
                margin-right: 30%;
                text-align: left;
                border: 1px solid #E0E0E0;
            ">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 展示历史消息
    for message in st.session_state.messages:
        if message['role'] == 'user':
            user_message(message['content'])
        else:
            ai_message(message['content'])

    # 输入框
    if prompt := st.chat_input("输入你的消息"):
        # 添加用户消息
        st.session_state.messages.append({
            'role': 'user', 
            'content': prompt
        })
        user_message(prompt)

        # 模拟AI回复（实际场景替换为真实的AI生成）
        ai_response = f"你说的是：{prompt}"
        st.session_state.messages.append({
            'role': 'ai', 
            'content': ai_response
        })
        ai_message(ai_response)

# 创建标签页
tab1,tab2,tab3,tab4 = st.tabs(['文本生成', '图像生成', '视频生成', '语音生成'])

with tab1:
    display_chat()
with tab2:
    st.header('图像生成')
with tab3:
    st.header('视频生成')
with tab4:
    st.header('语音生成')

