import random
import string

# -------------------------------
# 🧑 获取当前用户名（已登录或匿名）
# -------------------------------
def get_current_user(session):
    return session.get("user") or session.get("guest_id") or "unknown"

# -------------------------------
# 🔐 判断是否已登录
# -------------------------------
def is_logged_in(session):
    return session.get("user") is not None

# -------------------------------
# 🛡️ 判断是否为管理员
# -------------------------------
def is_admin(session):
    return session.get("role") == "admin"

# -------------------------------
# 🧭 获取当前用户角色
# -------------------------------
def get_user_role(session):
    return session.get("role", "guest")

# -------------------------------
# 🆔 确保匿名用户拥有 guest_id 和默认角色
# -------------------------------
def ensure_guest_id(session):
    if "guest_id" not in session:
        session["guest_id"] = f"guest_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"
    if "role" not in session:
        session["role"] = "guest"
