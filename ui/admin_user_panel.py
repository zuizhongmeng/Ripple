import streamlit as st
import pandas as pd
from db.connection import get_connection
from db.user import delete_user
from db.logs import export_search_logs

# -------------------------------
# 👥 管理员用户管理界面
# -------------------------------
def admin_user_panel(i18n):
    st.markdown("## 👥 " + i18n.t("interface", "admin_page") + "（管理员专属）")

    # ✅ 加载用户列表
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT username, role, created_at FROM users", conn)

    # 🔍 用户搜索过滤
    keyword = st.text_input("🔍 搜索用户名")
    if keyword:
        df = df[df["username"].str.contains(keyword)]

    # ✏️ 用户角色编辑器
    edited_df = st.data_editor(
        df,
        num_rows="fixed",
        column_config={
            "role": st.column_config.SelectboxColumn("角色", options=["admin", "user"])
        },
        use_container_width=True,
        key="user_editor"
    )

    # 💾 保存角色修改
    if st.button("💾 保存角色修改"):
        with get_connection() as conn:
            cursor = conn.cursor()
            for _, row in edited_df.iterrows():
                cursor.execute("UPDATE users SET role = ? WHERE username = ?", (row["role"], row["username"]))
            conn.commit()
        st.success("✅ 角色已更新")

    # 🗑️ 批量删除用户（排除 admin）
    st.markdown("### 🗑️ 批量删除用户")
    selectable = [u for u in df["username"].tolist() if u != "admin"]
    selected = st.multiselect("选择要删除的用户", selectable)

    if st.button("确认批量删除"):
        deleted = []
        for user in selected:
            delete_user(user)
            deleted.append(user)
        if deleted:
            st.success(f"✅ 已删除用户：{', '.join(deleted)}")
        else:
            st.info("ℹ️ 未删除任何用户")

    # 📊 用户图表视图
    st.markdown("### 📊 用户图表")
    view = st.selectbox("选择图表视图", ["角色分布", "登录活跃度"])

    if view == "角色分布":
        role_counts = df["role"].value_counts().reset_index()
        role_counts.columns = ["角色", "数量"]
        st.bar_chart(role_counts.set_index("角色"))
    else:
        with get_connection() as conn:
            logs = pd.read_sql_query("SELECT timestamp FROM login_logs", conn)
        logs["日期"] = pd.to_datetime(logs["timestamp"]).dt.date
        daily = logs["日期"].value_counts().sort_index()
        st.line_chart(daily)

    # 📤 搜索记录导出
    st.markdown("### 📤 搜索记录导出")
    export_user = st.text_input("导出指定用户搜索记录")
    if st.button("📤 导出搜索记录"):
        df_export = export_search_logs(export_user if export_user else None)
        if df_export.empty:
            st.info("该用户暂无搜索记录")
        else:
            csv = df_export.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "下载 CSV 文件",
                data=csv,
                file_name=f"{export_user or 'all'}_search_logs.csv",
                mime="text/csv"
            )
