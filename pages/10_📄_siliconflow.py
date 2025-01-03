import streamlit as st
import openai
from dotenv import load_dotenv
import os
import datetime
import requests
import json

# 加载环境变量
load_dotenv()
api_key = os.getenv('SILICONFLOW_API_KEY')

base_url = "https://api.siliconflow.cn/v1"

st.title("🎯 SiliconFlow AI Studio")


def display_chat():
    # 初始化消息列表
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 简单输入框
    prompt = st.text_input("输入提示词")
    
    if st.button("生成"):
        if prompt:
            # 添加用户消息
            st.session_state.messages.append({
                'role': 'user', 
                'content': prompt,
                'time': datetime.datetime.now().strftime("%H:%M")
            })
            
            # 模拟AI回复
            ai_response = f"模型回复：{prompt}"
            st.session_state.messages.append({
                'role': 'ai', 
                'content': ai_response,
                'time': datetime.datetime.now().strftime("%H:%M")
            })
            
            # 重新运行
            st.rerun()

    # 展示生成内容
    st.write("生成内容：")
    for message in st.session_state.messages:
        if message['role'] == 'ai':
            st.text_area("", value=message['content'], height=100, disabled=True)

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
                        "Authorization": "Bearer " + api_key,
                        "Content-Type": "application/json"
                    }
                    data = {
                        "prompt": new_message,
                        "model":"Pro/black-forest-labs/FLUX.1-schnell",
                        "n": 1,  # 生成1张图片
                        "image_size": "1024x1024"  # 图片尺寸
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
    
    # 语音生成参数设置
    col1, col2 = st.columns(2)
    with col1:
        voice = st.selectbox("选择语音", ["male", "female", "child"])
        response_format = st.selectbox("选择输出格式", ["mp3", "wav", "ogg"])
        sample_rate = st.selectbox("选择采样率", ["22050", "44100", "48000"])
    with col2:
        stream = st.selectbox("选择流式传输", ["true", "false"])
        speed = st.number_input("语速 (0.5-2.0)", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        gain = st.number_input("音量增益 (0.1-10.0)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    
    text_input = st.text_area("输入要转换为语音的文本")
    
    if st.button("生成语音"):
        if text_input:
            with st.spinner('正在生成语音...'):
                try:
                    url = base_url + "/audio/speech"
                    headers = {
                        "Authorization": "Bearer " + api_key,
                        "Content-Type": "application/json"
                    }
                    data = {
                        "model": "fishaudio/fish-speech-1.5",
                        "input": text_input,
                        "voice": voice,
                        "response_format": response_format,
                        "sample_rate": int(sample_rate),
                        "stream": stream.lower() == "true",
                        "speed": speed,
                        "gain": gain
                    }
                    response = requests.post(url, headers=headers, json=data)
                    response.raise_for_status()
                    
                    # 处理响应
                    if response_format == "mp3":
                        st.audio(response.content, format="audio/mp3")
                    elif response_format == "wav":
                        st.audio(response.content, format="audio/wav")
                    elif response_format == "ogg":
                        st.audio(response.content, format="audio/ogg")
                    
                    st.success("语音生成成功！")
                except requests.exceptions.RequestException as e:
                    st.error(f"语音生成失败: {str(e)}")
        else:
            st.warning("请输入要转换为语音的文本")
with tabModels:
    st.header('所有模型')
    url = base_url + "/models"
    headers = {"Authorization": "Bearer "+api_key}
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text).get("data",[])
    models = [x["id"] for x in data]
    st.write(models)
