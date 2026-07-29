"""
Automated ML Model Training Pipeline for EcoGrid Core Infrastructure
Trains models on Kaggle datasets using Scikit-Learn and serializes artifacts to models/
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np

# Ensure project root is present in sys.path for direct execution and Docker builds
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, f1_score
from ml_engine.dataset_loader import DatasetLoader

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

def train_all_models() -> dict:
    """Trains 4 ML models on Kaggle datasets and saves serialized .joblib files."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    results = {}

    print("[ML PIPELINE] Initializing Kaggle Dataset Training...")

    # 1. Traffic Congestion Predictor (RandomForestRegressor)
    df_traffic = DatasetLoader.load_traffic_dataset()
    X_tr = df_traffic[['vehicle_count_per_hr', 'avg_speed_kmh', 'weather_code', 'hour', 'is_peak_hour']]
    y_tr = df_traffic['congestion_index']

    tr_model = RandomForestRegressor(n_estimators=100, random_state=42)
    tr_model.fit(X_tr, y_tr)
    y_pred_tr = tr_model.predict(X_tr)
    r2_tr = r2_score(y_tr, y_pred_tr)
    rmse_tr = float(np.sqrt(mean_squared_error(y_tr, y_pred_tr)))

    tr_path = os.path.join(MODEL_DIR, "traffic_congestion_model.joblib")
    joblib.dump(tr_model, tr_path)
    results["traffic_model"] = {"r2_score": round(r2_tr, 4), "rmse": round(rmse_tr, 4), "path": tr_path}
    print(f"  Traffic Model Trained: R2 = {r2_tr:.4f}, RMSE = {rmse_tr:.4f}")

    # 2. Grid Load Predictor (GradientBoostingRegressor)
    df_grid = DatasetLoader.load_grid_load_dataset()
    X_grid = df_grid[['ambient_temp_c', 'humidity_pct', 'ev_station_kw', 'hour', 'is_peak_pricing']]
    y_grid = df_grid['total_load_kw']

    grid_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    grid_model.fit(X_grid, y_grid)
    y_pred_grid = grid_model.predict(X_grid)
    r2_grid = r2_score(y_grid, y_pred_grid)
    rmse_grid = float(np.sqrt(mean_squared_error(y_grid, y_pred_grid)))

    grid_path = os.path.join(MODEL_DIR, "grid_load_model.joblib")
    joblib.dump(grid_model, grid_path)
    results["grid_load_model"] = {"r2_score": round(r2_grid, 4), "rmse": round(rmse_grid, 4), "path": grid_path}
    print(f"  Grid Load Model Trained: R2 = {r2_grid:.4f}, RMSE = {rmse_grid:.4f}")

    # 3. Solar Generation Predictor (RandomForestRegressor)
    df_solar = DatasetLoader.load_solar_dataset()
    X_sol = df_solar[['irradiance_wm2', 'panel_temp_c', 'cloud_cover_pct', 'hour']]
    y_sol = df_solar['generation_kw']

    solar_model = RandomForestRegressor(n_estimators=100, random_state=42)
    solar_model.fit(X_sol, y_sol)
    y_pred_sol = solar_model.predict(X_sol)
    r2_sol = r2_score(y_sol, y_pred_sol)
    rmse_sol = float(np.sqrt(mean_squared_error(y_sol, y_pred_sol)))

    solar_path = os.path.join(MODEL_DIR, "solar_generation_model.joblib")
    joblib.dump(solar_model, solar_path)
    results["solar_model"] = {"r2_score": round(r2_sol, 4), "rmse": round(rmse_sol, 4), "path": solar_path}
    print(f"  Solar Generation Model Trained: R2 = {r2_sol:.4f}, RMSE = {rmse_sol:.4f}")

    # 4. Cyber Anomaly & Threat Classifier (RandomForestClassifier)
    X_anom = df_grid[['grid_frequency_hz', 'total_load_kw', 'ev_station_kw', 'hour']]
    y_anom = df_grid['is_cyber_attack']

    anom_model = RandomForestClassifier(n_estimators=50, random_state=42)
    anom_model.fit(X_anom, y_anom)
    y_pred_anom = anom_model.predict(X_anom)
    acc_anom = accuracy_score(y_anom, y_pred_anom)
    f1_anom = f1_score(y_anom, y_pred_anom, zero_division=1)

    anom_path = os.path.join(MODEL_DIR, "anomaly_detector_model.joblib")
    joblib.dump(anom_model, anom_path)
    results["anomaly_model"] = {"accuracy": round(acc_anom, 4), "f1_score": round(f1_anom, 4), "path": anom_path}
    print(f"  Cyber Anomaly Model Trained: Accuracy = {acc_anom:.4f}, F1-Score = {f1_anom:.4f}")

    print("[ML PIPELINE] All 4 Kaggle models successfully trained and serialized to models/\n")
    return results

if __name__ == "__main__":
    train_all_models()
