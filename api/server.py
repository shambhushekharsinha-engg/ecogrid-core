"""
Production FastAPI REST Microservice Server for EcoGrid Core Infrastructure
Exposes RESTful endpoints for Authentication, ML Predictions, Smart City Traffic & EV Load,
AI Copilot Q&A, Multi-Currency Conversion, BFT Consensus, Cryptographic Ledger, and Retraining.
Also serves as a Web Gateway reverse-proxying Streamlit SCADA UI to localhost:8501.
"""

import os
import sys
import asyncio
import httpx
import websockets
from fastapi import FastAPI, HTTPException, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Ensure project root is present in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from security.auth import auth_manager
from ml_engine.predictor import predictor
from ml_engine.train_models import train_all_models
from core.traffic_engine import EcoGridTrafficEngine
from core.consensus_engine import BFTConsensusEngine
from core.mitigation_engine import GroundLevelMitigation
from security.crypto_ledger import CryptographicLedger
from cloud_auditor import auditor

app = FastAPI(
    title="EcoGrid Core Enterprise REST API",
    description="RESTful Microservice API powering Microgrid SCADA, Smart City Traffic & EV Load Optimization, 3/3 BFT Consensus, AI Copilot, and Kaggle AI Predictors.",
    version="6.5.0-PROD"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ledger = CryptographicLedger()

STREAMLIT_INTERNAL_HTTP = "http://127.0.0.1:8501"
STREAMLIT_INTERNAL_WS = "ws://127.0.0.1:8501"

# ────────────── REQUEST & RESPONSE SCHEMAS ──────────────
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, json_schema_extra={"example": "ecogrid_operator"})
    password: str = Field(..., min_length=8, json_schema_extra={"example": "StrongPass@123"})
    role: str = Field("Operator", json_schema_extra={"example": "Microgrid Chief Engineer"})

class LoginRequest(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "admin"})
    password: str = Field(..., json_schema_extra={"example": "Admin@123"})

class DemoLoginRequest(BaseModel):
    role_preset: str = Field(..., json_schema_extra={"example": "admin"})

class TrafficPredictionRequest(BaseModel):
    vehicle_count: int = Field(..., json_schema_extra={"example": 950})
    avg_speed_kmh: float = Field(..., json_schema_extra={"example": 22.5})
    weather: str = Field("SUNNY", json_schema_extra={"example": "SUNNY"})
    hour: int = Field(14, json_schema_extra={"example": 17})

class SignalOptimizeRequest(BaseModel):
    intersection_id: str = Field(..., json_schema_extra={"example": "INT_ALPHA_CBD"})
    vehicle_count: int = Field(..., json_schema_extra={"example": 950})
    cross_street_count: int = Field(250, json_schema_extra={"example": 300})
    emergency_flag: bool = Field(False, json_schema_extra={"example": False})

class EVBalanceRequest(BaseModel):
    grid_load_kw: float = Field(..., json_schema_extra={"example": 1650.0})
    max_capacity_kw: float = Field(2000.0, json_schema_extra={"example": 2000.0})
    queued_evs: int = Field(15, json_schema_extra={"example": 20})

class GridLoadPredictRequest(BaseModel):
    ambient_temp_c: float = Field(32.0, json_schema_extra={"example": 34.5})
    humidity_pct: float = Field(50.0, json_schema_extra={"example": 45.0})
    ev_station_kw: float = Field(600.0, json_schema_extra={"example": 750.0})
    hour: int = Field(16, json_schema_extra={"example": 17})
    is_peak_price: int = Field(1, json_schema_extra={"example": 1})

class BFTConsensusRequest(BaseModel):
    proposed_action: str = Field("SIGNAL_PHASE_OVERRIDE", json_schema_extra={"example": "SIGNAL_PHASE_OVERRIDE"})
    target_node: str = Field("Node_Alpha_Residential", json_schema_extra={"example": "Node_Alpha_Residential"})
    grid_freq_hz: float = Field(50.0, json_schema_extra={"example": 50.0})

