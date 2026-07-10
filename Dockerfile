FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

COPY frontend/dist/ ./static/

EXPOSE 8000

ENV DEEPSEEK_API_KEY=""
ENV DATABASE_URL="mysql+pymysql://root:password@host:3306/naming_db"
ENV SECRET_KEY=""
ENV ADMIN_USERNAME="admin"
ENV ADMIN_PASSWORD="admin123456"
ENV SMTP_HOST="smtp.qq.com"
ENV SMTP_PORT="587"
ENV SMTP_USER=""
ENV SMTP_PASSWORD=""
ENV SMTP_FROM=""

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
