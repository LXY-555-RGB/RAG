from openai import OpenAI

# 本地 Ollama 服务
api_key = "ollama"
base_url = "http://localhost:11434/v1"

client = OpenAI(api_key=api_key, base_url=base_url)

response = client.chat.completions.create(
    model="qwen2.5:0.5b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好"}
    ],
    max_tokens=150,
    temperature=0.7,
    stream=True
)

# 逐块打印
for chunk in response:
    chunk_msg = chunk.choices[0].delta.content
    if chunk_msg:
        print(chunk_msg, end="")