"""
Ground-Level Mitigation Engine & International Multi-Country Currency Matrix
Calculates dynamic operational mitigation costs, localized utility tariffs,
and instant multi-currency conversions across 10 international grid sectors.
"""

class GroundLevelMitigation:
    """Generates actionable engineering prescriptions and manages international currency localization."""

    # Dynamic Currency & Utility Tariff Matrix for 10 Countries
    COUNTRY_MATRIX = {
        "IN": {"name": "India", "currency": "INR", "symbol": "₹", "base_rate_kwh": 7.50, "inr_conversion": 1.0},
        "US": {"name": "United States", "currency": "USD", "symbol": "$", "base_rate_kwh": 0.18, "inr_conversion": 0.012},
        "EU": {"name": "European Union", "currency": "EUR", "symbol": "€", "base_rate_kwh": 0.24, "inr_conversion": 0.011},
        "UK": {"name": "United Kingdom", "currency": "GBP", "symbol": "£", "base_rate_kwh": 0.35, "inr_conversion": 0.0093},
        "JP": {"name": "Japan", "currency": "JPY", "symbol": "¥", "base_rate_kwh": 31.00, "inr_conversion": 1.82},
        "AU": {"name": "Australia", "currency": "AUD", "symbol": "$", "base_rate_kwh": 0.36, "inr_conversion": 0.018},
        "BR": {"name": "Brazil", "currency": "BRL", "symbol": "R$", "base_rate_kwh": 0.75, "inr_conversion": 0.068},
        "CA": {"name": "Canada", "currency": "CAD", "symbol": "$", "base_rate_kwh": 0.16, "inr_conversion": 0.016},
        "UAE": {"name": "United Arab Emirates", "currency": "AED", "symbol": "AED ", "base_rate_kwh": 0.30, "inr_conversion": 0.044},
        "ZA": {"name": "South Africa", "currency": "ZAR", "symbol": "R ", "base_rate_kwh": 3.20, "inr_conversion": 0.22}
    }

    @classmethod
    def get_currency_info(cls, country_code: str = "IN") -> dict:
        """Retrieves country metadata, symbol, base tariff rate, and conversion ratio."""
        code = country_code.upper().strip()
        return cls.COUNTRY_MATRIX.get(code, cls.COUNTRY_MATRIX["IN"])

    @classmethod
    def convert_price_from_inr(cls, price_inr: float, target_country_code: str = "IN") -> tuple[float, str]:
        """Instantly converts spot market rate in INR to target country's currency."""
        info = cls.get_currency_info(target_country_code)
        converted_val = price_inr * info["inr_conversion"]
        formatted_str = f"{info['symbol']}{converted_val:,.2f} {info['currency']}"
        return converted_val, formatted_str

    @classmethod
    def calculate_regional_mitigation(cls, saved_kwh: float, country_code: str = "IN") -> dict:
        """Calculates dynamic financial mitigation savings localized to target country."""
        info = cls.get_currency_info(country_code)
        total_cost = saved_kwh * info["base_rate_kwh"]
        return {
            "country_code": country_code.upper(),
            "country_name": info["name"],
            "currency_code": info["currency"],
            "currency_symbol": info["symbol"],
            "base_tariff_per_kwh": info["base_rate_kwh"],
            "mitigated_kwh": saved_kwh,
            "total_savings_raw": round(total_cost, 2),
            "total_savings_formatted": f"{info['symbol']}{total_cost:,.2f}"
        }

    @staticmethod
    def get_prescription(reason_code: str, current_value: float, targeted_node: str) -> list[str]:
        """Generates ground-level engineering prescriptions for microgrid field technicians."""
        if "Frequency" in reason_code or "SPOOF" in reason_code or "ANOMALY" in reason_code:
            return [
                f"1. [FIELD ACTION] Dispatch emergency technician crew to Substation Box ({targeted_node.upper()}).",
                f"2. [ISOLATION] Isolate sub-station breaker line from primary feed (Frequency offset: {current_value} Hz).",
                "3. [FIRMWARE FLUSH] Purge local RTU cache and re-verify 3/3 BFT cryptographic handshake.",
                "4. [HARDWARE TEST] Manually measure inverter phase angles with a handheld digital oscilloscope."
            ]
        elif "Budget" in reason_code or "Load" in reason_code or "SPIKE" in reason_code:
            return [
                f"1. [LOAD SHEDDING] Initiate automatic load shedding on non-critical industrial circuits at {targeted_node.upper()}.",
                f"2. [THERMAL CHECK] Inspect step-down transformers for high thermal degradation due to load spike ({current_value} kW).",
                "3. [BATTERY DISCHARGE] Engage local battery array for parallel discharge balancing.",
                "4. [DEMAND RESPONSE] Broadcast curtailment alerts to high-draw consumer relays."
            ]
        else:
            return [
                f"1. [PHYSICAL SWEEP] Perform routine visual inspection of junction sub-arrays at {targeted_node.upper()}.",
                "2. [SYSTEM REBOOT] Force manual hard-reset of telemetry ingestion kernel."
            ]