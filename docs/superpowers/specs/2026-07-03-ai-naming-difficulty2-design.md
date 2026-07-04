# AI 智能取名系统 — 难度 2 设计文档

> 难度 1 已完成 · 难度 2 增量设计
> 日期：2026-07-03

## 1. 增量概述

在难度 1（匿名取名 + 多轮微调）基础上增加：

| 新增 | 说明 |
|------|------|
| 注册/登录/登出 | JWT 认证，密码 bcrypt 哈希 |
| 路由守卫 | 未登录 → 强制跳转登录页 |
| 数据库（SQLAlchemy） | 默认 SQLite，改 URL 即切 MySQL |
| 3 张表（users + naming_history + auth_logs） | 用户 + 取名历史 + 认证日志 |
| 取名历史记录 | 登录后可查看过往所有取名结果 |
| 接口鉴权 | generate/refine/history 需登录 |
| 管理后台 | 仅 admin 可查看认证日志 + 全部取名记录 |

## 2. 数据库设计

使用 SQLAlchemy ORM，默认 SQLite，改 `DATABASE_URL` 即切 MySQL。

### users

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK AUTO_INCREMENT | 用户 ID |
| username | VARCHAR(50) UNIQUE NOT NULL | 用户名 |
| password_hash | VARCHAR(255) NOT NULL | bcrypt 哈希 |
| role | VARCHAR(20) DEFAULT 'user' | user / admin |
| created_at | DATETIME DEFAULT NOW | 注册时间 |

### naming_history

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK AUTO_INCREMENT | 记录 ID |
| user_id | INT FK → users.id | 归属用户 |
| surname | VARCHAR(5) | 姓氏 |
| gender | VARCHAR(10) | 性别 |
| birthday | VARCHAR(20) | 生日 |
| birth_time | VARCHAR(10) | 时辰 |
| style | VARCHAR(50) | 风格 |
| expectations | VARCHAR(200) | 期望 |
| result_json | TEXT | 名字结果 JSON |
| feedback | TEXT | 微调对话历史 JSON |
| created_at | DATETIME DEFAULT NOW | 生成时间 |

### auth_logs

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK AUTO_INCREMENT | 日志 ID |
| username | VARCHAR(50) NOT NULL | 用户名 |
| action | VARCHAR(20) NOT NULL | register/login/logout |
| ip_address | VARCHAR(45) | 客户端 IP |
| created_at | DATETIME DEFAULT NOW | 操作时间 |

## 3. API

| 方法 | 路径 | 鉴权 | 说明 |
|------|------|------|------|
| POST | /api/auth/register | 无 | 注册 |
| POST | /api/auth/login | 无 | 登录，返回 JWT |
| POST | /api/auth/logout | JWT | 登出 |
| POST | /api/naming/generate | JWT | 生成名字 + 保存历史 |
| POST | /api/naming/refine | JWT | 微调名字 |
| GET | /api/naming/history | JWT | 历史列表 |
| GET | /api/naming/history/{id} | JWT | 历史详情 |

## 4. 后端改动

```
新增：database.py, config.py, middleware/auth.py
新增：models/user.py, models/naming_history.py, models/auth_log.py
实现：routers/auth.py, routers/admin.py, services/auth_service.py
改造：routers/naming.py（加 JWT 依赖 + 入库保存历史）
```

## 5. 前端改动

```
新增：LoginView.vue, HistoryView.vue
新增：stores/auth.ts (Pinia)
改造：router/index.ts（路由守卫）
改造：HomeView.vue（header 显示用户 + 登出）
改造：api/index.ts（token 注入 + 新接口）
```

## 6. 新依赖

| 层 | 包 | 用途 |
|-----|-----|------|
| 后端 | sqlalchemy | ORM |
| 后端 | pymysql | MySQL 驱动 |
| 后端 | python-jose[cryptography] | JWT 签发/验证 |
| 后端 | passlib[bcrypt] | 密码哈希 |
| 前端 | pinia | 状态管理 |
