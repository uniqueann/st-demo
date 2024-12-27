import streamlit as st
import openai
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()
openai.api_key = os.getenv('SILICONFLOW_API_KEY')


st.title("🎯 SiliconFlow AI Studio")

def display_chat():
    # 自定义CSS
    st.markdown("""
    <style>
    .stApp {
        display: flex;
        flex-direction: column;
        height: 100vh;
    }
    .main-container {
        flex-grow: 1;
        overflow-y: auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding-bottom: 100px; /* 为输入框留空间 */
    }
    .message {
        max-width: 70%;
        padding: 10px;
        border-radius: 10px;
    }
    .user-message {
        background-color: #3B81F6; 
        color: white;
        align-self: flex-end;
        margin-left: auto;
    }
    .ai-message {
        background-color: #F1F0F0; 
        color: black;
        align-self: flex-start;
        margin-right: auto;
    }
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 10px;
        background-color: white;
        z-index: 1000;
        border-top: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

    # 对话历史
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 主容器
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 聊天内容容器
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # 展示历史消息
    for message in st.session_state.messages:
        message_class = 'user-message' if message['role'] == 'user' else 'ai-message'
        st.markdown(f'''
        <div class="message {message_class}">
            {message['content']}
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 固定底部的输入框容器
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
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
        
        # 重新运行
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # 自动滚动脚本
    st.markdown("""
    <script>
    // 自动滚动到底部的函数
    function scrollToBottom() {
        var mainContainer = document.querySelector('.main-container');
        if (mainContainer) {
            mainContainer.scrollTop = mainContainer.scrollHeight;
        }
    }
    
    // 页面加载后和内容变化时滚动
    window.onload = scrollToBottom;
    setTimeout(scrollToBottom, 100);
    </script>
    """, unsafe_allow_html=True)

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

