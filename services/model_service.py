import requests
import json

# -------------------------------
# 🧠 本地模型调用（Ollama）
# -------------------------------
def call_ollama(prompt, model, url, temperature):
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        lines = response.text.strip().split("\n")
        result = ""
        for line in lines:
            try:
                obj = json.loads(line)
                result += obj.get("response", "")
            except json.JSONDecodeError:
                continue
        return result
    except requests.RequestException as e:
        return f"[Ollama 调用失败] {str(e)}"

# -------------------------------
# ☁️ OpenAI 中继调用（通过本地服务）
# -------------------------------
def call_openai_via_relay(prompt, model, username, temperature=0.7):
    payload = {
        "prompt": prompt,
        "username": username,
        "model": model,
        "temperature": temperature
    }
    try:
        response = requests.post("http://localhost:8000/ask", json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("result", "[无响应]")
    except requests.RequestException as e:
        return f"[中继调用失败] {str(e)}"
