# EcoGrid AI: Autonomous Smart Grid Arbitrage & Core Balancer

EcoGrid AI is an autonomous, multi-agent infrastructure orchestration engine designed for localized smart microgrids. Built using the **Agent Development Kit (ADK)** structural philosophy, the system intelligently balances volatile renewable energy inputs against real-time consumer demands, leverages external data environments via

## 🏗️ Architectural Topology

The software architecture completely decouples data tracking from transactional execution routing. The main orchestrator manages synchronization loops between two isolated, specialized agents, validating telemetry streams against strict decoupled security skill files.

```text
[ Live Microgrid Telemetry Stream ] 
                   │
                   ▼
   ┌───────────────────────────────┐
   │     main.py (Orchestrator)    │◄─────── [ mcp_server.py ]
   └───────────────┬───────────────┘       (Live Weather Context)
                   │
    ┌──────────────┴──────────────┐
    ▼                             ▼
    ┌────────────────┐            ┌────────────────┐
│   Forecaster   │            │  Arbitrageur   │
│    Agent       │───────────►│    Agent       │
└───────┬────────┘            └───────┬────────┘
│                             │
└──────────────┬──────────────┘
│ Validates Constraints Against
▼
┌───────────────────────────┐
│ skills/grid-safety/       │
│         └── SKILL.md      │
└───────────────────────────┘

## 📂 System Directory Layout

The project enforces a strict, portable skill hierarchy preventing context rot and keeping execution rules independent of the model's primary system instructions:

```text
ecogrid-core/
│
├── main.py                    # Master Engine Orchestrator & Loop Synchronization
├── mcp_server.py              # Weather Telemetry Model Context Protocol Emulator
├── battery_system.py          # Stateful Lithium-Ion Chemical Degradation Tracker
│
├── agents/
│   ├── forecaster.json        # Agent 1: System constraints and instructions
│   └── arbitrageur.json       # Agent 2: Financial trading routing constraints
│
└── skills/
    └── grid-safety/
        └── SKILL.md           # Decoupled Security Parameters & HITL Containment Rules

```
```text

🛠️ Multi-Aspect System Features
This project cleanly demonstrates three key high-impact technical architectures:

Evaluation Metric   

Agent Framework

Context Protocol

Safety Guardrails

Asset State Mgmt
