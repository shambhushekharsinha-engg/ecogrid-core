# ────────────── ECOGRID CORE DOCKERFILE ──────────────
FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and Kaggle dataset assets
COPY . .

# Pre-train Kaggle Machine Learning models during build stage
RUN PYTHONPATH=/app python -m ml_engine.train_models

# Expose Streamlit Dashboard (8501) and FastAPI REST API (8000)
EXPOSE 8501 8000

# Default entrypoint starts both REST API and Streamlit UI
CMD uvicorn api.server:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0