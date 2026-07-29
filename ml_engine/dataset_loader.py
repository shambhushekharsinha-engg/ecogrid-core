"""
Kaggle Dataset Loader for Aegis Traffic & EcoGrid SCADA ML Engine
Loads and pre-processes time-series Kaggle CSV datasets.
"""

import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

class DatasetLoader:
    """Manages ingestion of Kaggle datasets for ML training and evaluation."""

    @staticmethod
    def load_traffic_dataset() -> pd.DataFrame:
        path = os.path.join(DATA_DIR, "kaggle_traffic_flow.csv")
        df = pd.read_csv(path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        weather_map = {"SUNNY": 0, "CLOUDY": 1, "RAINY": 2, "STORMY": 3}
        df['weather_code'] = df['weather_condition'].map(lambda x: weather_map.get(str(x).upper(), 0))
        return df

    @staticmethod
    def load_grid_load_dataset() -> pd.DataFrame:
        path = os.path.join(DATA_DIR, "kaggle_grid_load.csv")
        df = pd.read_csv(path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        return df

    @staticmethod
    def load_solar_dataset() -> pd.DataFrame:
        path = os.path.join(DATA_DIR, "kaggle_solar_generation.csv")
        df = pd.read_csv(path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        return df
