# ⚡ EcoGrid Core: Multi-Stage Production Industrial Docker Container
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies manifest
COPY requirements.txt .

# Install Python requirements
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy complete project codebase
COPY . .

# Expose Streamlit Dashboard (8501) and FastAPI REST API (8000)
EXPOSE 8501 8000

# Default command: Start Streamlit Command Cockpit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]