class AICopilotRequest(BaseModel):
    user_query: str = Field(..., json_schema_extra={"example": "How does EcoGrid Core optimize signal timing during peak hours?"})
    context_data: dict = Field({}, json_schema_extra={"example": {"active_intersection": "INT_ALPHA_CBD"}})

class CurrencyConvertRequest(BaseModel):
    price_inr: float = Field(..., json_schema_extra={"example": 3500.0})
    target_country_code: str = Field("US", json_schema_extra={"example": "US"})

# ────────────── NATIVE FASTAPI REST ENDPOINTS ──────────────
@app.get("/health")
def health_check():
    return {
        "status": "ONLINE",
        "service": "EcoGrid Core Enterprise REST API",
        "version": "6.5.0-PROD",
        "loaded_ml_models": list(predictor.models.keys()),
        "supported_countries": list(GroundLevelMitigation.COUNTRY_MATRIX.keys()),
        "database_backend": "PostgreSQL" if os.environ.get("DATABASE_URL") else "SQLite (Local Embedded)"
    }

# ──── AUTHENTICATION ENDPOINTS ────
@app.post("/api/v1/auth/register")
def register_user(req: RegisterRequest):
    success, result = auth_manager.register_user(req.username, req.password, req.role)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return {"success": True, "message": result}

@app.post("/api/v1/auth/login")
def login_user(req: LoginRequest):
    success, result = auth_manager.authenticate_user(req.username, req.password)
    if not success:
        raise HTTPException(status_code=401, detail=result)
    return {"success": True, "user": result}

@app.post("/api/v1/auth/demo-login")
def demo_login(req: DemoLoginRequest):
    preset = req.role_preset.lower()
    if preset not in auth_manager.DEMO_USERS:
        raise HTTPException(status_code=400, detail=f"Invalid preset. Choose from: {list(auth_manager.DEMO_USERS.keys())}")
    meta = auth_manager.DEMO_USERS[preset]
    success, result = auth_manager.authenticate_user(preset, meta["password"])
    if not success:
        raise HTTPException(status_code=500, detail="Demo login failed.")
    return {"success": True, "user": result}

# ──── ECOGRID TRAFFIC & EV GRID ENDPOINTS ────
@app.post("/api/v1/predict/traffic")
def predict_traffic(req: TrafficPredictionRequest):
    metrics = EcoGridTrafficEngine.calculate_intersection_metrics(
        req.vehicle_count, req.avg_speed_kmh, req.weather, req.hour
    )
    return {"success": True, "data": metrics}

@app.post("/api/v1/traffic/optimize-signal")
def optimize_signal(req: SignalOptimizeRequest):
    plan = EcoGridTrafficEngine.optimize_signal_timing(
        req.intersection_id, req.vehicle_count, req.cross_street_count, req.emergency_flag
    )
    ledger.record_transaction("EcoGrid_Traffic_Orchestrator", "SIGNAL_PHASE_OPTIMIZE", plan)
    return {"success": True, "signal_plan": plan}

@app.post("/api/v1/traffic/ev-balance")
def balance_ev_charging(req: EVBalanceRequest):
    res = EcoGridTrafficEngine.balance_ev_charging_queue(
        req.grid_load_kw, req.max_capacity_kw, req.queued_evs
    )
    return {"success": True, "data": res}

# ──── AI COPILOT & MULTI-CURRENCY ────
@app.post("/api/v1/ai/copilot")
def ai_copilot_query(req: AICopilotRequest):
    answer = auditor.answer_user_query(req.user_query, req.context_data)
    return {"success": True, "data": answer}

