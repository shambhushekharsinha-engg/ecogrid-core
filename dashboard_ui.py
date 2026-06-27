import json
import os

class TerminalDashboard:
    """Renders an enterprise administrative status dashboard directly in the terminal interface."""

    @staticmethod
    def load_active_region_meta():
        """Safely extracts global active settings and pricing criteria from scenarios configuration."""
        config_path = os.path.join("config", "scenarios.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                active_region = data.get("global_settings", {}).get("active_region", "IN")
                matrix = data.get("regional_pricing_matrix", {})
                region_meta = matrix.get(active_region, {"currency": "INR", "symbol": "₹", "base_rate_per_kwh": 7.50})
                return active_region, region_meta
        except Exception:
            # Sturdy fallback if the nested config structure isn't resolved yet
            return "IN", {"currency": "INR", "symbol": "₹", "base_rate_per_kwh": 7.50}

    @classmethod
    def render(cls, iteration, total_nodes, weather, spot_rate, system_status="OPERATIONAL", saved_kwh=150.0):
        # Clear terminal screen dynamically based on OS
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Read cryptographic audit ledger length from reports/ledger.json path
        ledger_path = os.path.join("reports", "ledger.json")
        try:
            with open(ledger_path, "r", encoding="utf-8") as f:
                ledger_entries = len(json.load(f))
        except Exception:
            ledger_entries = 0

        # Load international currency properties dynamically
        region_code, region_meta = cls.load_active_region_meta()
        symbol = region_meta.get("symbol", "₹")
        base_rate = region_meta.get("base_rate_per_kwh", 7.50)

        # Calculate mitigation savings based on active global tariff parameters
        estimated_mitigation = saved_kwh * base_rate

        print("█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
        print(f"█   ECOGRID AI INFRASTRUCTURE SYSTEMS MANAGEMENT PANEL v5.5-UI   █")
        print("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
        print(f"  [RUN STATE] {system_status}  |  [ITERATION LOG] #{iteration}  |  [ONLINE SECTORS] {total_nodes}/3")
        print(" ─────────────────────────────────────────────────────────────────")
        print(f"  🌍 [ENVIRONMENT DATA]  Sky Profile: {weather['weather_condition']}  |  Solar Efficiency: {int(weather['solar_generation_efficiency']*100)}%")
        print(f"  💰 [ENERGY MARKET]     Spot Pricing Rate: {spot_rate} INR / MWh")
        print(f"  🌐 [GLOBAL BOUNDARY]   Active Node: Region {region_code} ({region_meta['currency']})")
        print(f"  📊 [MITIGATION VALUE]  Estimated Savings: {symbol}{estimated_mitigation:,.2f}")
        print(f"  🔐 [CRYPTO AUDITING]   Total Sealed Ledger Transactions: {ledger_entries}")
        print(" ─────────────────────────────────────────────────────────────────")