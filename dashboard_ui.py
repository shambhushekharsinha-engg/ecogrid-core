import json
import os

class TerminalDashboard:
    """Renders an enterprise administrative status dashboard directly in the terminal interface."""

    @staticmethod
    def render(iteration, total_nodes, weather, spot_rate, system_status="OPERATIONAL"):
        # Clear terminal screen dynamically based on OS
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Read cryptographic audit ledger length
        try:
            with open("ledger.json", "r") as f:
                ledger_entries = len(json.load(f))
        except:
            ledger_entries = 0

        print("█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
        print(f"█   ECOGRID AI INFRASTRUCTURE SYSTEMS MANAGEMENT PANEL v5.5-UI  █")
        print("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
        print(f"  [RUN STATE] {system_status}  |  [ITERATION LOG] #{iteration}  |  [ONLINE SECTORS] {total_nodes}/3")
        print(" ─────────────────────────────────────────────────────────────────")
        print(f"  🌍 [ENVIRONMENT DATA]  Sky Profile: {weather['weather_condition']}  |  Solar Efficiency: {int(weather['solar_generation_efficiency']*100)}%")
        print(f"  💰 [ENERGY MARKET]     Spot Pricing Rate: {spot_rate} INR / MWh")
        print(f"  🔐 [CRYPTO AUDITING]   Total Sealed Ledger Transactions: {ledger_entries}")
        print(" ─────────────────────────────────────────────────────────────────")