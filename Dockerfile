FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

COPY frontend/dist/ ./static/

EXPOSE 8000

ENV ENVIRONMENT="production"
# SECRET_KEY、ADMIN_USERNAME、ADMIN_PASSWORD、DEEPSEEK_API_KEY 必须由部署平台注入。

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
