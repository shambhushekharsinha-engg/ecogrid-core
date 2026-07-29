"""
EcoGrid Core Production Startup Orchestrator
Pre-trains Kaggle ML models, patches Tornado RequestHandler in-process for Render HEAD / health check 200 OK,
disables inotify file watchers, launches FastAPI REST service on port 8000,
and runs Streamlit SCADA Command Cockpit on public $PORT.
"""

import os
import sys
import time
import subprocess

# Ensure project root is present in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Patch Tornado RequestHandler in-process BEFORE Streamlit Web Server initializes
try:
    import tornado.web
    def _safe_head(self, *args, **kwargs):
        self.set_status(200)
        self.finish()
    tornado.web.RequestHandler.head = _safe_head
except Exception as e:
    print(f"⚠️ Tornado patch note: {e}")

from ml_engine.train_models import train_all_models

def main():
    print("🚀 [ECOGRID CORE] Initializing Native Production Web Server...")

    # 1. Pre-train ML models if not already present
    model_path = os.path.join("models", "traffic_congestion_model.joblib")
    if not os.path.exists(model_path):
        print("🤖 [ECOGRID ML] Pre-training Kaggle Machine Learning models...")
        train_all_models()

    # 2. Launch FastAPI REST Microservice on background port 8000
    print("📡 [FASTAPI REST API] Starting background microservice on port 8000...")
    api_cmd = [
        sys.executable, "-m", "uvicorn", "api.server:app",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    try:
        subprocess.Popen(
            api_cmd,
            env=dict(os.environ, PYTHONPATH=os.path.dirname(os.path.abspath(__file__)))
        )
    except Exception as e:
        print(f"⚠️ FastAPI background note: {e}")

    # 3. Determine public web port assigned by Render ($PORT or default 10000 / 8501)
    port = os.environ.get("PORT", "10000")
    print(f"⚡ [STREAMLIT WEB COCKPIT] Launching primary web interface on 0.0.0.0:{port}...")

    # 4. Programmatically run Streamlit in the SAME process so Tornado retains the HEAD 200 OK patch
    sys.argv = [
        "streamlit", "run", "app.py",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.fileWatcherType", "none",
        "--browser.gatherUsageStats", "false",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]

    from streamlit.web.cli import main as streamlit_cli
    streamlit_cli()

if __name__ == "__main__":
    main()
