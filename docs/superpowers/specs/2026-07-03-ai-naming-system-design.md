# AI 智能取名系统 — 设计文档

> 软件外包创新实践基地 2025 级新人实训 · 难度 1
> 日期：2026-07-03
> 作者：陈奕恺

---

## 1. 项目概述

基于大语言模型的在线取名系统。用户输入姓氏、性别、生日、时辰、风格偏好、寓意期望等信息，系统调用 DeepSeek API 生成名字建议及详细解释，支持多轮对话微调结果。

### 1.1 核心功能（难度 1）

- 匿名用户在网页端填写取名需求表单
- 后端拼装 prompt，调用 DeepSeek API
- 返回结构化名字列表（姓名、寓意、五行、出处）
- 支持对话式反馈微调（"更文艺一点"）
- 前端展示名字卡片，Apple 风格简洁设计

### 1.2 范围边界

| 不做 | 计划 |
|------|------|
| 注册/登录 | 难度 2 |
| 数据库存储 | 难度 2 |
| 取名历史记录 | 难度 2 |
| 付费/充值 | 难度 3 |
| 接口鉴权 | 难度 3 |
| 移动端适配 | 后续迭代 |
| Docker 部署 | 最后处理 |

---

## 2. 技术选型

| 层 | 选型 | 理由 |
|-----|------|------|
| 前端框架 | Vue 3 + Composition API + TypeScript | 开发者熟悉，生态成熟 |
| 构建工具 | Vite | 快 |
| 样式 | Tailwind CSS | 快速开发，保持一致 |
| 状态管理 | Pinia（难度 1 暂不用） | 为难度 2 预留 |
| 路由 | Vue Router | 为多页面升级预留 |
| 后端框架 | Python FastAPI | 自动生成 API 文档，异步支持 |
| LLM | DeepSeek API (deepseek-chat) | 便宜，中文能力强 |
| 包管理 | npm (前端) + pip (后端) | 标准 |

---

## 3. 项目结构

```
D:\Projects\ai-naming/
├── frontend/                       # Vue 3 + Vite
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.ts
│   │   ├── router/
│   │   │   └── index.ts            # 路由（难度1仅主页路由）
│   │   ├── views/
│   │   │   ├── HomeView.vue        # 难度1：取名主页
│   │   │   ├── LoginView.vue       # 难度2：占位
│   │   │   └── HistoryView.vue     # 难度2：占位
│   │   ├── components/
│   │   │   ├── NameForm.vue        # 取名表单
│   │   │   ├── NameResults.vue     # 名字结果卡片列表
│   │   │   └── RefineChat.vue      # 底部对话微调
│   │   ├── api/
│   │   │   └── index.ts            # axios 封装
│   │   ├── stores/                 # 难度2：Pinia stores（占位）
│   │   └── types/
│   │       └── index.ts            # TypeScript 类型
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── tailwind.config.js
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI 入口 + CORS
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── naming.py           # 难度1：取名接口
│   │   │   ├── auth.py             # 难度2：注册登录（占位）
│   │   │   └── payment.py          # 难度3：付费（占位）
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── naming_service.py   # prompt 拼装 + 结果解析
│   │   │   └── auth_service.py     # 难度2（占位）
│   │   ├── models/                 # 难度2：SQLAlchemy 模型（占位）
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── deepseek.py         # DeepSeek API 客户端
│   └── requirements.txt
└── docs/                           # 交付文档
    ├── superpowers/
    │   └── specs/
    │       └── 2026-07-03-ai-naming-system-design.md  # 本文件
    ├── 需求规格说明书.md            # 待写
    ├── 技术方案.md                  # 待写
    ├── 编译构建安装部署手册.md       # 待写
    └── 用户操作手册.md              # 待写
```

---

## 4. API 设计

### 4.1 架构模式

**方案 A：无状态 API**

前端管理对话历史，每次请求携带完整上下文。后端只负责拼 prompt + 调用 DeepSeek。无状态，简单可测试。

