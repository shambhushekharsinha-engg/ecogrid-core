import json
import os

class TerminalDashboard:
    """Renders an enterprise administrative status dashboard directly in the terminal interface."""

    @staticmethod
    def load_active_region_meta():
        config_path = os.path.join("config", "scenarios.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                active_region = data.get("global_settings", {}).get("active_region", "IN")
                matrix = data.get("regional_pricing_matrix", {})
                region_meta = matrix.get(active_region, {"currency": "INR", "symbol": "₹", "base_rate_per_kwh": 7.50})
                return active_region, region_meta
        except Exception:
            return "IN", {"currency": "INR", "symbol": "₹", "base_rate_per_kwh": 7.50}

    @classmethod
    def render(cls, iteration, total_nodes, weather, spot_rate, system_status="OPERATIONAL", saved_kwh=150.0):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        ledger_path = os.path.join("reports", "ledger.json")
        try:
            with open(ledger_path, "r", encoding="utf-8") as f:
                ledger_entries = len(json.load(f))
        except Exception:
            ledger_entries = 0

        region_code, region_meta = cls.load_active_region_meta()
        symbol = region_meta.get("symbol", "₹")
        base_rate = region_meta.get("base_rate_per_kwh", 7.50)
        estimated_mitigation = saved_kwh * base_rate

        print("█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
        print(f"█   AEGIS TRAFFIC & ECOGRID SCADA COCKPIT v6.0-PROD              █")
        print("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
        print(f"  [RUN STATE] {system_status}  |  [ITERATION] #{iteration}  |  [SECTORS] {total_nodes}/3")
        print(" ─────────────────────────────────────────────────────────────────")
        print(f"  🚦 [AEGIS TRAFFIC]    Intersection Mode: ADAPTIVE_ML_OPTIMIZED")
        print(f"  🌍 [ENVIRONMENT]      Sky: {weather['weather_condition']}  |  Solar Eff: {int(weather['solar_generation_efficiency']*100)}%")
        print(f"  💰 [MARKET RATE]      Spot Rate: {spot_rate} INR / MWh")
        print(f"  🌐 [SECTOR REGION]    Active Node: Region {region_code} ({region_meta['currency']})")
        print(f"  📊 [MITIGATION VALUE] Savings: {symbol}{estimated_mitigation:,.2f}")
        print(f"  🔐 [3/3 BFT LEDGER]   Sealed Blocks: {ledger_entries}")
        print(" ─────────────────────────────────────────────────────────────────")