@app.post("/api/v1/currency/convert")
def convert_currency(req: CurrencyConvertRequest):
    val, formatted = GroundLevelMitigation.convert_price_from_inr(req.price_inr, req.target_country_code)
    mitigation = GroundLevelMitigation.calculate_regional_mitigation(150.0, req.target_country_code)
    return {
        "success": True,
        "input_price_inr": req.price_inr,
        "target_country": req.target_country_code.upper(),
        "converted_value": val,
        "formatted_price": formatted,
        "regional_mitigation": mitigation
    }

# ──── ML INFERENCE & GRID DISPATCH ────
@app.post("/api/v1/predict/load")
def predict_grid_load(req: GridLoadPredictRequest):
    load_kw = predictor.predict_grid_load(
        req.ambient_temp_c, req.humidity_pct, req.ev_station_kw, req.hour, req.is_peak_price
    )
    return {"success": True, "predicted_grid_load_kw": load_kw}

@app.post("/api/v1/scada/bft-consensus")
def evaluate_bft_consensus(req: BFTConsensusRequest):
    res = BFTConsensusEngine.evaluate_state_proposal(
        req.proposed_action, req.target_node, {"grid_freq_hz": req.grid_freq_hz}
    )
    ledger.record_transaction("BFT_Consensus_Kernel", "STATE_PROPOSAL_VOTE", res)
    return {"success": True, "consensus": res}

@app.get("/api/v1/ledger")
def get_ledger_verification():
    is_valid, msg = ledger.verify_chain()
    return {"success": True, "is_valid": is_valid, "verification_summary": msg}

@app.post("/api/v1/ml/retrain")
def retrain_models():
    results = train_all_models()
    predictor.load_models()
    ledger.record_transaction("ML_Pipeline_Kernel", "KAGGLE_MODELS_RETRAINED", results)
    return {"success": True, "message": "All 4 Kaggle ML models retrained successfully!", "results": results}

# ────────────── STREAMLIT WEBSOCKET & REVERSE PROXY ──────────────
@app.websocket("/_stcore/stream")
@app.websocket("/_stcore/stream/{ws_path:path}")
async def websocket_proxy(websocket: WebSocket, ws_path: str = ""):
    await websocket.accept()
    target_url = f"{STREAMLIT_INTERNAL_WS}/_stcore/stream"
    if ws_path:
        target_url += f"/{ws_path}"

    try:
        async with websockets.connect(target_url) as target_ws:
            async def forward_to_streamlit():
                try:
                    while True:
                        msg = await websocket.receive_text()
                        await target_ws.send(msg)
                except Exception:
                    pass

            async def forward_to_client():
                try:
                    while True:
                        msg = await target_ws.recv()
                        await websocket.send_text(msg)
                except Exception:
                    pass

            await asyncio.gather(forward_to_streamlit(), forward_to_client())
    except Exception as e:
        print(f"⚠️ Streamlit WebSocket relay note: {e}")
    finally:
        try:
            await websocket.close()
        except Exception:
            pass

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def reverse_proxy_streamlit(request: Request, path: str):
    # Route matching protection for native FastAPI endpoints
    if path.startswith("api/") or path.startswith("docs") or path.startswith("openapi.json") or path == "health":
        raise HTTPException(status_code=404, detail="API endpoint not found")

    url = f"{STREAMLIT_INTERNAL_HTTP}/{path}"
    if request.query_params:
        url += f"?{request.query_params}"

    headers = dict(request.headers)
    headers.pop("host", None)

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            content = await request.body()
            resp = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=content
            )

            excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
            resp_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}

            return Response(
                content=resp.content,
                status_code=resp.status_code,
                headers=resp_headers
            )
    except Exception as e:
        return Response(
            content="<html><head><meta http-equiv='refresh' content='2'></head><body style='background:#0A0F1D;color:#00E5FF;font-family:sans-serif;text-align:center;padding-top:20%'><h2>⚡ EcoGrid Core Initializing...</h2><p>Connecting to Streamlit SCADA interface...</p></body></html>",
            status_code=200,
            media_type="text/html"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)
