import streamlit as st
from services.prompt_history import save_prompt, load_versions, restore_version
from services.unified_reply import reply

# -------------------------------
# ✏️ 提示词编辑器界面
# -------------------------------
def editor(i18n):
    st.title(i18n.t("history", "title"))

    # ✅ 用户输入区域
    prompt = st.text_area("请输入提示词")
    task = st.text_input("任务类型", value="翻译")
    tone = st.selectbox("语气", ["正式", "随意", "幽默"], index=0)
    format = st.selectbox("格式", ["纯文本", "Markdown", "HTML"], index=1)

    # 🚀 提交并保存版本
    if st.button("提交") and prompt.strip():
        result = reply(prompt)
        st.write("模型回复：")
        st.write(result)

        save_prompt(
            prompt_text=prompt,
            task=task,
            tone=tone,
            format=format,
            ai_reply=result
        )

    # 🕰️ 加载历史版本
    versions = load_versions()
    if versions:
        selected_id = st.selectbox("选择一个历史版本", [v["timestamp"] for v in versions])
        if st.button(i18n.t("history", "restore_button")):
            restored_prompt, restored_task, restored_tone, restored_format = restore_version(selected_id)
            st.session_state["restored_prompt"] = restored_prompt
            st.session_state["restored_task"] = restored_task
            st.session_state["restored_tone"] = restored_tone
            st.session_state["restored_format"] = restored_format
            st.success(i18n.t("history", "restored_success"))
            st.rerun()
    else:
        st.info(i18n.t("history", "no_versions"))
