import streamlit as st
from config import DEFAULT_OLLAMA_URL, DEFAULT_LOCAL_MODEL_NAME, OPENAI_MODEL_OPTIONS
from i18n import SUPPORTED_LANGS

def sidebar_config(i18n):
    # 🌐 语言选择
    lang = st.session_state["lang"]
    lang_labels = list(SUPPORTED_LANGS.keys())
    lang_values = list(SUPPORTED_LANGS.values())

    try:
        current_index = lang_values.index(lang)
    except ValueError:
        current_index = 0

    selected_label = st.selectbox(
        "🌐 " + i18n.t("interface", "language"),
        lang_labels,
        index=current_index
    )

    new_lang = SUPPORTED_LANGS[selected_label]
    if new_lang != lang:
        st.session_state["lang"] = new_lang
        st.rerun()

    # 🤖 模型来源选择
    st.markdown("### " + i18n.t("model", "model_source"))
    model_options = [
        i18n.t("model", "local_model_option"),
        i18n.t("model", "openai_model_option")
    ]
    selected = st.selectbox(i18n.t("model", "model_source"), model_options)

    st.session_state["model_source"] = "local" if selected == model_options[0] else "openai"

    # 🧠 本地模型配置
    if st.session_state["model_source"] == "local":
        st.session_state["ollama_url"] = st.text_input(
            i18n.t("model", "ollama_url"),
            value=st.session_state.get("ollama_url", DEFAULT_OLLAMA_URL)
        )
        st.session_state["local_model"] = st.text_input(
            i18n.t("model", "model_name"),
            value=st.session_state.get("local_model", DEFAULT_LOCAL_MODEL_NAME)
        )
    else:
        # ☁️ OpenAI 模型选择（从 config.py 读取）
        st.session_state["openai_model"] = st.selectbox(
            i18n.t("model", "openai_model_select"),
            OPENAI_MODEL_OPTIONS
        )

    # 🌡️ 稳定度调节器
    st.markdown("### " + i18n.t("stability", "stability_title"))
    st.slider(
        i18n.t("stability", "stability_slider"),
        min_value=0.0,
        max_value=1.5,
        value=st.session_state.get("stability", 0.7),
        step=0.1,
        key="stability"
    )
