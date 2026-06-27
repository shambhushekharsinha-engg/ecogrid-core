### ⚡ EcoGrid: Multi-Agent SCADA Infrastructure

█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀██    ECOGRID AI INFRASTRUCTURE SYSTEMS MANAGEMENT PANEL v5.5-UI   ██▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=black" alt="Render">
  <img src="https://img.shields.io/badge/Streamlit-Configured-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/License-MIT-000000?style=for-the-badge" alt="License">
</p>

---

## 🔬 Project Overview

**EcoGrid** is a next-generation, containerized microgrid control infrastructure designed to solve the critical vulnerabilities of modern centralized power networks. Traditional Supervisory Control and Data Acquisition (SCADA) systems act as single points of failure, leaving them highly susceptible to systemic cloud outages, localized network partitioning, and targeted cyber-physical attacks. 

By replacing rigid centralized orchestrators with an autonomous, **distributed multi-agent intelligence architecture**, EcoGrid establishes a self-healing grid environment secured by a **3/3 Byzantine Fault Tolerant (BFT) consensus core** and automated **cloud-to-edge failover mechanisms**.

---

## 🏗️ Core Architectural Pillars

* 🤖 **Autonomous Multi-Agent Coordination:** Independent, specialized software agents continuously track localized load demand, evaluate battery states of charge, and perform automated peer-to-peer load-balancing operations in real time.

* 🛡️ **3/3 Byzantine Fault Tolerance (BFT):** Secures grid governance against internal node corruption or malicious data injection. Critical operational changes require a unanimous, cryptographic signature validation across all active cluster agents.

* 🔐 **Immutable Cryptographic Audit Trails:** Every system state change, telemetry baseline update, and consensus agreement is cryptographically signed and secured using **SHA-256 chaining**, creating a permanent, tamper-evident local forensic ledger.

* 🔌 **Automated Cloud-to-Edge Failover:** Equipped with a dedicated latency and heartbeat listener that monitors cloud routing health. If cloud communication drops, edge nodes automatically isolate and transition to localized config baselines without a single byte of state loss.

* 🌐 **Global Multi-Currency Localization:** Features an integrated regionalization engine mapping operations across 10 international grid sectors (including India, US, UK, EU, and Japan), calculating dynamic power mitigation value metrics using real-world localized utility tariffs and currency criteria.

---

## 📁 Technical Repository Structure

The production codebase is structurally organized into modular directories separating the telemetry interface, cryptographic security layers, core agent execution mechanics, and regional settings profiles:

```text
ecogrid-core/
│
├── .streamlit/
│   └── config.toml             # Frontend UI configuration presets
│
├── agents/
│   ├── arbitrageur.json        # Market optimization agent properties
│   └── forecaster.json         # Predictive load demand configurations
│
├── config/
│   ├── sample_grid_data.csv    # Real-world country baseline telemetry datasets
│   └── scenarios.json          # Multi-country pricing and 20 stress-testing profiles
│
├── core/
│   ├── battery_system.py       # Localized storage node simulation logic
│   ├── data_aggregator.py      # Real-time multi-agent parameter consolidation
│   └── mitigation_engine.py    # Active load balancing and multi-currency calculations
│
├── reports/
│   ├── build_matrix.py         # System calculation validation models
│   └── ledger.json             # Local persistent cryptographic ledger history
│
├── security/
│   ├── chaos_monkey.py         # Fault-injection tool for live network partitioning simulation
│   └── crypto_ledger.py        # 3/3 BFT SHA-256 cryptographic chaining core
│
├── skills\grid-safety/
│   └── SKILL.md                # Autonomous safety protocol declarations
│
├── app.py                      # Global entry point application
├── cloud_auditor.py            # Render-to-edge latency and heartbeat listener
├── dashboard_ui.py             # Console-powered global telemetry cockpit UI
├── Dockerfile                  # Production micro-container configurations
├── EcoGrid_Architecture_...xlsx # Structural engineering and currency calculation sheets
├── LICENSE                     # Open-source distribution parameters
├── main.py                     # System operational runtime orchestrator
├── mcp_server.py               # Model Context Protocol communications server
├── README.md                   # Technical onboarding documentation
└── requirements.txt            # Python dependency matrix
```

# ⚙️ Core Protocol & Verification WorkflowThe ecosystem ensures complete transparency and resilience during operational cycles via a strict 4-step pipeline:[ Telemetry Capture ] ──> [ Consensus Verification ] ──> [ Cryptographic Locking ] ──> [ Edge Failover Router ]

#  (Node anomaly check)       (3/3 BFT Bounded Vote)         (SHA-256 Ledger Block)       (Heartbeat Status Sync)

Telemetry Capture: Node sensors track voltage, capacity, and current frequencies, instantly broadcasting telemetry state packets to neighboring agents.Consensus Verification: Peer nodes cross-verify incoming streams against their internal validation engines. If parameters match acceptable structural safety limits, agents sign off on the proposed state change.Cryptographic Locking: Upon crossing a unanimous 3/3 matching threshold, the transaction is declared immutable. The block computes a unique SHA-256 hash string, chaining it directly to the preceding audit ledger history.

Failover Activation: If a primary network partition or high-ping timeout is flagged by the cloud auditor, a localized heartbeat routine kicks in, shifting node instruction parsing to edge profiles until a cloud handshake is re-established.

🚀 Quick Start Deployment Guide Prerequisites Python 3.11+ Docker (Optional, for containerized isolation runs) Local Configuration SetupClone the repository and navigate into the root workspace:
```bash
git clone https://github.com/shambhushekharsinha-engg/ecogrid-core.git
```
```
cd ecogrid-core
```

Install the minimal dependency matrix:
```
pip install -r requirements.txt
```
Initialize the orchestrator application:
```
python main.py
```
## Operational Modes
# Upon launching main.py,
 the interactive terminal cockpit initializes and prompts for execution paths:

# Mode 1: Pre-configured Scenarios:
 Sequentially loops through 20 severe historical and adversarial microgrid stress-tests (e.g., Peak Summer Heatwave, Monsoon Flash Flood, or Ransomware Frequency Injection).

# Mode 2: Quick-Tap Menu:
 Provides full development flexibility, allowing users to manually select spot market pricing scales, atmospheric sky profiles, and inject targeted cyber-threats on individual nodes on the fly.

## 🧪 Simulated Stress-Testing Scenarios
 To prove structural resilience, the system natively tests and documents specific grid disruptions: 

# Byzantine Threat Vector :
  Attempts to inject fraudulent load readings into a specific node. The consensus core detects the outlier signature, blocks block-chaining, and generates an emergency containment log.
  
# Islanding Drill:
  Simulates an abrupt cloud network failure. Edge monitors drop cloud polling speeds under 2.5 seconds and safely enforce local mitigation protocols until restoration occurs.
  
# Ledger Security Test:
  Attempts to retroactively manipulate logging blocks trigger an immediate hash-mismatch warning, neutralizing tamper trends before they penetrate adjacent system boundaries.
  
  ## 👤 Developer Profile 
  # Developed with passion by Shambhu Shekhar Sinha, a Computer Science and Engineering student specializing in Artificial Intelligence and Machine Learning.
  
  # 📄 LicenseThis project is licensed under the MIT License - see the LICENSE file for complete open-source governance parameters.