### 4.2 接口列表

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/naming/generate` | POST | 首次生成名字 |
| `/api/naming/refine` | POST | 根据用户反馈微调 |
| `/api/health` | GET | 健康检查 |

### 4.3 POST /api/naming/generate

**请求体：**
```json
{
  "surname": "陈",
  "gender": "male",
  "birthday": "2020-05-15",
  "birth_time": "辰时",
  "style": "文雅书香",
  "expectations": "希望名字有诗意，蕴含美好祝福"
}
```

**响应体：**
```json
{
  "conversation_id": "uuid-string",
  "names": [
    {
      "full_name": "陈书远",
      "meaning": "书香致远，寓意学识渊博志向远大",
      "wuxing": "金水相生",
      "source": "《礼记·学记》"
    }
  ]
}
```

### 4.4 POST /api/naming/refine

**请求体：**
```json
{
  "conversation_id": "uuid-string",
  "original_request": { /* 原始表单数据 */ },
  "history": [
    { "role": "user", "content": "太文艺了，想要大气一点的" },
    { "role": "assistant", "content": "好的，已调整..." }
  ],
  "feedback": "更大气硬朗一些"
}
```

**响应体：** 与 generate 同构。

### 4.5 错误响应

| 情况 | HTTP 状态 | body.message |
|------|-----------|--------------|
| 参数校验失败 | 422 | 具体缺失字段 |
| DeepSeek API 超时 | 504 | "AI 服务响应超时，请重试" |
| DeepSeek 返回不可解析 | 502 | "AI 返回格式异常，请重试" |
| 未知错误 | 500 | "服务异常，请稍后重试" |

通用错误响应格式：
```json
{
  "error": true,
  "message": "错误描述",
  "code": "ERROR_CODE"
}
```

---

## 5. Prompt 设计

### 5.1 System Prompt

```
你是一位专业的中国取名大师，精通五行八字、诗词典故、音律美学。
你的任务是根据用户提供的信息，生成高质量的中文名字建议。

要求：
1. 生成 5 个名字，每个名字 2-3 个字（含姓氏）
2. 名字要好听、有文化内涵、避免生僻字
3. 每个名字需提供：寓意解释、五行属性、文化出处
4. 严格按 JSON 格式返回，不要有其他文字

返回格式：
{
  "names": [
    {
      "full_name": "姓名",
      "meaning": "寓意解释（50字以内）",
      "wuxing": "五行属性",
      "source": "文化出处"
    }
  ]
}
```

### 5.2 User Prompt（generate）

根据表单字段动态拼装：

```
请为以下信息生成名字：
- 姓氏：{surname}
- 性别：{gender}
- 出生日期：{birthday}
- 出生时辰：{birth_time}
- 期望风格：{style}
- 其他期望：{expectations}
```

### 5.3 User Prompt（refine）

```
原始需求：
{original_request}

之前的对话：
{history_text}

用户的新反馈：{feedback}

