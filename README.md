# RAG

### 一.使用开源大语言模型 Qwen2.5 搭建 RAG & Agen

#### 1.安装依赖：

```
# torch 
pip install torch==2.6.0 
# 基础库 
pip install transformers==4.45.0 modelscope==1.18.1 
# FastAPI 
pip install fastapi==0.115.12 uvicorn==0.34.0 
# 前端 
pip install streamlit==1.39.0 gradio==5.0.2 
# LangChain 
pip install langchain langchain-openai langchain-community faiss-cpu sentence-transformers 
# vLLM（可选加速） 
pip install vllm==0.6.3.post1 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 2.Ollama 部署本地模型

​	1.准备 Qwen2.5 GGUF 模型
​	2.编写 Modelfile
​	3.创建并运行模型

```bash
ollama create qwen2.5_7b -f Modelfile
ollama run qwen2.5_7b
```



#### 3.vLLM 推理加速

​	使用 PagedAttention 提升推理速度，支持 OpenAI 兼容接口。

```bash
python -m vllm.entrypoints.openai.api_server --port 10222 --model 模型路径 --served-model-name Qwen2.5-7B-Instruct
```

#### 4. FastAPI 后端（端口 6066）

提供 /chat 流式对话接口，支持：
	系统提示词，历史对话管理，temperature /top_p/max_tokens 参数调节，流式返回

```bash
python fa.py
```

#### 5.Streamlit 前端（端口 8501）

```bash
streamlit run Sr.py
```

#### 6.Gradio 前端（端口 7860）

```bash
python Gra.py
```

### 二.LangChain

#### 1.LLMChain

​	将提示模板 + 大模型串联，实现标准化输入输出

#### 2.RAG 检索链

	加载文档 → 文本分块
	生成 Embedding 向量
	FAISS 向量库存储
	用户问题检索 → 生成回答
#### 3.自定义链（LCEL）

​	使用 prompt | model | parser 快速构建任务链。

### 三.词语接龙

#### 1.代码及分析

```python

import os

# 你的成语文件路径
FILE_PATH = r"F:\tutorial\damoxing\RAG\成语大全.txt"


# 加载成语库
def load_idioms():
    if not os.path.exists(FILE_PATH):
        print(f"未找到文件：{FILE_PATH}，请确保文件存在")
        return []

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        idioms = [line.strip() for line in f if line.strip()]
    return idioms


idiom_list = load_idioms()


# 根据最后一个字查找下一个成语
def find_next_idiom(last_char, idioms):
    for idiom in idioms:
        if idiom.startswith(last_char):
            return idiom
    return None


# ====================== 第8章：成语接龙链 ======================
def idiom_chain(user_idiom):
    # 1. 检查是否在库中
    if user_idiom not in idiom_list:
        return f"❌ 成语【{user_idiom}】不在成语库中，游戏终止！", True

    # 2. 取最后一个字接龙
    last_char = user_idiom[-1]
    next_idiom = find_next_idiom(last_char, idiom_list)

    if not next_idiom:
        return f"❌ 没有以【{last_char}】开头的成语，游戏终止！", True

    # 3. 接龙成功
    return f"✅ {user_idiom} → {next_idiom}", False


# ====================== 交互运行 ======================
if __name__ == "__main__":
    if not idiom_list:
        exit()

    print("=== 成语接龙游戏（输入 exit 退出）===")
    print(f"已加载成语：{len(idiom_list)} 个")

    while True:
        user = input("\n请输入成语：").strip()
        if user.lower() == "exit":
            print("=== 退出游戏 ===")
            break

        res, stop = idiom_chain(user)
        print(res)

        if stop:
            print("=== 游戏结束 ===")
            break
```

1.检查文件是否存在
2.按行读取成语，过滤空行
3.返回成语列表
4.Chain 的 数据加载阶段
5.根据上一个成语的最后一个字
6.检索以该字开头的成语
7.检索 / 匹配阶段。

#### 2.主链

```python
def idiom_chain(user_idiom):
    # 1. 校验输入
    if user_idiom not in idiom_list:
        return "错误信息", True

    # 2. 处理：取最后一字
    last_char = user_idiom[-1]

    # 3. 检索：查找下一个
    next_idiom = find_next_idiom(last_char, idiom_list)

    # 4. 终止判断
    if not next_idiom:
        return "无匹配成语，终止", True

    # 5. 输出结果
    return f"✅ {user_idiom} → {next_idiom}", False
```

 Chain 结构：
1.输入处理
2.逻辑判断
3.检索匹配
4.结果输出
5.终止条件

### 四.微调结果呈现

#### 1.前端结果

​	<img src="F:\tutorial\damoxing\RAG\运行结果\前端结果.jpg">

#### 2.后端结果

<img src="F:\tutorial\damoxing\RAG\运行结果\后端结果.jpg">

#### 3.词语接龙结果

<img src="F:\tutorial\damoxing\RAG\运行结果\chen.jpg">