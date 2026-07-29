"""
EcoGrid AI Infrastructure Copilot & Cognitive Cloud Auditor Engine
Powered by Google GenAI (Gemini) and Edge AI with domain-specific SCADA diagnostic logic.
Provides detailed AI Q&A answers with Executive Summaries, Incident Reports, and Engineering Prescriptions.
"""

import os
import json

class CloudCognitiveAuditor:
    """Enterprise AI Copilot providing Q&A analytics, root-cause analysis, and executive summaries for EcoGrid Core."""

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"⚠️ Gemini Client init note: {e}")

    def answer_user_query(self, user_query: str, context_data: dict = None) -> dict:
        """Answers user queries in detail with an Executive Summary and Actionable Recommendations."""
        ctx_str = json.dumps(context_data or {}, indent=2)

        prompt = f"""
        You are EcoGrid AI Copilot, the Chief SCADA Infrastructure and Smart Grid AI Specialist for EcoGrid Core.
        User Query: "{user_query}"
        
        System Context:
        {ctx_str}
        
        Please format your response into 3 structured sections:
        1. 📋 EXECUTIVE SUMMARY: A concise 2-3 sentence overview answering the user's core question.
        2. 🔬 DETAILED TECHNICAL ANALYSIS: In-depth technical breakdown explaining microgrid physics, ML predictions, BFT consensus status, or operational mechanics.
        3. 🛠️ RECOMMENDED ACTION PLAN: Bulleted step-by-step engineering recommendations for grid operators.
        """

        if self.client:
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                full_text = response.text
                return {
                    "provider": "Google Gemini 2.5 Flash",
                    "full_response": full_text,
                    "summary": full_text.split("🔬")[0].replace("📋 EXECUTIVE SUMMARY:", "").strip() if "🔬" in full_text else full_text[:250] + "..."
                }
            except Exception as e:
                print(f"⚠️ Gemini Cloud call note: {e}")

        # Intelligent Fallback Cognitive Engine (Offline / Local Edge Mode)
        query_lower = user_query.lower()
        if "traffic" in query_lower or "signal" in query_lower or "congestion" in query_lower or "ev" in query_lower:
            summary = "EcoGrid Core utilizes Kaggle-trained Machine Learning models to dynamically manage urban intersection signals and EV charging station queues, safeguarding local grid transformer stability."
            detailed = (
                "### 🚦 EcoGrid Smart City Traffic & EV Management Dynamics\n\n"
                "The Intersection Congestion Index (ICI) evaluates real-time vehicle flow rate (veh/hr), average speed (km/h), and atmospheric conditions.\n"
                "- **Optimal Flow (ICI < 0.60)**: Maintains standard 90s signal cycles with balanced split.\n"
                "- **Moderate Congestion (0.60 <= ICI < 0.85)**: Dynamically extends main-artery green phases up to 75s.\n"
                "- **Critical Congestion (ICI >= 0.85)**: Triggers EV charging load shedding to protect local step-down transformers.\n"
                "- **Emergency Corridor**: Overrides signal light timing instantly to green wave mode (120s green phase).\n"
            )
            recommendations = [
                "Verify sensor calibration on primary intersection cameras (INT_ALPHA_CBD).",
                "Keep EV charging station shedding limits set to 15kW during peak hours (17:00 - 19:00).",
                "Ensure emergency corridor priority routing has 3/3 BFT consensus pre-approval."
            ]
        elif "security" in query_lower or "attack" in query_lower or "ledger" in query_lower or "bft" in query_lower:
            summary = "EcoGrid's 3/3 Byzantine Fault Tolerance (BFT) consensus engine requires unanimous cryptographic signatures across all cluster nodes before committing state changes to the tamper-evident SHA-256 ledger."
            detailed = (
                "### 🛡️ EcoGrid Cryptographic Security & BFT Governance\n\n"
                "When malicious telemetry spoofing occurs (e.g. frequency injected > 50.8 Hz):\n"
                "- **BFT Consensus Engine**: Peer nodes detect outlier grid signatures and reject consensus (0/3 votes).\n"
                "- **Crypto Ledger**: Generates SHA-256 block hash linked to preceding block hash, creating a tamper-evident audit record in both SQLite/PostgreSQL and local JSON ledgers.\n"
                "- **Mitigation Action**: Automated isolation of affected substation breaker lines with manual oscilloscope verification."
            )
            recommendations = [
                "Run periodic Chaos Monkey simulation drills to verify network partitioning resilience.",
                "Inspect local ledger block hashes for chain continuity verification.",
                "Rotate cryptographic node signature keys every 30 days."
            ]
        else:
            summary = "EcoGrid Core integrates distributed multi-agent SCADA control with Kaggle AI predictive models, multi-currency localization, and 3/3 BFT consensus for deployable microgrid & urban energy infrastructure."
            detailed = (
                "### ⚡ EcoGrid SCADA Operational Architecture\n\n"
                "EcoGrid multi-agent SCADA coordinates load demand, solar generation efficiency, and battery state-of-charge (SOC).\n"
                "- **Multi-Country Currency Switching**: Supports instant localization across 10 international grid sectors (INR ₹, USD $, EUR €, GBP £, JPY ¥, AUD $, BRL R$, CAD $, UAE AED, ZAR R).\n"
                "- **Production REST API**: FastAPI backend provides endpoints for ML predictions, traffic signal optimization, BFT consensus voting, and automated retraining."
            )
            recommendations = [
                "Monitor battery chemical health degradation (keep SOC between 20% and 90%).",
                "Utilize the REST API OpenAPI Swagger docs at /docs for system integration.",
                "Trigger automated model retraining when Kaggle dataset drift exceeds 5%."
            ]

        full_resp = f"### 📋 EXECUTIVE SUMMARY\n{summary}\n\n{detailed}\n\n### 🛠️ RECOMMENDED ACTION PLAN\n" + "\n".join([f"- {r}" for r in recommendations])
        return {
            "provider": "EcoGrid Intelligent Cognitive Engine (Local Edge)",
            "full_response": full_resp,
            "summary": summary
        }

    def generate_executive_briefing(self, latest_transaction: dict) -> str:
        """Generates executive briefing summary for a transaction block."""
        return self.answer_user_query("Analyze latest transaction", latest_transaction)["summary"]

auditor = CloudCognitiveAuditor()