import json
import time
import random
import os
from mcp_server import WeatherMcpServer
from dashboard_ui import TerminalDashboard

# Explicitly pointing to files inside your subfolders
from core.battery_system import BatteryBank
from core.mitigation_engine import GroundLevelMitigation
from security.crypto_ledger import CryptographicLedger
from security.chaos_monkey import ChaosMonkey

def load_json_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def get_interactive_scenario():
    """Allows the developer to rapidly map options via tap-numbers instead of typing words."""
    print("\n🎛️  [MANUAL QUICK-TAP MODE] Select Grid Parameters:")
    try:
        # 1. Market Rate Setup
        print("\n  [1/4] Select Spot Market Pricing Baseline:")
        print("    1) Low Operational Cost (1800 INR)")
        print("    2) Balanced Market Rate (3500 INR)")
        print("    3) High Volatility Peak  (5500 INR)")
        price_choice = input("  Tap Choice (1-3) [Default 2]: ")
        price_map = {"1": 1800, "2": 3500, "3": 5500}
        price = price_map.get(price_choice, 3500)

        # 2. Sky Profile Setup
        print("\n  [2/4] Select Weather Environment Profile:")
        print("    1) SUNNY  (Optimal Generation)")
        print("    2) CLOUDY (Moderate Generation)")
        print("    3) RAINY  (Low Generation)")
        print("    4) STORMY (Critical Danger)")
        weather_choice = input("  Tap Choice (1-4) [Default 1]: ")
        weather_map = {"1": ("SUNNY", 0.95), "2": ("CLOUDY", 0.45), "3": ("RAINY", 0.15), "4": ("STORMY", 0.05)}
        sky, eff = weather_map.get(weather_choice, ("SUNNY", 0.95))

        # 3. Cybersecurity Attack Allocation
        print("\n  [3/4] Inject Malicious Cyber-Threat Vector:")
        print("    1) Clear Stream (No Attacks Active)")
        print("    2) Isolate & Target Medical District (Node_Gamma_Medical)")
        print("    3) Isolate & Target Industrial Complex (Node_Beta_Industrial)")
        attack_choice = input("  Tap Choice (1-3) [Default 1]: ")
        
        attack_node = "None"
        if attack_choice == "2":
            attack_node = "Node_Gamma_Medical"
        elif attack_choice == "3":
            attack_node = "Node_Beta_Industrial"
            
        return [{
            "scenario_name": "User-Defined Live Injection Drill",
            "market_price_inr": price,
            "weather_condition": sky,
            "solar_efficiency": eff,
            "forced_attack_node": attack_node,
            "attack_type": "FREQUENCY_SPOOF" if attack_node != "None" else "NONE"
        }]
    except Exception:
        print("   ⚠️ Input tracking error. Reverting to automated profiles.")
        return None

