"""邮件服务 — QQ邮箱 SMTP."""
import random
import smtplib
import string
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText

from sqlalchemy.orm import Session

from app.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM
from app.models.email_verification import EmailVerification

# 北京时间
CST = timezone(timedelta(hours=8))


def _send_email(to: str, subject: str, body: str):
    """底层 SMTP 发送."""
    msg = MIMEText(body, "html", "utf-8")
    msg["From"] = SMTP_FROM
    msg["To"] = to
    msg["Subject"] = subject

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(SMTP_FROM, [to], msg.as_string())
    server.quit()


def generate_code() -> str:
    """生成 6 位数字验证码."""
    return "".join(random.choices(string.digits, k=6))


def send_verification(db: Session, email: str, purpose: str) -> str:
    """发送验证码，返回 code。同一邮箱 60 秒内只能发一次."""
    # 频率限制：60秒
    one_minute_ago = datetime.now(CST) - timedelta(seconds=60)
    recent = (
        db.query(EmailVerification)
        .filter(
            EmailVerification.email == email,
            EmailVerification.purpose == purpose,
            EmailVerification.created_at > one_minute_ago,
        )
        .first()
    )
    if recent:
        raise ValueError("请60秒后再试")

    code = generate_code()
    expire_at = datetime.now(CST) + timedelta(minutes=10)

    record = EmailVerification(
        email=email,
        code=code,
        purpose=purpose,
        expire_at=expire_at,
    )
    db.add(record)
    db.commit()

    titles = {
        "bind": "绑定邮箱验证码",
        "reset_password": "重置密码验证码",
    }
    title = titles.get(purpose, "验证码")
    html = f"""<div style="max-width:480px;margin:0 auto;font-family:Arial,sans-serif">
<h2>AI 智能取名系统</h2>
<p>你的{title}为：</p>
<h1 style="color:#0071e3;font-size:36px;letter-spacing:4px">{code}</h1>
<p>有效期 10 分钟，请勿泄露。</p>
</div>"""
    _send_email(email, title, html)
    return code


def verify_code(db: Session, email: str, code: str, purpose: str) -> bool:
    """验证验证码是否正确且在有效期内."""
    record = (
        db.query(EmailVerification)
        .filter(
            EmailVerification.email == email,
            EmailVerification.code == code,
            EmailVerification.purpose == purpose,
            EmailVerification.used == False,
        )
        .order_by(EmailVerification.created_at.desc())
        .first()
    )
    if not record:
        return False
    now = datetime.now(CST)
    if record.expire_at.tzinfo is None:
        record.expire_at = record.expire_at.replace(tzinfo=CST)
    if now > record.expire_at:
        return False
    record.used = True
    db.commit()
    return True
