# Skill: Smart Grid Operational Safety & Human-in-the-Loop Triage

## Purpose
Enforces operational guardrails over the microgrid energy balancing loops. This skill prevents unauthorized or non-deterministic agent actions during extreme grid anomalies.

## Core Operational Parameters
* **Max Autonomous Transaction Limit:** 5,000 INR
* **Critical Frequency Tolerance Threshold:** 49.5 Hz - 50.5 Hz
* **Maximum Battery State of Charge (SoC) Rate:** 95%
* **Minimum Battery State of Charge (SoC) Rate:** 10%

## Execution Guardrail Protocols

### Protocol A: Automatic Execution (Normal State)
The agent is authorized to execute balancing operations autonomously ONLY when:
1. The simulated grid frequency stays between **49.5 Hz and 50.5 Hz**.
2. The projected transactional arbitrage cost is less than **5,000 INR**.

### Protocol B: Human-in-the-Loop Escalation (Anomaly State)
The agent MUST immediately freeze all operations, halt the trading execution queue, and output an escalation ticket to the human operator if:
1. Grid fluctuations cross critical thresholds (< 49.5 Hz or > 50.5 Hz), signaling a severe grid anomaly.
2. A single balancing market transaction exceeds **5,000 INR**.

## Required Agent Output on Escalation
When a threshold is breached, the agent must output a structured JSON log using this exact schema:
```json
{
  "status": "HALTED",
  "reason": "[Breached Parameter Name]",
  "current_value": "[Live Metric value]",
  "requires_approval": true
}