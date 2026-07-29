"""
EcoGrid Core Master Production Startup Orchestrator
Pre-trains Kaggle ML models, launches internal Streamlit SCADA instance on 127.0.0.1:8501,
and launches public FastAPI Gateway server on 0.0.0.0:${PORT:-8000}.
"""

import os
import sys
import time
import subprocess
import uvicorn

# Ensure project root is present in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml_engine.train_models import train_all_models

def main():
    print("🚀 [ECOGRID CORE] Starting Production Gateway Master Orchestrator...")

    # 1. Pre-train ML models if not already present
    model_path = os.path.join("models", "traffic_congestion_model.joblib")
    if not os.path.exists(model_path):
        print("🤖 [ECOGRID ML] Pre-training Kaggle Machine Learning models...")
        train_all_models()

    # 2. Launch Internal Streamlit Server on 127.0.0.1:8501
    print("⚡ [STREAMLIT] Launching internal Streamlit SCADA Cockpit on 127.0.0.1:8501...")
    streamlit_cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.address", "127.0.0.1",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    streamlit_process = subprocess.Popen(
        streamlit_cmd,
        env=dict(os.environ, PYTHONPATH=os.path.dirname(os.path.abspath(__file__)))
    )

    # 3. Brief pause to allow Streamlit internal server initialization
    time.sleep(3.5)

    # 4. Launch Public FastAPI Gateway Server on 0.0.0.0:${PORT:-8000}
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 [FASTAPI GATEWAY] Starting public web gateway on 0.0.0.0:{port}...")

    try:
        uvicorn.run("api.server:app", host="0.0.0.0", port=port, log_level="info")
    except Exception as e:
        print(f"⚠️ Uvicorn process note: {e}")
    finally:
        print("🛑 Shutting down internal Streamlit process...")
        streamlit_process.terminate()

if __name__ == "__main__":
    main()
