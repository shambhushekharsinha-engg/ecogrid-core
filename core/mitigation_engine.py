class GroundLevelMitigation:
    """Generates ground-level actionable engineering protocols for on-site microgrid technicians."""

    @staticmethod
    def get_prescription(reason_code, current_value, targeted_node):
        print(f"\n  🛠️ [GROUND-LEVEL MITIGATION PROTOCOL GENERATED FOR {targeted_node.upper()}]")
        print("  " + "─" * 65)
        
        if "Frequency" in reason_code or "SPOOF" in reason_code:
            return [
                "1. [FIELD ACTION] Deploy field technician to substation box to check physical inverter synchronization.",
                "2. [ISOLATION] Isolate sub-station breaker line from primary high-voltage feed to prevent circuit burn.",
                "3. [FIRMWARE] Flush local RTU (Remote Terminal Unit) cache and verify cryptographic handshake with central mesh core.",
                "4. [HARDWARE] Manually verify phase angles using a handheld calibrated oscilloscope."
            ]
        elif "Budget" in reason_code or "Load" in reason_code or "SPIKE" in reason_code:
            return [
                "1. [FIELD ACTION] Initiate immediate demand-side load shedding on secondary non-critical lines.",
                "2. [HARDWARE] Inspect local step-down transformers for high thermal signatures due to current over-saturation.",
                "3. [ROUTING] Route storage inverter arrays to output parallel discharge currents matching local transformer baselines.",
                "4. [COMMUNICATION] Broadcast local grid curtailment requests to high-draw consumer automation relays."
            ]
        else:
            return [
                "1. [FIELD ACTION] Perform general physical sweep of localized sub-array junctions.",
                "2. [SYSTEM] Force manual hard-reset of telemetry ingestion kernel."
            ]
        
    @staticmethod
    def calculate_regional_mitigation(saved_kwh, region_code="IN"):
        """Calculates dynamic operational mitigation costs across international grid parameters."""
        # Real-world currency symbols paired with average country tariff metrics
        matrix = {
            "US": ("$", 0.18), "EU": ("€", 0.24), "IN": ("₹", 7.50), 
            "UK": ("£", 0.35), "JP": ("¥", 31.00), "AU": ("$", 0.36), 
            "BR": ("R$", 0.75), "CA": ("$", 0.16), "UAE": ("AED ", 0.30), 
            "ZA": ("R ", 3.20)
        }
        
        symbol, rate = matrix.get(region_code.upper(), ("₹", 7.50))
        total_estimated_cost = saved_kwh * rate
        
        return f"{symbol}{total_estimated_cost:,.2f}"