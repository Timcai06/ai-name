"""安全中间件 — 频率限制 + 登录保护."""
import time
from collections import defaultdict

from fastapi import Request, HTTPException, status

# 频率限制
RATE_LIMIT = 60  # 每分钟最多请求数
rate_store: dict[str, list[float]] = defaultdict(list)

# 登录保护
MAX_LOGIN_FAILS = 5
BLOCK_DURATION = 900  # 15分钟
login_fails: dict[str, list[float]] = defaultdict(list)


def check_rate_limit(ip: str) -> bool:
    """检查IP是否超过频率限制，返回True=允许."""
    now = time.time()
    window = now - 60
    rate_store[ip] = [t for t in rate_store[ip] if t > window]
    rate_store[ip].append(now)
    return len(rate_store[ip]) <= RATE_LIMIT


def check_login_block(ip: str) -> bool:
    """检查IP是否被封，返回True=被封."""
    now = time.time()
    fails = [t for t in login_fails.get(ip, []) if t > now - BLOCK_DURATION]
    login_fails[ip] = fails
    if len(fails) >= MAX_LOGIN_FAILS:
        return True
    return False


def record_login_fail(ip: str):
    """记录登录失败."""
    login_fails[ip].append(time.time())


def reset_login_fails(ip: str):
    """登录成功后清除失败记录."""
    login_fails.pop(ip, None)


async def rate_limit_middleware(request: Request, call_next):
    """FastAPI 中间件：频率限制."""
    ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(ip):
        raise HTTPException(status_code=429, detail="请求过于频繁，请稍后重试")
    response = await call_next(request)
    return response
