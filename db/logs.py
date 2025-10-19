from db.connection import get_connection
from datetime import datetime
import pandas as pd

# -------------------------------
# 📜 登录日志记录
# -------------------------------
def log_login(username, success):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login_logs VALUES (?, ?, ?)", (username, now, success))
        conn.commit()

# -------------------------------
# 💾 保存搜索记录
# -------------------------------
def save_search(username, prompt, response, model):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO search_logs (username, model, prompt, response, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (username, model, prompt, response, now))
        conn.commit()

# -------------------------------
# 📜 加载用户搜索历史
# -------------------------------
def load_user_history(username, limit=100, offset=0):
    with get_connection() as conn:
        query = """
            SELECT prompt, response, model, timestamp
            FROM search_logs
            WHERE username = ?
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        """
        return pd.read_sql_query(query, conn, params=(username, limit, offset))

# -------------------------------
# 📤 导出搜索记录（全部或指定用户）
# -------------------------------
def export_search_logs(username=None):
    with get_connection() as conn:
        query = "SELECT * FROM search_logs"
        if username:
            return pd.read_sql_query(query + " WHERE username = ?", conn, params=(username,))
        else:
            return pd.read_sql_query(query, conn)
