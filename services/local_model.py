import requests
from config import DEFAULT_OLLAMA_URL, DEFAULT_LOCAL_MODEL_NAME

# -------------------------------
# 🧠 本地模型调用（备用接口）
# -------------------------------
def local_model(prompt, model_name=None, temperature=0.7, ollama_url=None):
    """
    参数：
    - prompt: 用户输入的提示词
    - model_name: 模型名称（如 deepseek-r1, llama3 等）
    - temperature: 创意强度（0.0 ~ 1.0）
    - ollama_url: Ollama 服务地址（未指定时使用默认配置）

    返回：
    - 模型回复文本 或 错误信息
    """
    if not prompt:
        return "⚠️ 没有输入提示词"

    # 使用默认配置项
    if ollama_url is None:
        ollama_url = DEFAULT_OLLAMA_URL
    if model_name is None:
        model_name = DEFAULT_LOCAL_MODEL_NAME

    try:
        response = requests.post(
            ollama_url,
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
