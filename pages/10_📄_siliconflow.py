import streamlit as st
import openai
from dotenv import load_dotenv
import os
import datetime
import requests
import json

# 加载环境变量
load_dotenv()
openai.api_key = os.getenv('SILICONFLOW_API_KEY')

base_url = "https://api.siliconflow.cn/v1"

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

    /* 输入框容器 */
    .input-wrapper {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        display: flex;
        justify-content: center;
        padding: 10px;
        background-color: white;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }

    /* 输入框样式 */
    .input-wrapper .stChatInput {
        max-width: 800px; /* 限制最大宽度 */
        width: 100%;
    }

    .input-wrapper .stChatInput > div > div > input {
        border: 1px solid #e0e0e0;
        border-radius: 20px;
        padding: 10px 15px;
        background-color: #f5f5f5;
        width: 100%;
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

    # 输入框容器
    st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
    
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

    st.markdown('</div>', unsafe_allow_html=True)

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

def display_img():
    # 显示使用提示
    with st.expander("💡 使用提示"):
        st.markdown("""
        #### 根据文本提示创建图像
        在使用文生图的大模型时，为了生成更高质量的图像，输入的prompt（提示词）需要精心设计。
        以下是一些有助于提高生成图像质量的提示词输入技巧：

        * **具体描述**: 尽量详细地描述你想要生成的图像内容。比如，如果你想生成一幅日落的海滩风景，不要仅仅输入"海滩日落"，而是可以尝试输入"一个宁静的海滩上，夕阳西下，天空呈现出橙红色，海浪轻轻拍打着沙滩，远处有一艘小船"。
        * **情感和氛围**: 除了描述图像的内容，还可以加入对情感或氛围的描述，比如"温馨的"、"神秘的"、"充满活力的"等，这样可以帮助模型更好地理解你想要的风格。
        * **风格指定**: 如果你有特定的艺术风格偏好，比如"印象派"、"超现实主义"等，可以在prompt中明确指出，这样生成的图像更有可能符合你的期待。
        * **避免模糊不清的词汇**: 尽量避免使用过于抽象或模糊不清的词汇，比如"美"、"好"等，这些词汇对于模型来说难以具体化，可能会导致生成的图像与预期相差较大。
        * **使用否定词**: 如果你不希望图像中出现某些元素，可以使用否定词来排除。例如，"生成一幅海滩日落的图片，但不要有船"。
        * **分步骤输入**: 对于复杂场景，可以尝试分步骤聚输入提示词，先生成基础图像，再根据需要调整或添加细节。
        * **尝试不同的描述方式**: 有时候，即使描述的是同一个场景，不同的描述方式也会得到不同的结果。可以尝试从不同的角度或使用不同的词汇来描述，看看哪种方式能得到更满意的结果。
        * **利用模型的特定功能**: 一些模型可能提供了特定的功能或参数调整选项，比如调整生成图像的分辨率、风格强度等，合理利用这些功能也可以帮助提高生成图像的质量。
        """)
    new_message = st.text_area("请输入生成图像的提示词：")
    if st.button("生成图片"):
        if new_message:
            with st.spinner('正在生成图像...'):
                try:
                    # 调用SiliconFlow的图像生成API
                    url = base_url + "/images/generations"
                    headers = {
                        "Authorization": "Bearer " + openai.api_key,
                        "Content-Type": "application/json"
                    }
                    data = {
                        "prompt": new_message,
                        "n": 1,  # 生成1张图片
                        "size": "1024x1024"  # 图片尺寸
                    }
                    response = requests.post(url, headers=headers, json=data)
                    response.raise_for_status()
                    
                    # 获取生成的图片URL并显示
                    image_url = response.json()["data"][0]["url"]
                    st.image(image_url, caption="生成的图像", use_column_width=True)
                    st.success("图像生成成功！")
                except requests.exceptions.RequestException as e:
                    st.error(f"图像生成失败: {str(e)}")
        else:
            st.warning("请输入生成图像的提示词")


# 创建标签页
tab1,tab2,tab3,tab4,tabModels = st.tabs(['文本生成', '图像生成', '视频生成', '语音生成', '所有模型'])

with tab1:
    display_chat()
with tab2:
    display_img()
with tab3:
    st.header('视频生成')
with tab4:
    st.header('语音生成')
with tabModels:
    st.header('所有模型')
    url = base_url + "/models"
    headers = {"Authorization": "Bearer "+openai.api_key}
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text).get("data",[])
    models = [x["id"] for x in data]
    st.write(models)