def run_orchestrator():
    battery = BatteryBank()
    ledger = CryptographicLedger()
    chaos = ChaosMonkey()
    
    forecaster = load_json_file("agents/forecaster.json")
    arbitrageur = load_json_file("agents/arbitrageur.json")
    
    print("\n[EcoGrid Core Startup]")
    print("  1. Run Pre-configured Scenarios File")
    print("  2. Inject Custom Live Grid Scenario via Quick-Tap Menu")
    choice = input("Select Execution Mode (1 or 2): ")
    
    if choice == "2":
        scenarios = get_interactive_scenario() or load_json_file("scenarios.json")
    else:
        scenarios = load_json_file("scenarios.json")
        
    frequency_history = []

    try:
        for idx, scenario in enumerate(scenarios, start=1):
            print(f"\n[Processing Engine Sequence] Loading data matrix...")
            time.sleep(1.0)
            
            price = scenario["market_price_inr"]
            weather = {
                "weather_condition": scenario["weather_condition"],
                "solar_generation_efficiency": scenario["solar_efficiency"]
            }
            
            nodes = {
                "Node_Alpha_Residential": {"demand_kw": random.randint(100, 250), "grid_freq_hz": round(random.uniform(49.8, 50.2), 2), "priority_level": 3},
                "Node_Beta_Industrial": {"demand_kw": random.randint(400, 800), "grid_freq_hz": round(random.uniform(49.7, 50.3), 2), "priority_level": 2},
                "Node_Gamma_Medical": {"demand_kw": random.randint(200, 350), "grid_freq_hz": round(random.uniform(49.8, 50.2), 2), "priority_level": 1}
            }
            
            if scenario["forced_attack_node"] in nodes:
                target = scenario["forced_attack_node"]
                if scenario["attack_type"] == "FREQUENCY_SPOOF":
                    nodes[target]["grid_freq_hz"] = 53.10
            
            TerminalDashboard.render(iteration=idx, total_nodes=3, weather=weather, spot_rate=price)
            print(f"  🎬 ACTIVE RUNTIME SCENARIO: {scenario['scenario_name']}")
            print("  [LIVE LOG ANALYSIS TRACE]")
            
            for node_name, node_telemetry in nodes.items():
                incident_report = chaos.inject_adversarial_fault(node_telemetry) if scenario["forced_attack_node"] == "None" else {"is_attack_active": node_telemetry["grid_freq_hz"] > 51.0, "attack_type": "Deterministic Injection Attack", "data": node_telemetry}
                active_telemetry = incident_report["data"]
                
                if incident_report["is_attack_active"]:
                    print(f"    💥 ALERT: Malicious telemetry spoofing caught on {node_name}!")
                    ledger.record_transaction("SECURITY_IDS_KERNEL", "CYBER_ATTACK_CONTAINMENT", {"targeted_node": node_name, "vector": incident_report["attack_type"]})
                    protocols = GroundLevelMitigation.get_prescription(incident_report["attack_type"], active_telemetry["grid_freq_hz"], node_name)
                    for step in protocols:
                        print(f"      {step}")
                    continue
                
                freq = active_telemetry["grid_freq_hz"]
                load = active_telemetry["demand_kw"]
                priority = active_telemetry["priority_level"]
                
                frequency_history.append(freq)
                if len(frequency_history) > 3:
                    frequency_history.pop(0)
                
                if len(frequency_history) >= 2:
                    drift_delta = round(frequency_history[-1] - frequency_history[-2], 2)
                    if abs(drift_delta) >= 0.3:
                        print(f"    🔮 PREDICTIVE FORECAST: {forecaster['agent_name']} flagged a critical instability trend drift ({drift_delta} Hz/s) on {node_name}!")
                
                print(f"    [Clear Stream] Metrics -> Load: {load}kW | Freq: {freq}Hz")
                
                # Step 1: Forecaster Diagnostics Check
                if freq < 49.5 or freq > 50.5:
                    if priority == 1:
                        print(f"    🚨 EMERGENCY: Hospital Anomaly! Injecting backup reserves!")
                        ledger.record_transaction(forecaster["agent_name"], "EMERGENCY_RESERVE_INJECTION", {"node": node_name})
                        continue
                    else:
                        TerminalDashboard.render(iteration=idx, total_nodes=2, weather=weather, spot_rate=price, system_status="CRITICAL_HALT")
                        print(f"    🚨 HALT: Unsafe frequency ({freq} Hz) on non-critical sector {node_name}.")
                        protocols = GroundLevelMitigation.get_prescription("Frequency_Anomaly", freq, node_name)
                        for step in protocols:
                            print(f"      {step}")
                        return
                
                # Step 2: Arbitrageur Balancing Decisions
                if weather["solar_generation_efficiency"] < 0.5 and price > 4000:
                    print(f"    ⚠️ PIVOT: Microgrid routing to battery cells active for {node_name}.")
                    batt_state = battery.discharge_for_arbitrage(load)
                    ledger.record_transaction(arbitrageur["agent_name"], "BATTERY_ROUTING_PIVOT", {"node": node_name, "remaining_soc": batt_state["current_soc"]})
                else:
                    if price > 5000:
                        TerminalDashboard.render(iteration=idx, total_nodes=2, weather=weather, spot_rate=price, system_status="BUDGET_HALT")
                        print(f"    🚨 HALT: Cost Overrun ({price} INR) on {node_name}.")
                        protocols = GroundLevelMitigation.get_prescription("Budget_Overrun", price, node_name)
                        for step in protocols:
                            print(f"      {step}")
                        return
                    else:
                        print(f"    ✅ SUCCESS: Data clear. Routed to standard market line for {node_name}.")
                        ledger.record_transaction(arbitrageur["agent_name"], "GRID_CLEARANCE_APPROVAL", {"node": node_name})
                        
            print("\n  " + "="*60 + "\n  Scan complete. Simulation run finished.")
            
    except KeyboardInterrupt:
        print("\nOrchestrator securely brought down by developer.")

if __name__ == "__main__":
    run_orchestrator()