import requests

# -------------------------------
# 🧠 本地模型调用（备用接口）
# -------------------------------
def local_model(prompt, model_name="deepseek-r1", temperature=0.7, ollama_url="http://localhost:11434"):
    """
    参数：
    - prompt: 用户输入的提示词
    - model_name: 模型名称（如 deepseek-r1, llama3 等）
    - temperature: 创意强度（0.0 ~ 1.0）
    - ollama_url: Ollama 服务地址

    返回：
    - 模型回复文本 或 错误信息
    """
    if not prompt:
        return "⚠️ 没有输入提示词"

    try:
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "⚠️ 模型未返回任何内容")
    except Exception as e:
        return f"❌ 本地模型调用失败：{e}"
