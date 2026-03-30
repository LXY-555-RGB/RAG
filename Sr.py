import streamlit as st
import requests

backend_url = "http://127.0.0.1:6066/chat"

st.set_page_config(page_title="ChatBot", page_icon="🤖", layout="centered")
st.title("🤖 聊天机器人")

# 清空历史
def clear_chat_history():
    st.session_state.history = []

# 侧边栏配置
with st.sidebar:
    st.title("设置")
    sys_prompt = st.text_input("系统提示词:", value="You are a helpful assistant.")
    history_len = st.slider("保留历史轮数:", 1, 10, 1)
    temperature = st.slider("temperature:", 0.01, 2.0, 0.5, 0.01)
    top_p = st.slider("top_p:", 0.01, 1.0, 0.5, 0.01)
    max_tokens = st.slider("max_tokens:", 256, 4096, 1024, 8)
    stream = st.checkbox("stream", value=True)
    st.button("清空聊天历史", on_click=clear_chat_history)

# 初始化历史
if "history" not in st.session_state:
    st.session_state.history = []

# 显示历史
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入
if prompt := st.chat_input("来和我聊天~~~"):
    with st.chat_message("user"):
        st.markdown(prompt)

    data = {
        "query": prompt,
        "sys_prompt": sys_prompt,
        "history_len": history_len,
        "history": st.session_state.history,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }

    response = requests.post(backend_url, json=data, stream=True)
    if response.status_code == 200:
        chunks = ""
        assistant_placeholder = st.chat_message("assistant")
        assistant_text = assistant_placeholder.markdown("")

        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            chunks += chunk
            assistant_text.markdown(chunks)

        st.session_state.history.append({"role": "user", "content": prompt})
        st.session_state.history.append({"role": "assistant", "content": chunks})