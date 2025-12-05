FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies and pip packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

# Ensure runtime directories exist
RUN mkdir -p /app/uploads /app/results /app/queue /app/logs

EXPOSE 8000

CMD ["uvicorn", "server_production:app", "--host", "0.0.0.0", "--port", "8000"]
