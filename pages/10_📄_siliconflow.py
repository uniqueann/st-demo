import streamlit as st
import openai
from dotenv import load_dotenv
import os
import datetime

# 加载环境变量
load_dotenv()
openai.api_key = os.getenv('SILICONFLOW_API_KEY')


st.title("🎯 SiliconFlow AI Studio")


def display_chat():
    # 自定义CSS
    st.markdown("""
    <style>
    /* 全局布局 */
    .stApp {
        display: flex;
        flex-direction: column;
        height: 100vh;
        max-height: 100vh;
        overflow: hidden;
    }

    /* 主容器，允许滚动 */
    .main-container {
        flex-grow: 1;
        overflow-y: auto;
        padding: 20px;
        padding-bottom: 100px; /* 为输入框留空间 */
        display: flex;
        flex-direction: column;
        max-height: calc(100vh - 100px); /* 减去输入框高度 */
    }

    /* 聊天容器 */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        width: 100%;
    }

    /* 消息样式 */
    .message {
        max-width: 75%;
        padding: 12px 15px;
        border-radius: 15px;
        line-height: 1.5;
        position: relative;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .user-message {
        background-color: #007bff; 
        color: white;
        align-self: flex-end;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }

    .ai-message {
        background-color: #f1f0f0; 
        color: #333;
        align-self: flex-start;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }

    /* 输入框固定在底部 */
    .stChatInput {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        padding: 10px;
        background-color: white;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }

    /* 输入框样式 */
    .stChatInput > div > div > input {
        border: 1px solid #e0e0e0;
        border-radius: 20px;
        padding: 10px 15px;
        background-color: #f5f5f5;
    }

    /* 消息包装器 */
    .message-wrapper {
        display: flex;
        flex-direction: column;
        width: 100%;
        align-items: flex-end;
    }

    .user-message-wrapper {
        align-items: flex-end;
    }

    .ai-message-wrapper {
        align-items: flex-start;
    }

    .message-time {
        font-size: 0.7em;
        color: #888;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 初始化消息列表
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 主容器
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 聊天容器
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # 展示历史消息
    for message in st.session_state.messages:
        wrapper_class = 'user-message-wrapper' if message['role'] == 'user' else 'ai-message-wrapper'
        message_class = 'user-message' if message['role'] == 'user' else 'ai-message'
        
        st.markdown(f'''
        <div class="message-wrapper {wrapper_class}">
            <div class="message {message_class}">
                {message['content']}
            </div>
            <div class="message-time">
                {message.get('time', '刚刚')}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 输入框
    if prompt := st.chat_input("输入你的消息", key="chat_input"):
        # 添加用户消息
        st.session_state.messages.append({
            'role': 'user', 
            'content': prompt,
            'time': datetime.datetime.now().strftime("%H:%M")
        })
        
        # 模拟AI回复（实际场景替换为真实的AI生成）
        ai_response = f"你说的是：{prompt}"
        st.session_state.messages.append({
            'role': 'ai', 
            'content': ai_response,
            'time': datetime.datetime.now().strftime("%H:%M")
        })
        
        # 重新运行
        st.rerun()

    # 自动滚动脚本
    st.markdown("""
    <script>
    function scrollToBottom() {
        var mainContainer = document.querySelector('.main-container');
        if (mainContainer) {
            mainContainer.scrollTop = mainContainer.scrollHeight;
        }
    }
    
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

