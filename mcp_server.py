import random

class WeatherMcpServer:
    """Emulates a canonical Model Context Protocol (MCP) server for environmental telemetry."""
    
    def __init__(self):
        self.conditions = ["SUNNY", "CLOUDY", "RAINY", "STORMY"]

    def fetch_live_weather(self):
        # Emulating a structured read-only tool response
        current_sky = random.choice(self.conditions)
        
        # Solar generation efficiency drops based on weather context
        if current_sky == "SUNNY":
            solar_efficiency = 1.0
        elif current_sky == "CLOUDY":
            solar_efficiency = 0.4
        else:
            solar_efficiency = 0.1  # Rain/Storm heavily limits solar output
            
        return {
            "mcp_status": "CONNECTED",
            "weather_condition": current_sky,
            "solar_generation_efficiency": solar_efficiency
        }

# Quick validation check when run directly
if __name__ == "__main__":
    server = WeatherMcpServer()
    print("Testing MCP Protocol Output:", server.fetch_live_weather())