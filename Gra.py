import gradio as gr
import requests

backend_url = "http://127.0.0.1:6066/chat"

def chat_with_backend(prompt, history, sys_prompt, history_len, temperature, top_p, max_tokens, stream):
    history_clean = [{"role": h["role"], "content": h["content"]} for h in history]
    data = {
        "query": prompt,
        "sys_prompt": sys_prompt,
        "history": history_clean,
        "history_len": history_len,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }
    response = requests.post(backend_url, json=data, stream=True)
    chunks = ""
    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        chunks += chunk
        if stream:
            yield chunks
    if not stream:
        yield chunks

def clear_history(history):
    return ""

with gr.Blocks(fill_width=True, fill_height=True) as demo:
    with gr.Tab("🤖 聊天机器人"):
        gr.Markdown("## 🤖 聊天机器人")
        with gr.Row():
            with gr.Column(scale=1, variant="panel"):
                sys_prompt = gr.Textbox(label="系统提示词", value="You are a helpful assistant")
                history_len = gr.Slider(1, 10, 1, label="保留历史轮数")
                temperature = gr.Slider(0.01, 2.0, 0.5, step=0.01, label="temperature")
                top_p = gr.Slider(0.01, 1.0, 0.5, step=0.01, label="top_p")
                max_tokens = gr.Slider(512, 4096, 1024, step=8, label="max_tokens")
                stream = gr.Checkbox(label="stream", value=True)
            with gr.Column(scale=10):
                chatbot = gr.Chatbot(type="messages", height=500)
                gr.ChatInterface(
                    fn=chat_with_backend,
                    type="messages",
                    chatbot=chatbot,
                    additional_inputs=[sys_prompt, history_len, temperature, top_p, max_tokens, stream]
                )

demo.launch()