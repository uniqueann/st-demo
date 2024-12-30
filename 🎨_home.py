import streamlit as st
import openai
import os
from dotenv import load_dotenv
from utils.preprocess_utils import *
import pandas as pd


st.subheader('当前Streamlit版本：'+st.__version__)  # 查看当前版本

load_dotenv('.env')
# 设置OpenAI API密钥
openai.api_key = os.getenv('OPENAI_API_KEY')

data = openai.Model.list().data
models =[ x["id"]  for x in data]
#  if x.owned_by=="openai"

st.write(models)
# base_engines = ['ada','babbage','curie','davinci']
# options = [item['id'] for item in models.data for eng in base_engines if item['id'].startswith(eng)]

retrieve_model_input = st.text_input('请输入要检索模型id')
if st.button('确定检索模型'):
    if retrieve_model_input:
        st.write(openai.Model.retrieve(retrieve_model_input))
    else:
        st.toast('请输入检索模型id')

radio_selection = st.sidebar.radio("Select a radio", ["完成","聊天", "编辑", "图像", "嵌入", "音频"])

    

# 定义函数，使用OpenAI API获取回答
def get_answer(prompt,temp,max_tokens):
    response = openai.Completion.create(
        engine = 'text-davinci-003', 
        prompt=prompt, 
        temperature=temp,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer = response.choices[0].text
    return answer

def get_chat(prompt,temp,max_tokens):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt }
        ],
        temperature=temp,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer = response.choices[0].message.content
    return answer

def get_image(prompt,n,size):
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size=size
    )
    return response.data

subheader = st.subheader('text-davinci-003')
new_message = st.text_area("请输入聊天内容：")


def chat():
    subheader.subheader('gpt-3.5-turbo')
    temperature = st.slider('请选择参数 temperature',0.1,2.0,0.1,0.1,help='值越小，随机性越小')
    max_tokens = st.slider('请选择参数 max_tokens',100,2048,1024,100,help='值越大，能够返回的内容越多，配额消耗也越大')
    if st.button('发送'):
        if new_message:
            answer = get_chat(new_message,temperature,max_tokens)
            st.write(answer)

def ans():
    subheader.subheader('text-davinci-003')
    temperature = st.slider('请选择参数 temperature',0.1,2.0,0.1,0.1,help='值越小，随机性越小')
    max_tokens = st.slider('请选择参数 max_tokens',100,2048,1024,100,help='值越大，能够返回的内容越多，配额消耗也越大')
    if st.button('完成'):
        if new_message:
            answer = get_answer(new_message,temperature,max_tokens)
            st.write(answer)

def img():
    subheader.subheader('create image')
    n = st.slider('请选择生成图片数量',1,5,3,1,help='图片数量')
    size = st.select_slider('请选择生成图片尺寸', ['256x256', '512x512', '1024x1024'], '512x512')
    if st.button('create image'):
        if new_message:
            with st.spinner('Please wait...'):
                prompt = preprocess(new_message)
                imgs = get_image(prompt,n,size)

                col1,col2,col3 = st.columns(3)
                for i,img in enumerate(imgs):
                    if i % 3 == 0:
                        img_col = col1
                    elif i % 3 == 1:
                        img_col = col2
                    else:
                        img_col = col3

                    img_col.image(img.url, use_column_width=True)

if radio_selection == "完成":
    ans()
elif radio_selection == "聊天":
    chat()
elif radio_selection == "编辑":
    st.write('edit')
elif radio_selection == "图像":
    img()
elif radio_selection == "音频":
    st.write('audio')
