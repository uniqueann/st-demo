import streamlit as st
import openai
from dotenv import load_dotenv
import os
from datetime import datetime

# 加载环境变量
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# 页面配置
st.set_page_config(
    page_title="AI 助手对话",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stSelectbox > div > div > select {
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #1e88e5;
        color: #ffffff;
    }
    .assistant-message {
        background-color: #f5f5f5;
        color: #000000
    }
    .message-header {
        font-size: 0.8rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'messages' not in st.session_state:
    st.session_state.messages = []

def get_available_models():
    try:
        models = openai.Model.list()
        # 过滤出 GPT 相关模型
        gpt_models = [model.id for model in models.data if "gpt" in model.id.lower()]
        return sorted(gpt_models)
    except Exception as e:
        st.error(f"获取模型列表失败: {str(e)}")
        return ["gpt-3.5-turbo", "gpt-4"]  # 返回默认模型列表

# 侧边栏配置
with st.sidebar:
    st.title("⚙️ 设置")
    
    # 模型选择
    selected_model = st.selectbox(
        "选择模型",
        get_available_models(),
        index=0
    )
    
    # 温度滑块
    temperature = st.slider(
        "温度 (创造性)", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.7, 
        step=0.1,
        help="较高的值会使输出更随机，较低的值会使输出更确定"
    )
    
    # 最大令牌数
    max_tokens = st.number_input(
        "最大令牌数", 
        min_value=50, 
        max_value=4000, 
        value=2000,
        help="回复的最大长度"
    )
    
    # 清空对话按钮
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.experimental_rerun()

# 主页面
st.title("🤖 AI 助手对话")
st.markdown("---")

# 显示对话历史
for idx, message in enumerate(st.session_state.messages):
    role = message["role"]
    content = message["content"]
    time = message.get("time", "")
    
    # 为不同角色设置不同的样式
    css_class = "user-message" if role == "user" else "assistant-message"
    
    with st.container():
        st.markdown(f"""
        <div class="chat-message {css_class}">
            <div class="message-header">
                {'👤 用户' if role == 'user' else '🤖 助手'} | {time}
            </div>
            {content}
        </div>
        """, unsafe_allow_html=True)

# 用户输入
user_input = st.text_area("输入你的问题", height=100, key="user_input")

# 发送按钮
if st.button("发送 📤"):
    if user_input:
        # 添加用户消息
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "time": current_time
        })
        
        try:
            # 调用 OpenAI API
            response = openai.ChatCompletion.create(
                model=selected_model,
                messages=[{"role": m["role"], "content": m["content"]} 
                         for m in st.session_state.messages],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # 添加助手回复
            assistant_response = response.choices[0].message.content
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_response,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # 清空输入框
            st.experimental_rerun()
            
        except Exception as e:
            st.error(f"发生错误: {str(e)}")
    else:
        st.warning("请输入内容后再发送")

# 显示使用提示
with st.expander("💡 使用提示"):
    st.markdown("""
    - 在侧边栏选择合适的模型和参数
    - 在文本框中输入你的问题
    - 点击发送按钮获取 AI 回复
    - 使用清空对话按钮开始新的对话
    - 温度参数越高，回答越具有创造性
    - 令牌数限制影响回答的最大长度
    """)
