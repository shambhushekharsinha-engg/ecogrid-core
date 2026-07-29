"""
EcoGrid Core Lightweight Startup Orchestrator
Optimized for 512MB RAM cloud environments (Render / PaaS).
Patches Tornado RequestHandler in-process for Render HEAD / health check 200 OK,
disables inotify file watchers, and runs Streamlit SCADA Command Cockpit on public $PORT.
"""

import os
import sys

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

def main():
    print("🚀 [ECOGRID CORE] Initializing Lightweight Production Cockpit...")

    # Determine public web port assigned by Render ($PORT or default 10000)
    port = os.environ.get("PORT", "10000")
    print(f"⚡ [STREAMLIT WEB COCKPIT] Launching primary web interface on 0.0.0.0:{port}...")

    # Programmatically run Streamlit in the SAME process (Memory footprint: ~210MB)
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
