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

    # 自定义CSS样式
    st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        height: calc(100vh - 150px);
        overflow-y: auto;
        padding-bottom: 80px;
    }
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 10px;
        z-index: 1000;
        border-top: 1px solid #e0e0e0;
    }
    .message-container {
        margin-bottom: 10px;
        display: flex;
    }
    .user-message {
        background-color: #3B81F6; 
        color: white;
        max-width: 70%; 
        padding: 10px; 
        border-radius: 10px; 
        margin-left: auto;
        text-align: right;
    }
    .ai-message {
        background-color: #F1F0F0; 
        color: black;
        max-width: 70%; 
        padding: 10px; 
        border-radius: 10px; 
        margin-right: auto;
        text-align: left;
        border: 1px solid #E0E0E0;
    }
    </style>
    """, unsafe_allow_html=True)

    # 聊天区域
    st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)
    
    # 展示历史消息
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f'''
            <div class="message-container">
                <div class="user-message">{message['content']}</div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="message-container">
                <div class="ai-message">{message['content']}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # 固定底部的输入框
    st.markdown('<div class="fixed-input">', unsafe_allow_html=True)
    
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

    # 自动滚动到底部的JavaScript
    st.markdown("""
    <script>
    // 自动滚动到底部
    function scrollToBottom() {
        var chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // 页面加载后立即滚动
    window.onload = scrollToBottom;
    
    // 如果内容变化也滚动
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

