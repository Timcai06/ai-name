FROM python:3.11-slim

WORKDIR /app

# 后端依赖
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 后端代码
COPY backend/ .

# 前端构建产物
COPY frontend/dist/ ./static/

EXPOSE 8000

ENV DEEPSEEK_API_KEY=""
ENV SECRET_KEY=""
ENV ADMIN_USERNAME="admin"
ENV ADMIN_PASSWORD="admin123456"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
