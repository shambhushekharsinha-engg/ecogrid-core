import random

class ChaosMonkey:
    """Simulates adversarial security anomalies and data-tampering attacks on microgrid infrastructure."""
    
    def __init__(self):
        # 0.0 = No attack, 1.0 = Constant attack. We set it to 30% chance.
        self.attack_probability = 0.3 

    def inject_adversarial_fault(self, real_node_telemetry):
        """Randomly alters telemetry data streams to mimic malicious cyberattacks."""
        tampered = False
        attack_type = "NONE"
        
        if random.random() < self.attack_probability:
            tampered = True
            choice = random.choice(["FREQUENCY_SPOOF", "DEMAND_SPIKE_INJECTION"])
            
            if choice == "FREQUENCY_SPOOF":
                attack_type = "Adversarial Frequency Spoofing (Man-in-the-Middle)"
                # Artificially inject a destructive frequency surge
                real_node_telemetry["grid_freq_hz"] = round(random.uniform(51.5, 53.0), 2)
            
            elif choice == "DEMAND_SPIKE_INJECTION":
                attack_type = "Malicious Phantom Load Inflation (DDoS Mock)"
                # Overinflate demand to force massive financial drainage
                real_node_telemetry["demand_kw"] = random.randint(2500, 4000)
                
        return {
            "is_attack_active": tampered,
            "attack_type": attack_type,
            "data": real_node_telemetry
        }