import streamlit as st
import openai
import os
from dotenv import load_dotenv

# load_dotenv('.env')
# 设置OpenAI API密钥
openai.api_key = os.getenv('OPENAI_API_KEY')


# 定义函数，使用OpenAI API获取回答
def get_answer(prompt,temp,max_tokens):
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

# 使用Streamlit库创建对话界面
st.title("GPT-3.5-Turbo")

expander = st.expander('关于GPT-3.5-Turbo 了解更多')
with expander:
    st.write('GPT-3.5模型可以理解和生成自然语言或代码。在GPT-3.5家族中，我们最强大且成本效益最高的模型是gpt-3.5-turbo，它已经针对聊天进行了优化，但在传统的完成任务中也表现良好。')

temperature = st.slider('请选择参数 temperature',0.1,2.0,0.1,0.1,help='值越小，随机性越小')

max_tokens = st.slider('请选择参数 max_tokens',100,2048,1024,100,help='值越大，能够返回的内容越多，配额消耗也越大')

new_message = st.text_area("请输入聊天内容：")

if st.button('发送'):
    if new_message:
        answer = get_answer(new_message,temperature,max_tokens)
        st.write(answer)

