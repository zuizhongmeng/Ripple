import streamlit as st
from services.model_service import call_ollama, call_openai_via_relay

# -------------------------------
# 🧠 通用模型回复接口
# 自动根据侧边栏设置选择本地或 OpenAI 模型
# -------------------------------
def reply(prompt: str, stability_override: float = None) -> str:
    """
    参数：
    - prompt: 用户输入的提示词
    - stability_override: 可选的温度覆盖值（优先使用）

    返回：
    - 模型回复文本
    """
    source = st.session_state.get("model_source", "local")
    stability = stability_override if stability_override is not None else st.session_state.get("stability", 0.7)

    if source == "local":
        model = st.session_state.get("local_model", "deepseek-r1")
        url = st.session_state.get("ollama_url", "http://localhost:11434/api/generate")
        return call_ollama(prompt, model, url, stability)
    else:
        model = st.session_state.get("openai_model", "gpt-3.5-turbo")
        username = st.session_state.get("user") or st.session_state.get("guest_id")
        return call_openai_via_relay(prompt, model, username, stability)