请根据反馈重新生成名字，保持 JSON 格式。
```

---

## 6. 前端设计

### 6.1 设计风格

Apple 风格：大量留白、PingFang SC 字体、灰度主色、毛玻璃卡片、克制动效。

### 6.2 配色

| 用途 | Tailwind Class | 色值 |
|------|----------------|------|
| 页面背景 | `bg-[#f5f5f7]` | #f5f5f7 |
| 卡片背景 | `bg-white/80 backdrop-blur` | rgba(255,255,255,0.8) |
| 主文字 | `text-[#1d1d1f]` | #1d1d1f |
| 次要文字 | `text-[#86868b]` | #86868b |
| 强调色/按钮 | `bg-[#0071e3]` | #0071e3 |
| 分割线 | `border-[#d2d2d7]` | #d2d2d7 |

### 6.3 字体规格

- 页面标题：36px / font-semibold / #1d1d1f / tracking-tight
- 副标题：17px / font-normal / #86868b
- 表单标签：13px / font-medium / #86868b
- 表单值：17px / font-normal / #1d1d1f
- 名字：24px / font-semibold / #1d1d1f
- 名字含义：15px / font-normal / #3a3a3c
- 按钮文字：17px / font-medium / white

### 6.4 页面布局

单页面 HomeView.vue，三段式：

1. **标题区** — 大标题 + 副标题，居中，上下大量留白
2. **表单卡片** — 一行一个字段，底部一条 1px 分割线分隔，底部居中按钮
3. **结果区** — 5 张名字卡片纵向排列，每张含名字/寓意/五行/出处
4. **微调区** — 底部输入框，"不满意？"引导文字

### 6.5 组件职责

| 组件 | 输入 | 输出 | 不管 |
|------|------|------|------|
| NameForm | 无 | emit 表单数据 | API 调用 |
| NameResults | name[] prop | 无（纯展示） | API 调用 |
| RefineChat | conversationId | emit feedback | 首次生成 |
| HomeView | 无 | 协调三组件 | 具体 UI |

### 6.6 状态处理

| 状态 | 表单 | 结果区 | 微调区 |
|------|------|--------|--------|
| 初始 | 正常可用 | 空状态提示"输入信息后点击生成" | 隐藏 |
| 加载中 | 按钮禁用+旋转 | 骨架屏脉冲动画 | 隐藏 |
| 有结果 | 正常可用（可重新生成） | 卡片逐张淡入（stagger 0.1s） | 显示 |
| 错误 | 不变 | 红色错误提示+重试按钮 | 隐藏 |
| 空结果 | 不变 | "暂无结果，请调整后重试" | 隐藏 |

### 6.7 边界情况

- **快速双击**：按钮防抖 500ms
- **超长输入**：期望字段限 200 字，前端截断
- **网络断开**：axios 全局拦截，显示 toast 提示
- **API 返回非预期格式**：前端 try-catch，显示友好错误
- **空姓氏**：必填校验，submit 前检查

---

## 7. 数据流

```
用户填表单
  │
  ▼
HomeView: handleGenerate(formData)
  │
  ▼
api/index.ts: POST /api/naming/generate
  │
  ▼
routers/naming.py: 参数校验
  │
  ▼
services/naming_service.py: 拼装 system prompt + user prompt
  │
  ▼
utils/deepseek.py: HTTP POST → api.deepseek.com/chat/completions
  │
  ▼
naming_service.py: 解析 JSON 响应，提取 names[]
  │
  ▼
FastAPI: 返回 JSON → 前端
  │
  ▼
HomeView: 更新 names[] → NameResults 渲染卡片
  │
  ▼
用户输入反馈 → handleRefine(feedback, history)
  │
  ▼
POST /api/naming/refine → 同上流程 → 更新结果
```

---

## 8. 7 天实施计划

| 天 | 任务 | 产出 |
|----|------|------|
| 1 | 需求文档 + 技术方案文档 | 需求规格说明书.md、技术方案.md |
| 2 | 后端：FastAPI 项目骨架、DeepSeek 客户端 | main.py、deepseek.py 可单独测试 |
| 3 | 后端：naming_service prompt 调试、接口联调 | generate + refine 接口可用 curl 测试 |
| 4 | 前端：Vue 项目搭建、Tailwind 配置 | 项目跑起来，Apple 风格基础样式 |
| 5 | 前端：NameForm + NameResults + RefineChat | 三个组件完成，Mock 数据可展示 |
| 6 | 联调：前后端对接、错误处理、边界情况 | 完整流程可走通 |
| 7 | 部署文档 + 操作手册 + 最终测试 | 全部交付物就绪 |

---

## 9. 升级路径

### 难度 1 → 难度 2

| 模块 | 变化 |
|------|------|
| 数据库 | 新增 MySQL + SQLAlchemy models/ |
| 用户系统 | auth.py 占位 → 实现注册登录 + JWT |
| 前端 | 新增 LoginView + HistoryView，路由守卫 |
| 历史记录 | 新接口 GET /api/history + naming 结果入库 |
| 状态管理 | Pinia stores/ 接入，管理用户状态 |

### 难度 2 → 难度 3

| 模块 | 变化 |
|------|------|
| 付费 | 新增 payment.py + 充值页面 + 余额模型 |
| 安全 | Shiro 组件，接口鉴权 |
| 高级功能 | 自主调研设计（如八字详批、名字评分等） |
| 计费 | 按调用次数扣费，余额不足返回 402 |

---

## 10. 参考信息

- DeepSeek API 文档：https://platform.deepseek.com/api-docs
- FastAPI 文档：https://fastapi.tiangolo.com/
- Vue 3 文档：https://cn.vuejs.org/
- Tailwind CSS：https://tailwindcss.com/
