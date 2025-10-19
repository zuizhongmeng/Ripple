import json
from datetime import datetime
import streamlit as st

# -------------------------------
# 💾 保存提示词版本（追加到 JSON 文件）
# -------------------------------
def save_prompt(prompt_text, task, tone, format, ai_reply=None, app_name="Ripple"):
    username = st.session_state.get("user") or st.session_state.get("guest_id")

    version = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "username": username,
        "task": task,
        "tone": tone,
        "format": format,
        "prompt": prompt_text,
        "ai_reply": ai_reply or "",
        "app_name": app_name
    }

    try:
        with open("prompt_versions.json", "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    history.append(version)
    with open("prompt_versions.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# -------------------------------
# 📖 加载当前用户的所有版本
# -------------------------------
def load_versions():
    username = st.session_state.get("user") or st.session_state.get("guest_id")

    try:
        with open("prompt_versions.json", "r", encoding="utf-8") as f:
            all_versions = json.load(f)
    except FileNotFoundError:
        return []

    return [v for v in all_versions if v.get("username") == username]

# -------------------------------
# 🔁 恢复指定版本（通过时间戳）
# -------------------------------
def restore_version(version_id):
    versions = load_versions()
    for v in versions:
        if v["timestamp"] == version_id:
            return v["prompt"], v["task"], v["tone"], v["format"]
    return "", "", "", ""
