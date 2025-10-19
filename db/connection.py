import sqlite3

# -------------------------------
# 🔗 数据库连接上下文管理器
# -------------------------------
DB_PATH = "ripple.db"

def get_connection():
    return sqlite3.connect(DB_PATH)
