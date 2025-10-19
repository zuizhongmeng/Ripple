import streamlit as st
from i18n.i18n import translator
from db.init import init_db
from services.user_service import ensure_guest_id
from ui.sidebar_config import sidebar_config
from ui.register_and_login import register_and_login
from ui.admin_user_panel import admin_user_panel
from ui.search_panel import show_search_ui
from ui.editor import editor
from ui.ui import sidebar_title

# -------------------------------
# 🧼 初始化 session_state 默认值
# -------------------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "zh"  # 默认语言设为中文

# -------------------------------
# 🌊 应用初始化
# -------------------------------

# 初始化数据库（如用户表、日志表等）
init_db()

# 确保匿名用户拥有唯一 guest_id 和默认角色
ensure_guest_id(st.session_state)

# -------------------------------
# 🌐 多语言翻译器设置
# -------------------------------

# 获取当前语言设置（默认为中文）
lang = st.session_state.get("lang", "zh")
translator.lang = lang
i18n = translator  # 简化引用

# -------------------------------
# 💠 侧边栏配置
# -------------------------------

with st.sidebar:
    # 显示侧边栏标题
    sidebar_title(i18n.t("interface", "page_title"))

    # 语言选择、模型配置、稳定度调节
    sidebar_config(i18n)

    # 登录 / 注册界面（含状态显示）
    register_and_login(i18n)

    # 页面选择（搜索 / 管理）
    page = st.selectbox(
        i18n.t("interface", "page_select"),
        [i18n.t("interface", "search_page"), i18n.t("interface", "admin_page")],
        key="page_select"
    )

# -------------------------------
# 📄 页面内容渲染
# -------------------------------

if page == i18n.t("interface", "search_page"):
    # 搜索界面（AI 回复 + 保存记录）
    show_search_ui(i18n)

elif page == i18n.t("interface", "admin_page"):
    # 管理员界面（用户管理 + 日志导出）
    if st.session_state.get("role") == "admin":
        admin_user_panel(i18n)
    else:
        st.warning(i18n.t("system", "admin_only"))
