import streamlit as st
import siliconflow as sf
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()
sf.api_key = os.getenv('SILICONFLOW_API_KEY')

# 获取所有可用模型
def get_available_models():
    try:
        # 获取所有模型列表
        models = sf.Model.list()
        
        # 按类型分类模型
        categorized_models = {
            "LLM": [],
            "VLM": [],
            "Image": [],
            "Video": [],
            "Audio": []
        }
        
        for model in models:
            # 根据模型的capabilities或其他属性来分类
            # 这里需要根据实际的API返回结构来调整
            if model.capabilities.get("text"):
                if model.capabilities.get("vision"):
                    categorized_models["VLM"].append(model)
                else:
                    categorized_models["LLM"].append(model)
            if model.capabilities.get("image"):
                categorized_models["Image"].append(model)
            if model.capabilities.get("video"):
                categorized_models["Video"].append(model)
            if model.capabilities.get("audio"):
                categorized_models["Audio"].append(model)
        
        return categorized_models
    except Exception as e:
        st.error(f"获取模型列表失败：{str(e)}")
        return None

def create_text_generation_tab(models):
    st.header("文本生成")
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # 选择模型类型
            model_type = st.radio("选择模型类型", ["LLM", "VLM"])
            
            # 获取选定类型的可用模型
            available_models = models.get(model_type, [])
            if not available_models:
                st.warning(f"当前没有可用的{model_type}模型")
                return
            
            # 选择具体模型
            selected_model = st.selectbox(
                "选择模型",
                options=available_models,
                format_func=lambda x: x.name
            )
            
            # 显示模型信息
            with st.expander("模型信息", expanded=False):
                st.json(selected_model.to_dict())
            
            # 模型参数设置
            with st.expander("模型参数设置", expanded=True):
                temperature = st.slider(
                    "Temperature",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.7,
                    step=0.1
                )
                max_tokens = st.number_input(
                    "最大令牌数",
                    min_value=1,
                    max_value=selected_model.max_tokens if hasattr(selected_model, 'max_tokens') else 4096,
                    value=1000
                )
            
            # VLM模型特有的图片上传功能
            if model_type == "VLM":
                uploaded_file = st.file_uploader("上传图片", type=['png', 'jpg', 'jpeg'])
                if uploaded_file is not None:
                    st.image(uploaded_file, caption="上传的图片")
            
            prompt = st.text_area("输入提示词", height=200)
            
            if st.button("生成", use_container_width=True):
                with st.spinner("生成中..."):
                    try:
                        # 构建请求参数
                        params = {
                            "temperature": temperature,
                            "max_tokens": max_tokens,
                            "prompt": prompt
                        }
                        
                        # 如果是VLM且有上传图片，添加图片参数
                        if model_type == "VLM" and uploaded_file:
                            params["image"] = uploaded_file
                        
                        # 调用API生成内容
                        response = selected_model.generate(**params)
                        
                        st.success("生成完成！")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"生成失败：{str(e)}")
        
        with col2:
            st.subheader("生成历史")
            st.info("这里显示历史生成记录")

def main():
    st.title("🎯 SiliconFlow AI Studio")
    
    # 获取可用模型
    models = get_available_models()
    if not models:
        st.error("无法获取模型列表，请检查API密钥是否正确")
        return
    
    # 创建标签页
    tabs = st.tabs(['文本生成', '图像生成', '视频生成', '语音生成'])
    
    with tabs[0]:
        create_text_generation_tab(models)
    with tabs[1]:
        create_image_generation_tab(models)
    with tabs[2]:
        create_video_generation_tab(models)
    with tabs[3]:
        create_audio_generation_tab(models)

if __name__ == "__main__":
    main()
