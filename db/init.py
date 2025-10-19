from db.connection import get_connection

# -------------------------------
# 🧱 初始化数据库结构
# -------------------------------
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        # 🧑 用户表（含令牌字段）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                role TEXT,
                created_at TEXT,
                token_count INTEGER DEFAULT 10
            )
        """)

        # 📜 登录日志表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_logs (
                username TEXT,
                timestamp TEXT,
                success INTEGER
            )
        """)

        # 🔍 搜索记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                model TEXT,
                prompt TEXT,
                response TEXT,
                timestamp TEXT
            )
        """)

        conn.commit()
