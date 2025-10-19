import sqlite3
from db.user import hash_pw  # ✅ 使用统一的密码加密函数
from datetime import datetime

# -------------------------------
# 🗄️ 连接数据库
# -------------------------------
try:
    conn = sqlite3.connect("ripple.db")
    cursor = conn.cursor()

    # -------------------------------
    # 🧱 删除旧表（开发阶段使用）
    # -------------------------------
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS search_logs")

    # -------------------------------
    # 🧱 创建表结构
    # -------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL,
            token_count INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            model TEXT NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    # -------------------------------
    # 👑 添加管理员用户
    # -------------------------------
    user_admin = {
        "username": "admin@example.com",
        "password": hash_pw("admin123"),
        "role": "admin",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "token_count": 999
    }

    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, role, created_at, token_count)
        VALUES (?, ?, ?, ?, ?)
    """, tuple(user_admin.values()))

    # -------------------------------
    # 👤 添加测试用户
    # -------------------------------
    user_test = {
        "username": "test_user@example.com",
        "password": hash_pw("test123"),
        "role": "user",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "token_count": 10
    }

    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, role, created_at, token_count)
        VALUES (?, ?, ?, ?, ?)
    """, tuple(user_test.values()))

    # -------------------------------
    # 🔍 添加搜索记录
    # -------------------------------
    search_log = {
        "username": user_test["username"],
        "model": "gpt-3.5-turbo",
        "prompt": "什么是傅里叶变换？",
        "response": "傅里叶变换是一种将信号从时域转换到频域的数学工具...",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    cursor.execute("""
        INSERT INTO search_logs (username, model, prompt, response, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, tuple(search_log.values()))

    # -------------------------------
    # ✅ 提交并关闭
    # -------------------------------
    conn.commit()
    print("✅ 测试数据已添加")

except Exception as e:
    print(f"❌ 初始化失败：{e}")

finally:
    conn.close()
