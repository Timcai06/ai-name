"""付费服务 — 充值、VIP、扣费、免费次数检查."""
from datetime import datetime, date, timezone, timedelta

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.transaction import Transaction
from app.models.daily_usage import DailyUsage

CST = timezone(timedelta(hours=8))

# 定价
PRICES = {"analyze": 1.0, "compare": 1.0, "premium": 2.0}
VIP_DAILY_LIMIT = {"vip": 10, "svip": 30}
VIP_PRICES = {"vip": 15.0, "svip": 30.0}


def recharge(db: Session, user: User, amount: float) -> float:
    """充值，返回新余额."""
    user.balance += amount
    _log_transaction(db, user, amount, "recharge", f"充值 {amount} 元")
    db.commit()
    return user.balance


def buy_vip(db: Session, user: User, level: str) -> dict:
    """购买VIP."""
    price = VIP_PRICES.get(level, 15.0)
    if user.balance < price:
        raise ValueError(f"余额不足，需要 {price} 元，当前余额 {user.balance} 元")
    user.balance -= price
    _log_transaction(db, user, -price, "vip_buy", f"购买 {level.upper()} 会员（30天）")
    user.vip_level = level
    now = datetime.now(CST)
    if user.vip_expire_at and user.vip_expire_at.replace(tzinfo=CST) > now:
        user.vip_expire_at = user.vip_expire_at.replace(tzinfo=CST) + timedelta(days=30)
    else:
        user.vip_expire_at = now + timedelta(days=30)
    db.commit()
    return {"balance": user.balance, "vip_level": level, "vip_expire_at": user.vip_expire_at.isoformat()}


def check_and_deduct(db: Session, user: User, feature: str) -> dict:
    """检查是否可以免费/付费使用，可以则扣费/扣次数。返回状态."""
    # 管理员免费
    if user.role == "admin":
        return {"allowed": True, "reason": "admin"}

    # 检查VIP是否过期
    now = datetime.now(CST)
    if user.vip_level != "free" and user.vip_expire_at:
        if user.vip_expire_at.replace(tzinfo=CST) < now:
            user.vip_level = "free"
            user.vip_expire_at = None
            db.commit()

    today = date.today()

    # VIP/SVIP：检查每日免费次数
    if user.vip_level in ("vip", "svip"):
        limit = VIP_DAILY_LIMIT[user.vip_level]
        usage = (
            db.query(DailyUsage)
            .filter(DailyUsage.user_id == user.id, DailyUsage.usage_date == today)
            .first()
        )
        today_free = usage.count if usage else 0
        if today_free < limit:
            _incr_daily(db, user, today, feature)
            return {"allowed": True, "reason": f"vip_{user.vip_level}", "remaining_free": limit - today_free - 1}

    # 普通用户每日体验
    if not user.daily_exp_used:
        user.daily_exp_used = True
        db.commit()
        return {"allowed": True, "reason": "daily_exp"}

    # 扣余额
    price = PRICES.get(feature, 1.0)
    if user.balance < price:
        return {"allowed": False, "reason": "insufficient_balance", "price": price, "balance": user.balance}

    user.balance -= price
    _log_transaction(db, user, -price, "consume", f"{feature} 消费")
    db.commit()
    return {"allowed": True, "reason": "paid", "price": price, "balance_after": user.balance}


def get_balance_info(db: Session, user: User) -> dict:
    """获取余额+VIP+免费次数信息."""
    info = {
        "balance": user.balance,
        "vip_level": user.vip_level,
        "vip_expire_at": user.vip_expire_at.isoformat() if user.vip_expire_at else None,
        "daily_exp_used": user.daily_exp_used,
    }
    if user.vip_level in ("vip", "svip"):
        today = date.today()
        usage = (
            db.query(DailyUsage)
            .filter(DailyUsage.user_id == user.id, DailyUsage.usage_date == today)
            .first()
        )
        limit = VIP_DAILY_LIMIT[user.vip_level]
        info["daily_free_used"] = usage.count if usage else 0
        info["daily_free_limit"] = limit
    return info


def _incr_daily(db: Session, user: User, today: date, feature: str):
    usage = db.query(DailyUsage).filter(DailyUsage.user_id == user.id, DailyUsage.usage_date == today).first()
    if usage:
        usage.count += 1
    else:
        db.add(DailyUsage(user_id=user.id, usage_date=today, feature_type=feature, count=1))
    db.commit()


def _log_transaction(db: Session, user: User, amount: float, ttype: str, detail: str):
    db.add(Transaction(user_id=user.id, amount=amount, type=ttype, detail=detail, balance_after=user.balance))
