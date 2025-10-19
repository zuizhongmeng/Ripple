from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from db.user import validate_login, get_token_count, deduct_token
import openai
import time
import os

app = FastAPI()

# -------------------------------
# 🔐 设置 OpenAI API 密钥
# -------------------------------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("请设置环境变量 OPENAI_API_KEY")
openai.api_key = api_key

# -------------------------------
# 🚦 简单频率限制（每 IP 每分钟最多 3 次）
# -------------------------------
rate_limit = {}
MAX_REQUESTS = 3
WINDOW = 60  # 秒

def check_rate_limit(ip: str) -> bool:
    now = time.time()
    history = rate_limit.get(ip, [])
    history = [t for t in history if now - t < WINDOW]
    if len(history) >= MAX_REQUESTS:
        return False
    history.append(now)
    rate_limit[ip] = history
    return True

# -------------------------------
# 📥 登录请求结构
# -------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

# -------------------------------
# 📤 模型请求结构
# -------------------------------
class Query(BaseModel):
    prompt: str
    username: str
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7

# -------------------------------
# 🔐 登录接口
# -------------------------------
@app.post("/login")
async def login(req: LoginRequest):
    result = validate_login(req.username, req.password)
    if result:
        return {"success": True, "role": result[0]}
    else:
        raise HTTPException(status_code=401, detail="登录失败")

# -------------------------------
# 🧠 模型调用接口
# -------------------------------
@app.post("/ask")
async def ask_openai(query: Query, request: Request):
    ip = request.client.host
    username = query.username

    # 🧨 检查令牌
    tokens = get_token_count(username)
    if tokens <= 0:
        raise HTTPException(status_code=403, detail="令牌已用尽")

    # 🚦 检查频率限制
    if not check_rate_limit(ip):
        raise HTTPException(status_code=429, detail="请求过于频繁")

    # 🧠 调用 OpenAI 模型
    try:
        response = openai.ChatCompletion.create(
            model=query.model,
            messages=[{"role": "user", "content": query.prompt}],
            temperature=query.temperature
        )
        result_text = response.choices[0].message.content

        # ✅ 扣除令牌（仅在成功后）
        deduct_token(username)

        return {
            "success": True,
            "data": {
                "result": result_text,
                "tokens_left": tokens - 1
            }
        }

    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"模型调用失败：{str(e)}")
    except Exception:
        raise HTTPException(status_code=500, detail="未知错误，请稍后再试")
