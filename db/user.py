from db.connection import get_connection
from datetime import datetime
import hashlib

# -------------------------------
# 🔐 密码加密函数（SHA256）
# -------------------------------
def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------------------
# 🧑 创建用户（含初始令牌）
# -------------------------------
def create_user(username, password="", role="user", tokens=10):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hashed_pw = hash_pw(password) if password else ""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, password, role, created_at, token_count)
            VALUES (?, ?, ?, ?, ?)
        """, (username, hashed_pw, role, now, tokens))
        conn.commit()

# -------------------------------
# 🔍 检查用户是否存在
# -------------------------------
def user_exists(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        return cursor.fetchone() is not None

# -------------------------------
# 🔐 验证登录（返回角色）
# -------------------------------
def validate_login(username, password):
    hashed = hash_pw(password)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, hashed))
        return cursor.fetchone()

# -------------------------------
# 🧠 获取用户剩余令牌
# -------------------------------
def get_token_count(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT token_count FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result[0] if result else 0

# -------------------------------
# 🧨 扣除用户令牌（每次调用）
# -------------------------------
def deduct_token(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET token_count = token_count - 1 WHERE username = ?", (username,))
        conn.commit()

# -------------------------------
# 🗑️ 删除用户及其相关记录
# -------------------------------
def delete_user(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        cursor.execute("DELETE FROM login_logs WHERE username = ?", (username,))
        cursor.execute("DELETE FROM search_logs WHERE username = ?", (username,))
        conn.commit()
