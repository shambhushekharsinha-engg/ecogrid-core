"""
Aegis & EcoGrid ML Predictor & Live Inference Engine
Loads trained Kaggle models from models/ directory for real-time predictions.
"""

import os
import joblib
import pandas as pd
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

class MLPredictor:
    """Provides high-performance live inference across Aegis Traffic and EcoGrid SCADA."""

    def __init__(self):
        self.models = {}
        self.load_models()

    def load_models(self):
        """Loads all serialized .joblib model artifacts."""
        model_files = {
            "traffic": "traffic_congestion_model.joblib",
            "grid_load": "grid_load_model.joblib",
            "solar": "solar_generation_model.joblib",
            "anomaly": "anomaly_detector_model.joblib"
        }
        for key, fname in model_files.items():
            path = os.path.join(MODEL_DIR, fname)
            if os.path.exists(path):
                try:
                    self.models[key] = joblib.load(path)
                except Exception as e:
                    print(f"⚠️ Error loading model {fname}: {e}")

    def predict_traffic_congestion(self, vehicle_count: int, avg_speed: float, weather: str = "SUNNY", hour: int = 14, is_peak: int = 0) -> float:
        """Predicts urban Intersection Congestion Index (0.0 to 1.0)."""
        if "traffic" in self.models:
            weather_map = {"SUNNY": 0, "CLOUDY": 1, "RAINY": 2, "STORMY": 3}
            w_code = weather_map.get(weather.upper(), 0)
            df = pd.DataFrame([{
                'vehicle_count_per_hr': vehicle_count,
                'avg_speed_kmh': avg_speed,
                'weather_code': w_code,
                'hour': hour,
                'is_peak_hour': is_peak
            }])
            pred = float(self.models["traffic"].predict(df)[0])
            return max(0.0, min(1.0, round(pred, 3)))
        else:
            # Heuristic calculation
            return max(0.0, min(1.0, round(vehicle_count / 1400.0, 3)))

    def predict_grid_load(self, temp_c: float, humidity_pct: float, ev_kw: float, hour: int = 15, is_peak_price: int = 1) -> float:
        """Predicts total grid energy load in kW."""
        if "grid_load" in self.models:
            df = pd.DataFrame([{
                'ambient_temp_c': temp_c,
                'humidity_pct': humidity_pct,
                'ev_station_kw': ev_kw,
                'hour': hour,
                'is_peak_pricing': is_peak_price
            }])
            pred = float(self.models["grid_load"].predict(df)[0])
            return max(100.0, round(pred, 2))
        else:
            return round(800.0 + (temp_c * 20.0) + (ev_kw * 0.8), 2)

    def predict_solar_generation(self, irradiance: float, panel_temp: float, cloud_cover: float, hour: int = 12) -> float:
        """Predicts solar generation in kW."""
        if "solar" in self.models:
            df = pd.DataFrame([{
                'irradiance_wm2': irradiance,
                'panel_temp_c': panel_temp,
                'cloud_cover_pct': cloud_cover,
                'hour': hour
            }])
            pred = float(self.models["solar"].predict(df)[0])
            return max(0.0, round(pred, 2))
        else:
            return max(0.0, round((irradiance * 0.9) * (1.0 - cloud_cover / 100.0), 2))

    def detect_cyber_anomaly(self, frequency_hz: float, total_load_kw: float, ev_kw: float = 300, hour: int = 12) -> dict:
        """Classifies telemetry streams for cyber-attack or frequency spoofing anomalies."""
        is_attack = False
        confidence = 0.95

        if "anomaly" in self.models:
            df = pd.DataFrame([{
                'grid_frequency_hz': frequency_hz,
                'total_load_kw': total_load_kw,
                'ev_station_kw': ev_kw,
                'hour': hour
            }])
            pred = int(self.models["anomaly"].predict(df)[0])
            is_attack = (pred == 1) or (frequency_hz < 49.2 or frequency_hz > 50.8)
        else:
            is_attack = (frequency_hz < 49.2 or frequency_hz > 50.8)

        return {
            "is_attack_detected": is_attack,
            "anomaly_type": "FREQUENCY_SPOOFING_INJECTION" if is_attack else "NOMINAL_TELEMETRY",
            "confidence_score": confidence,
            "monitored_frequency_hz": frequency_hz
        }

predictor = MLPredictor()
