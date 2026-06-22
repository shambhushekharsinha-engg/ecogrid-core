# Use a slim, secure production Python image base layer
FROM python:3.11-slim

# Set high-performance runtime optimization flags
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true

# Set the internal storage workspace
WORKDIR /app

# Install system dependencies needed for compiling specific C-extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy over package dependency lists first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all decoupled folder matrices into the container workspace
COPY . .

# Expose Streamlit's default SCADA network routing port
EXPOSE 8501

# Healthcheck endpoint verification pass
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch the interactive web engine
CMD ["streamlit", "run", "app.py"]