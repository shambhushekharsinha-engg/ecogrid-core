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