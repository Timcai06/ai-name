# AI 智能取名系统

基于 DeepSeek 大语言模型的智能取名系统。支持基础取名、AI名字分析、名字对比、精品取名。

## 技术栈

- 前端：Vue 3 + Vite + Tailwind CSS
- 后端：Python FastAPI + SQLAlchemy
- AI：DeepSeek API
- 数据库：SQLite（可切换 MySQL）
- 认证：JWT + bcrypt

## 快速开始

### 开发环境

```bash
# 后端
cd backend
pip install -r requirements.txt
cp .env.example .env  # 编辑配置 DEEPSEEK_API_KEY
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 前端
cd frontend
npm install
npm run dev
```

浏览器访问 http://localhost:5173

### Docker 部署

```bash
docker build -t ai-naming .
docker run -p 8000:8000 -e DEEPSEEK_API_KEY=your-key ai-naming
```

## 项目文档

- [需求规格说明书](docs/需求规格说明书.md)
- [技术方案](docs/技术方案.md)
- [编译构建安装部署手册](docs/编译构建安装部署手册.md)
- [用户操作手册](docs/用户操作手册.md)
- [开发调试指南](docs/开发调试指南.md)
