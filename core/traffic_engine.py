"""
Aegis Traffic Engine: Intelligent Urban Traffic & Intersection Control Infrastructure
Handles Signal Phase Duration Optimization, Emergency Corridor Overrides,
Intersection Congestion Index (ICI), and EV Charging Queue Load Balancing.
"""

from ml_engine.predictor import predictor

class AegisTrafficEngine:
    """Core domain engine for Aegis AI Intelligent Urban Traffic Control."""

    @staticmethod
    def calculate_intersection_metrics(vehicle_count: int, avg_speed_kmh: float, weather: str = "SUNNY", hour: int = 14) -> dict:
        """Calculates real-time Intersection Congestion Index (ICI) using ML prediction."""
        is_peak = 1 if (7 <= hour <= 9 or 16 <= hour <= 19) else 0
        predicted_ci = predictor.predict_traffic_congestion(
            vehicle_count=vehicle_count,
            avg_speed=avg_speed_kmh,
            weather=weather,
            hour=hour,
            is_peak=is_peak
        )

        if predicted_ci >= 0.85:
            level = "CRITICAL_CONGESTION"
            color = "#FF3333"
        elif predicted_ci >= 0.60:
            level = "MODERATE_TRAFFIC"
            color = "#FFB300"
        else:
            level = "OPTIMAL_FLOW"
            color = "#00FF66"

        return {
            "congestion_index": predicted_ci,
            "traffic_status_level": level,
            "status_color": color,
            "is_peak_hour": bool(is_peak),
            "vehicle_count_per_hr": vehicle_count,
            "avg_speed_kmh": avg_speed_kmh
        }

    @staticmethod
    def optimize_signal_timing(intersection_id: str, vehicle_count: int, cross_street_count: int = 250, emergency_flag: bool = False) -> dict:
        """Dynamically computes optimal green light duration (sec) for main vs cross street."""
        if emergency_flag:
            return {
                "intersection_id": intersection_id,
                "mode": "EMERGENCY_GREEN_CORRIDOR",
                "main_street_green_sec": 120,
                "cross_street_green_sec": 10,
                "yellow_phase_sec": 3,
                "pedestrian_walk_sec": 5,
                "action_summary": f"🚨 EMERGENCY PRIORITY CORRIDOR OVERRIDE ACTIVATED FOR {intersection_id}!"
            }

        total_vehicles = vehicle_count + cross_street_count
        ratio = vehicle_count / max(1, total_vehicles)
        cycle_length_sec = 120 if vehicle_count > 800 else 90

        main_green = int(max(20, min(90, round(cycle_length_sec * ratio))))
        cross_green = cycle_length_sec - main_green - 6  # 6s yellow/red clearance

        return {
            "intersection_id": intersection_id,
            "mode": "ADAPTIVE_ML_OPTIMIZED",
            "main_street_green_sec": main_green,
            "cross_street_green_sec": cross_green,
            "yellow_phase_sec": 3,
            "pedestrian_walk_sec": 15,
            "action_summary": f"🚦 Optimized timing: Main {main_green}s | Cross {cross_green}s (Cycle: {cycle_length_sec}s)"
        }

    @staticmethod
    def balance_ev_charging_queue(grid_load_kw: float, max_capacity_kw: float = 2000.0, queued_evs: int = 15) -> dict:
        """Dynamically adjusts EV charging station output per plug to protect grid stability."""
        available_margin_kw = max(0.0, max_capacity_kw - grid_load_kw)

        if available_margin_kw < 200.0:
            power_per_plug_kw = 15.0  # Eco slow charge mode
            mode = "SHEDDING_PROTECTION"
        elif available_margin_kw < 600.0:
            power_per_plug_kw = 50.0  # Standard fast charge
            mode = "BALANCED_LOAD"
        else:
            power_per_plug_kw = 150.0 # Ultra-fast charge
            mode = "MAXIMUM_DISPATCH"

        total_station_draw_kw = min(available_margin_kw, power_per_plug_kw * queued_evs)

        return {
            "charging_mode": mode,
            "power_per_plug_kw": power_per_plug_kw,
            "active_ev_chargers": queued_evs,
            "allocated_station_kw": round(total_station_draw_kw, 2),
            "remaining_grid_margin_kw": round(available_margin_kw, 2)
        }
