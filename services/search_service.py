from db.logs import save_search, load_user_history

# -------------------------------
# 💾 保存用户搜索记录
# -------------------------------
def save_user_search(username, prompt, response, model):
    save_search(username, prompt, response, model)

# -------------------------------
# 📜 获取用户搜索历史
# -------------------------------
def get_user_history(username):
    return load_user_history(username)
