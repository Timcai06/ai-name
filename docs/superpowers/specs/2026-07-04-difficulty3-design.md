# AI 智能取名系统 — 难度 3 设计文档

> 日期：2026-07-04 | 基于难度 1+2 增量

## 1. 概述

三块内容：付费体系 + 高级功能 + 安全加固。

## 2. 付费体系

### 2.1 定价

| 功能 | 普通用户 | VIP(15元/月) | SVIP(30元/月) | 管理员 |
|------|---------|-------------|--------------|--------|
| 基础取名 | 免费 | 免费 | 免费 | 免费 |
| 名字分析 | 1元/次 | 10次/天 | 30次/天 | 免费 |
| 名字对比 | 1元/次 | 10次/天 | 30次/天 | 免费 |
| 精品取名 | 2元/次 | 10次/天 | 30次/天 | 免费 |
| 收藏 | 免费 | 免费 | 免费 | 免费 |
| 每日体验 | 1次/天 | — | — | — |

### 2.2 扣费优先级

```
1. 管理员？ → 免费通过
2. VIP/SVIP？ → 检查今日免费次数 → 够 → 扣次数
3. 普通用户 → 今日体验次数还有？ → 用掉
4. 扣余额 → 足够？ → 扣款 → 不足 → 402 余额不足
```

### 2.3 数据模型

```
users 加：
  balance: DECIMAL(10,2) DEFAULT 0        # 余额
  vip_level: VARCHAR(10) DEFAULT 'free'    # free/vip/svip
  vip_expire_at: DATETIME                  # 会员到期
  daily_free_used: INT DEFAULT 0           # 今日已用免费次数
  daily_exp_used: BOOLEAN DEFAULT FALSE    # 今日已用体验

新表 transactions:
  id, user_id, amount, type(recharge/consume/vip_buy),
  detail, balance_after, created_at

新表 daily_usage:
  id, user_id, date, feature_type, count, created_at

新表 favorites:
  id, user_id, name_item JSON, created_at
```

### 2.4 充值接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/payment/balance | 余额+会员+今日免费次数 |
| POST | /api/payment/recharge | 模拟充值 {amount: 10/20/50} |
| GET | /api/payment/transactions | 交易记录 |
| POST | /api/payment/buy-vip | 买VIP {level: vip/svip} |

### 2.5 充值页面

预设按钮 10元/20元/50元，点了就加钱（预留支付宝接口）。

---

## 3. 高级功能

### 3.1 名字对比 (POST /api/naming/compare)

输入 2-5 个名字 → AI 横向对比。

收费：1元/次（规则见上）。

输入：
```json
{"names": ["陈书远","陈墨白","陈泽宇"], "gender": "male"}
```

输出：
```json
{
  "rankings": [
    {"rank":1, "full_name":"陈书远", "score":92, "summary":"..."},
    ...
  ],
  "comparison": {
    "meaning": {"陈书远":9, "陈墨白":8, ...},
    "sound": {"陈书远":9, ...},
    "wuxing": {"陈书远":8, ...},
    "character": {"陈书远":8, ...}
  }
}
```

### 3.2 精品取名 (POST /api/naming/premium)

在基础取名上加：八字分析、音律评分、字形评价、重名概率。

收费：2元/次。

输入同 generate，输出额外含 bazi_analysis、score、popularity。

### 3.3 收藏夹

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/favorites | 收藏列表 |
| POST | /api/favorites | 收藏名字 {name_item} |
| DELETE | /api/favorites/{id} | 取消收藏 |

免费功能。

---

## 4. 安全加固

| 安全项 | 实现 |
|------|------|
| API 频率限制 | 每个 IP 每分钟最多 60 次（slowapi 库） |
| 登录暴力防护 | 同一 IP 连续失败 5 次 → 封 15 分钟 |
| 敏感操作验证 | 注销/改密需输入密码确认 |
| JWT 密钥检查 | 启动时警告默认密钥 |
| 请求日志中间件 | 所有 API 调用记日志 |
| 管理员防删 | admin 账号不可注销 |

---

## 5. 前端改动

```
HomeView：
  ┌─ 取名 ── 基础取名 ── 精品取名 ─┐（分段切换）
  └─ 名字分析 ── 名字对比 ─────────┘

新增：
  /balance     充值页面（余额+VIP+充值按钮）
  /favorites   收藏夹
  右上角加 💰余额 + ⭐收藏图标
```

---

## 6. 文件变动

```
后端新增：routers/payment.py, routers/favorites.py
          services/payment_service.py, middleware/rate_limit.py
          models/favorite.py, models/transaction.py, models/daily_usage.py

后端改造：naming.py（加扣费逻辑+compare+premium端点）
          user.py（注销需密码确认）
          auth.py（登录失败计数）
          main.py（注册新路由+安全中间件）

前端新增：views/BalanceView.vue, views/FavoritesView.vue
          components/CompareView.vue, components/PremiumForm.vue

前端改造：HomeView.vue（分段切换+进入时检查余额）
          api/index.ts（新增接口）
```
