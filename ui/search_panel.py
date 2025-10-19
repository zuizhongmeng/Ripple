import streamlit as st
from services.unified_reply import reply
from services.prompt_history import save_prompt

# -------------------------------
# 🔍 搜索界面（独立模块）
# -------------------------------
def show_search_ui(i18n):
    st.title(i18n.t("interface", "search_page"))

    # ✅ 提示词输入框
    prompt = st.text_area(i18n.t("search", "search_input"))

    # ✅ 搜索按钮
    if st.button(i18n.t("search", "search_button")) and prompt.strip():
        st.info(i18n.t("search", "thinking"))

        result = reply(prompt)

        st.markdown("### " + i18n.t("search", "ai_response"))
        st.write(result)

        save_prompt(prompt, task="", tone="", format="", ai_reply=result)
