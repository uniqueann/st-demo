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
                background-color: #3B81F6; 
                color: white;
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
                background-color: #F1F0F0; 
                color: black;
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

    # 创建一个占位容器，用于固定输入框位置
    placeholder = st.empty()

    # 聊天区域（滚动）
    chat_container = st.container()
    
    with chat_container:
        # 展示历史消息
        for message in st.session_state.messages:
            if message['role'] == 'user':
                user_message(message['content'])
            else:
                ai_message(message['content'])

    # 固定在底部的输入框
    with placeholder.container():
        st.markdown("""
        <div style="
            position: fixed; 
            bottom: 0; 
            left: 0; 
            right: 0; 
            background-color: white; 
            padding: 10px; 
            z-index: 1000;
            border-top: 1px solid #e0e0e0;
        ">
        """, unsafe_allow_html=True)
        
        # 输入框
        if prompt := st.chat_input("输入你的消息", key="chat_input"):
            # 添加用户消息
            st.session_state.messages.append({
                'role': 'user', 
                'content': prompt
            })
            
            # 模拟AI回复（实际场景替换为真实的AI生成）
            ai_response = f"你说的是：{prompt}"
            st.session_state.messages.append({
                'role': 'ai', 
                'content': ai_response
            })
            
            # 重新运行以刷新聊天记录
            st.experimental_rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# 创建标签页
tab1,tab2,tab3,tab4 = st.tabs(['文本生成', '图像生成', '视频生成', '语音生成'])

with tab1:
    # 调整页面布局，为底部输入框腾出空间
    st.markdown("""
    <style>
    .block-container {
        padding-bottom: 100px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    display_chat()
with tab2:
    st.header('图像生成')
with tab3:
    st.header('视频生成')
with tab4:
    st.header('语音生成')

