import streamlit as st

# -------------------------------
# 💠 统一侧边栏标题组件
# -------------------------------
def sidebar_title(label, icon="💧", size="16px", color="#333"):
    """
    在侧边栏中显示统一样式的标题。

    参数:
    - label: 标题文字
    - icon: 图标（可选）
    - size: 字体大小（默认 16px）
    - color: 字体颜色（默认深灰）
    """
    st.markdown(
        f"<p style='font-size:{size}; font-weight:600; color:{color}; margin-bottom:0.3em;'>{icon} {label}</p>",
        unsafe_allow_html=True
    )
