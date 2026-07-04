"""应用配置."""
import os

from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件中的环境变量

# 数据库 — 默认 SQLite，设置 MYSQL_URL 环境变量切换 MySQL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:rootpassword@localhost:3306/naming_db")

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 小时

# 管理员 — 启动时自动创建
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123456")

# SMTP 邮件
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.qq.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", "")
