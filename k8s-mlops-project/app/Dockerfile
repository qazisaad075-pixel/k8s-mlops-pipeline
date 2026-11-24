FROM python:3.11-slim
RUN pip install --no-cache-dir --default-timeout=120 fastapi uvicorn
WORKDIR /app
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
