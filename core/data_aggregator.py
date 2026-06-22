import json
import random
import math

class DataAggregator:
    """Enterprise Data Ingestion Engine tracking real-time external stream parameters and CSV matrices."""

    @staticmethod
    def simulate_live_api_fetch(sky_profile):
        """Simulates an external live API endpoint fetch with dynamic sine-wave volatility adjustments."""
        base_efficiency = {"SUNNY": 0.95, "CLOUDY": 0.45, "RAINY": 0.15, "STORMY": 0.05}
        eff = base_efficiency.get(sky_profile, 0.50)
        
        # Inject natural stochastic drift (sensor noise)
        drift = round(random.uniform(-0.03, 0.03), 2)
        final_eff = max(0.0, min(1.0, eff + drift))
        
        # Synthesize real-time fluctuating load profiles based on standard municipal curves
        residential_load = int(180 + 50 * math.sin(random.uniform(0, 2 * math.pi)))
        industrial_load = int(600 + 150 * math.cos(random.uniform(0, 2 * math.pi)))
        medical_load = int(280 + 30 * math.sin(random.uniform(0, 2 * math.pi)))
        
        return {
            "source": "Live Simulated Stream (MCP Aggregator Feed)",
            "solar_efficiency": final_eff,
            "nodes": {
                "Node_Alpha_Residential": {"demand_kw": residential_load, "grid_freq_hz": round(random.uniform(49.85, 50.15), 2)},
                "Node_Beta_Industrial": {"demand_kw": industrial_load, "grid_freq_hz": round(random.uniform(49.75, 50.25), 2)},
                "Node_Gamma_Medical": {"demand_kw": medical_load, "grid_freq_hz": round(random.uniform(49.92, 50.08), 2)}
            }
        }

    @staticmethod
    def parse_uploaded_csv(file_contents):
        """Parses custom external industrial CSV uploads for time-series digital twin playback."""
        parsed_records = []
        try:
            lines = file_contents.decode("utf-8").split("\n")
            # Expected Header: timestamp,node_name,demand_kw,grid_freq_hz
            for line in lines[1:]: # Skip header
                if not line.strip():
                    continue
                parts = line.split(",")
                if len(parts) >= 4:
                    parsed_records.append({
                        "timestamp": parts[0].strip(),
                        "node_name": parts[1].strip(),
                        "demand_kw": int(parts[2].strip()),
                        "grid_freq_hz": float(parts[3].strip())
                    })
            return parsed_records
        except Exception:
            return None