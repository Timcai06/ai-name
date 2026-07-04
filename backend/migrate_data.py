"""SQLite → MySQL 数据迁移脚本."""
import sqlite3
import pymysql

# 源 (SQLite)
sqlite = sqlite3.connect("naming.db")
sqlite.row_factory = sqlite3.Row

# 目标 (MySQL)
mysql = pymysql.connect(
    host="localhost", port=3306,
    user="root", password="rootpassword",
    database="naming_db", charset="utf8mb4"
)
mc = mysql.cursor()

# 清空 MySQL 表（保留结构）
tables = ["users", "naming_history", "auth_logs", "email_verifications", "transactions", "daily_usage", "favorites"]
for t in tables:
    mc.execute(f"DELETE FROM {t}")
mysql.commit()

print("MySQL 表已清空，开始迁移...")

# ── users ──
rows = sqlite.execute("SELECT * FROM users").fetchall()
for r in rows:
    mc.execute(
        "INSERT INTO users (id, username, password_hash, role, email, avatar, nickname, is_deleted, balance, vip_level, vip_expire_at, daily_free_used, daily_exp_used, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (r["id"], r["username"], r["password_hash"], r["role"] or "user", r["email"], r["avatar"], r["nickname"], r["is_deleted"] or 0, r["balance"] or 0, r["vip_level"] or "free", r["vip_expire_at"], r["daily_free_used"] or 0, r["daily_exp_used"] or 0, r["created_at"])
    )
print(f"users: {len(rows)} 行")

# ── naming_history ──
rows = sqlite.execute("SELECT * FROM naming_history").fetchall()
for r in rows:
    mc.execute(
        "INSERT INTO naming_history (id, user_id, surname, gender, birthday, birth_time, style, expectations, result_json, feedback, is_deleted, record_type, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (r["id"], r["user_id"], r["surname"], r["gender"], r["birthday"], r["birth_time"], r["style"], r["expectations"], r["result_json"], r["feedback"], r["is_deleted"] or 0, r["record_type"] or "naming", r["created_at"])
    )
print(f"naming_history: {len(rows)} 行")

# ── auth_logs ──
rows = sqlite.execute("SELECT * FROM auth_logs").fetchall()
for r in rows:
    mc.execute(
        "INSERT INTO auth_logs (id, username, action, ip_address, created_at) VALUES (%s,%s,%s,%s,%s)",
        (r["id"], r["username"], r["action"], r["ip_address"], r["created_at"])
    )
print(f"auth_logs: {len(rows)} 行")

# ── email_verifications ──
try:
    rows = sqlite.execute("SELECT * FROM email_verifications").fetchall()
    for r in rows:
        mc.execute(
            "INSERT INTO email_verifications (id, email, code, purpose, used, expire_at, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (r["id"], r["email"], r["code"], r["purpose"], r["used"] or 0, r["expire_at"], r["created_at"])
        )
    print(f"email_verifications: {len(rows)} 行")
except:
    print("email_verifications: 0 行 (表不存在)")

# ── transactions ──
try:
    rows = sqlite.execute("SELECT * FROM transactions").fetchall()
    for r in rows:
        mc.execute(
            "INSERT INTO transactions (id, user_id, amount, type, detail, balance_after, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (r["id"], r["user_id"], r["amount"], r["type"], r["detail"], r["balance_after"], r["created_at"])
        )
    print(f"transactions: {len(rows)} 行")
except:
    print("transactions: 0 行 (表不存在)")

# ── daily_usage ──
try:
    rows = sqlite.execute("SELECT * FROM daily_usage").fetchall()
    for r in rows:
        mc.execute(
            "INSERT INTO daily_usage (id, user_id, usage_date, feature_type, count, created_at) VALUES (%s,%s,%s,%s,%s,%s)",
            (r["id"], r["user_id"], r["usage_date"], r["feature_type"], r["count"], r["created_at"])
        )
    print(f"daily_usage: {len(rows)} 行")
except:
    print("daily_usage: 0 行 (表不存在)")

# ── favorites ──
try:
    rows = sqlite.execute("SELECT * FROM favorites").fetchall()
    for r in rows:
        mc.execute(
            "INSERT INTO favorites (id, user_id, full_name, name_data, created_at) VALUES (%s,%s,%s,%s,%s)",
            (r["id"], r["user_id"], r["full_name"], r["name_data"], r["created_at"])
        )
    print(f"favorites: {len(rows)} 行")
except:
    print("favorites: 0 行 (表不存在)")

mysql.commit()
print("\n✅ 数据迁移完成！")

sqlite.close()
mc.close()
mysql.close()
