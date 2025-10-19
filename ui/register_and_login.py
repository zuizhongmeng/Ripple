import streamlit as st
from db.user import create_user, validate_login, user_exists
from db.logs import log_login

# -------------------------------
# 🔐 登录与注册界面（多语言支持）
# 注意：此函数由 app.py 外部用 st.sidebar 包裹
# -------------------------------
def register_and_login(i18n):
    # ✅ 已登录状态：显示欢迎信息与退出按钮
    if st.session_state.get("user"):
        st.success(f"{i18n.t('auth', 'logged_in')} `{st.session_state['user']}`")
        if st.button(i18n.t("auth", "logout")):
            st.session_state["user"] = None
            st.session_state["role"] = "guest"
            st.rerun()
        return

    # 🔐 登录 / 注册表单（展开区）
    with st.expander(i18n.t("auth", "login_box")):
        mode = st.selectbox(
            i18n.t("auth", "mode_select"),
            [i18n.t("auth", "login"), i18n.t("auth", "register")]
        )
        email = st.text_input(i18n.t("auth", "email"))
        password = st.text_input(i18n.t("auth", "password"), type="password")

        if st.button(i18n.t("auth", "submit_button")):
            if mode == i18n.t("auth", "register"):
                if user_exists(email):
                    st.error(i18n.t("auth", "user_exists"))
                else:
                    create_user(email, password)
                    st.success(i18n.t("auth", "register_success"))
                    st.stop()
            else:
                result = validate_login(email, password)
                log_login(email, success=bool(result))
                if result:
                    st.session_state["user"] = email
                    st.session_state["role"] = result[0]
                    st.toast(i18n.t("auth", "login_success"), icon="💧")
                    st.rerun()
                else:
                    st.error(i18n.t("auth", "login_fail"))
