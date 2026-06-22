class BatteryBank:
    """Manages stateful tracking of battery capacity and chemical health degradation."""
    
    def __init__(self):
        self.state_of_charge = 85.0  # Percentage starting point
        self.battery_health = 100.0   # Percentage health starting point

    def discharge_for_arbitrage(self, load_kw):
        # Every time the agent relies on the battery, charge drops and health degrades slightly
        self.state_of_charge -= (load_kw / 1000) * 5
        self.battery_health -= 0.05  # Micro-degradation factor
        
        # Keep values bound smoothly
        self.state_of_charge = max(0.0, round(self.state_of_charge, 2))
        self.battery_health = max(0.0, round(self.battery_health, 2))
        
        return {
            "current_soc": self.state_of_charge,
            "remaining_health": self.battery_health
        }