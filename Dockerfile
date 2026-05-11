# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (better Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app/ ./app/

# Expose the port uvicorn listens on
EXPOSE 8080

# GKE and Cloud Run both expect port 8080 by convention
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]