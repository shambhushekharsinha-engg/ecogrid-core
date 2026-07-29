"""
Automated Test Suite for Aegis Traffic & EcoGrid Core Platform
Tests Authentication, Traffic Engine, Kaggle ML Models, BFT Consensus,
Multi-Currency Switcher, AI Copilot Q&A, Crypto Ledger Chaining, and REST Endpoints.
"""

import os
import pytest
from fastapi.testclient import TestClient

from security.auth import auth_manager
from core.traffic_engine import AegisTrafficEngine
from core.consensus_engine import BFTConsensusEngine
from core.mitigation_engine import GroundLevelMitigation
from security.crypto_ledger import CryptographicLedger
from ml_engine.train_models import train_all_models
from ml_engine.predictor import predictor
from cloud_auditor import auditor
from api.server import app

client = TestClient(app)

# ────────────── 1. SECURITY & AUTHENTICATION TESTS ──────────────
def test_password_validation():
    valid, msg = auth_manager.validate_password_strength("Weak")
    assert not valid
    valid_strong, _ = auth_manager.validate_password_strength("StrongPass@123")
    assert valid_strong

def test_user_registration_and_login():
    test_user = "test_operator_99"
    test_pass = "SecurePass@99"
    ok, msg = auth_manager.register_user(test_user, test_pass, "Operator")
    assert ok or "already taken" in msg

    auth_ok, res = auth_manager.authenticate_user(test_user, test_pass)
    assert auth_ok
    assert res["username"] == test_user

def test_demo_login_presets():
    for role_key in ["admin", "traffic_op", "grid_eng", "guest"]:
        meta = auth_manager.DEMO_USERS[role_key]
        ok, res = auth_manager.authenticate_user(role_key, meta["password"])
        assert ok
        assert "username" in res

# ────────────── 2. AEGIS TRAFFIC ENGINE TESTS ──────────────
def test_intersection_congestion_index():
    metrics = AegisTrafficEngine.calculate_intersection_metrics(950, 22.5, "SUNNY")
    assert 0.0 <= metrics["congestion_index"] <= 1.0
    assert metrics["traffic_status_level"] in ["OPTIMAL_FLOW", "MODERATE_TRAFFIC", "CRITICAL_CONGESTION"]

def test_adaptive_signal_timing_optimization():
    plan = AegisTrafficEngine.optimize_signal_timing("INT_ALPHA_CBD", 950, 300, emergency_flag=False)
    assert plan["mode"] == "ADAPTIVE_ML_OPTIMIZED"
    assert plan["main_street_green_sec"] > 0
    assert plan["cross_street_green_sec"] > 0

def test_emergency_green_corridor_override():
    em_plan = AegisTrafficEngine.optimize_signal_timing("INT_ALPHA_CBD", 950, 300, emergency_flag=True)
    assert em_plan["mode"] == "EMERGENCY_GREEN_CORRIDOR"
    assert em_plan["main_street_green_sec"] == 120

def test_ev_charging_queue_balancing():
    res = AegisTrafficEngine.balance_ev_charging_queue(1850.0, 2000.0, 15)
    assert res["charging_mode"] == "SHEDDING_PROTECTION"
    assert res["power_per_plug_kw"] == 15.0

# ────────────── 3. MULTI-CURRENCY & AI COPILOT TESTS ──────────────
def test_multi_country_currency_switcher():
    for code in ["IN", "US", "EU", "UK", "JP", "AU", "BR", "CA", "UAE", "ZA"]:
        val, formatted = GroundLevelMitigation.convert_price_from_inr(3500.0, code)
        assert val > 0.0
        assert len(formatted) > 0

    mit = GroundLevelMitigation.calculate_regional_mitigation(150.0, "US")
    assert mit["currency_code"] == "USD"
    assert mit["currency_symbol"] == "$"

def test_ai_copilot_answers_and_summary():
    res = auditor.answer_user_query("How does Aegis Traffic optimize signal timing during peak hours?")
    assert "summary" in res
    assert "full_response" in res
    assert len(res["summary"]) > 0

# ────────────── 4. KAGGLE ML ENGINE TESTS ──────────────
def test_kaggle_model_training_and_inference():
    res = train_all_models()
    assert "traffic_model" in res
    assert "grid_load_model" in res
    assert "solar_model" in res
    assert "anomaly_model" in res

    predictor.load_models()
    ci = predictor.predict_traffic_congestion(800, 30.0)
    assert 0.0 <= ci <= 1.0

    load = predictor.predict_grid_load(30.0, 50.0, 400.0)
    assert load > 0.0

# ────────────── 5. BFT CONSENSUS & LEDGER TESTS ──────────────
def test_bft_consensus_verification():
    bft_ok = BFTConsensusEngine.evaluate_state_proposal("GRID_LOAD_TRANSFER", "Node_Alpha_Residential", {"grid_freq_hz": 50.0})
    assert bft_ok["is_consensus_reached"]

    bft_reject = BFTConsensusEngine.evaluate_state_proposal("GRID_LOAD_TRANSFER", "Node_Alpha_Residential", {"grid_freq_hz": 53.5})
    assert not bft_reject["is_consensus_reached"]

def test_crypto_ledger_verifiable_chain():
    ledger = CryptographicLedger()
    h = ledger.record_transaction("TEST_AGENT", "UNIT_TEST_ACTION", {"status": "SUCCESS"})
    assert len(h) == 64
    valid, msg = ledger.verify_chain()
    assert valid

# ────────────── 6. FASTAPI REST ENDPOINTS TESTS ──────────────
def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ONLINE"

def test_api_traffic_prediction_endpoint():
    response = client.post("/api/v1/predict/traffic", json={
        "vehicle_count": 950,
        "avg_speed_kmh": 22.5,
        "weather": "SUNNY",
        "hour": 17
    })
    assert response.status_code == 200
    assert response.json()["success"]

def test_api_ai_copilot_endpoint():
    response = client.post("/api/v1/ai/copilot", json={
        "user_query": "Explain frequency spoofing containment.",
        "context_data": {}
    })
    assert response.status_code == 200
    assert "summary" in response.json()["data"]

def test_api_currency_convert_endpoint():
    response = client.post("/api/v1/currency/convert", json={
        "price_inr": 3500.0,
        "target_country_code": "US"
    })
    assert response.status_code == 200
    assert response.json()["target_country"] == "US"
