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
        gap: 20px;  /* 增加消息间距 */
        padding-bottom: 100px; /* 为输入框留空间 */
    }
    .message {
        max-width: 75%;
        padding: 12px 15px;
        border-radius: 15px;
        line-height: 1.5;
        position: relative;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
    .message-wrapper {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    .message-time {
        font-size: 0.7em;
        color: #888;
        margin-top: 5px;
        text-align: right;
    }
    .user-message-time {
        align-self: flex-end;
        margin-right: 5px;
    }
    .ai-message-time {
        align-self: flex-start;
        margin-left: 5px;
    }
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 15px;
        background-color: white;
        z-index: 1000;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }
    /* 隐藏Streamlit默认的输入框边框 */
    .stTextInput > div > div > input {
        border: none;
        background-color: #f5f5f5;
        border-radius: 20px;
        padding: 10px 15px;
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
        time_class = 'user-message-time' if message['role'] == 'user' else 'ai-message-time'
        
        st.markdown(f'''
        <div class="message-wrapper">
            <div class="message {message_class}">
                {message['content']}
            </div>
            <div class="message-time {time_class}">
                {message.get('time', '刚刚')}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 固定底部的输入框容器
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # 输入框
    if prompt := st.chat_input("输入你的消息", key="chat_input"):
        import datetime
        
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

