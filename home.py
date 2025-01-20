import streamlit as st
from streamlit_modal import Modal
import bcrypt

# 自定义CSS样式
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        padding: 10px;
    }
    .stMarkdown {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 用户数据库（示例）
users_db = {
    "admin": {
        "password": b"$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password
        "name": "管理员"
    }
}

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

def show_login_modal():
    modal = Modal("登录", key="login_modal")
    with modal.container():
        with st.form("login_form"):
            st.markdown("### 🔐 用户登录")
            username = st.text_input("用户名", placeholder="请输入用户名")
            password = st.text_input("密码", type="password", placeholder="请输入密码")
            
            if st.form_submit_button("登录"):
                if username in users_db:
                    if verify_password(users_db[username]["password"], password):
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = username
                        st.success(f"欢迎回来，{users_db[username]['name']}！")
                        modal.close()
                    else:
                        st.error("密码错误")
                else:
                    st.error("用户名不存在")

# 在页面右上角添加登录按钮
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    if st.button("登录", key="login_button"):
        show_login_modal()
else:
    st.sidebar.markdown(f"欢迎，{users_db[st.session_state['username']]['name']}！")
    if st.sidebar.button("注销"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.experimental_rerun()
import pandas as pd
import json
from utils.db_utils import SQLiteDB

st.set_page_config(layout="wide")

# 读取data.json文件
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 转换为DataFrame
df = pd.DataFrame(data)

# 配置列
column_config = {
    "name": "名称",
    "url": st.column_config.LinkColumn("链接"),
    "desc": "描述"
}

# 展示数据
st.title("资源分类展示")

# 按tag分组展示
for tag, group in df.groupby('tag'):
    st.subheader(f"{tag}")
    st.dataframe(
        group,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
        column_order=["name", "url", "desc"],
        width=1800
    )


with SQLiteDB('st-demo.db') as db:
    users = db.fetch_all('SELECT * from user')
    # st.write(users)
    st.dataframe(users)
