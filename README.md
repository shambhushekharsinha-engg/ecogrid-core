# 🚦 Aegis Traffic & ⚡ EcoGrid Core Infrastructure

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-REST_Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-8_Domain_Tabs-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Google_Gemini-AI_Copilot-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white" alt="Google Gemini">
  <img src="https://img.shields.io/badge/Scikit--Learn-Kaggle_AI-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/Multi--Currency-10_Countries-00FF66?style=for-the-badge" alt="Multi-Currency">
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-000000?style=for-the-badge" alt="License">
</p>

---

## 🔬 System Overview

**Aegis Traffic & EcoGrid Core** is an enterprise-grade, containerized urban infrastructure intelligence platform combining **Aegis AI Intelligent Traffic Signal Optimization** with **EcoGrid Multi-Agent Microgrid SCADA Management**. 

Equipped with an **AI Infrastructure Copilot** (powered by Google Gemini 2.5 Flash & Edge AI), an **Instant Multi-Country Currency Switcher** across 10 international sectors, Kaggle time-series dataset Machine Learning models, 3/3 Byzantine Fault Tolerance (BFT) consensus, and a tamper-evident SHA-256 cryptographic audit ledger.

---

## 🗂️ 8 Dedicated System Domain Tabs

The Streamlit Web Cockpit (`app.py`) features 8 dedicated domain tabs:

1. 🚦 **Aegis Traffic Operations:** Intersection Congestion Index (ICI), adaptive green light timing optimization, emergency green wave corridor override, and EV charging queue load shedding.
2. ⚡ **EcoGrid SCADA & Energy Grid:** Multi-agent microgrid load balancing, battery state-of-charge health tracking, live sine-wave frequency stream monitors, and dynamic regional tariff savings.
3. 🌐 **Multi-Country Currency Center:** Instant currency conversion and tariff comparison matrix across 10 international grid sectors (INR ₹, USD $, EUR €, GBP £, JPY ¥, AUD $, BRL R$, CAD $, UAE AED, ZAR R).
4. 🧠 **AI Infrastructure Copilot:** AI Q&A Assistant providing detailed technical analyses, Executive Summaries, and bulleted engineering action plans.
5. 🤖 **Kaggle AI & ML Model Hub:** Scikit-Learn model predictors, live prediction sandboxes, Kaggle dataset data explorer, and 1-click CSV dataset exporter.
6. 🛡️ **Cybersecurity & 3/3 BFT Ledger:** Chaos Monkey threat injector, 3/3 BFT unanimous signature consensus evaluator, SHA-256 ledger explorer, and audit CSV exporter.
7. 📑 **Incident Reports & Prescriptions:** Automated ground-level engineering prescriptions for on-site technicians and downloadable Markdown forensic incident reports.
8. 📡 **REST API & System Telemetry:** Live FastAPI microservice endpoints matrix, OpenAPI Swagger UI link, and system deployment status.

---

## 🌐 Instant Multi-Country Currency Matrix (10 Sectors)

Switching the active country node in the sidebar instantly updates spot market pricing, utility tariffs, and financial savings across the entire application:

| Country Code | Sector Country | Currency | Symbol | Base Tariff (/kWh) |
| :--- | :--- | :--- | :--- | :--- |
| **IN** | India | INR | ₹ | ₹7.50 |
| **US** | United States | USD | $ | $0.18 |
| **EU** | European Union | EUR | € | €0.24 |
| **UK** | United Kingdom | GBP | £ | £0.35 |
| **JP** | Japan | JPY | ¥ | ¥31.00 |
| **AU** | Australia | AUD | $ | $0.36 |
| **BR** | Brazil | BRL | R$ | R$0.75 |
| **CA** | Canada | CAD | $ | $0.16 |
| **UAE** | United Arab Emirates | AED | AED | AED 0.30 |
| **ZA** | South Africa | ZAR | R | R 3.20 |

---

## 🔑 Quick Login Presets (Demo Credentials)

| Role Preset | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `Admin@123` | Full Administrative Access |
| **Traffic Operations Chief** | `traffic_op` | `Traffic@123` | Aegis Traffic Signal Control & Emergency Routing |
| **Microgrid Chief Engineer** | `grid_eng` | `Grid@123` | SCADA Energy Dispatch & Battery Storage |
| **Guest Auditor** | `guest` | `Guest@123` | Read-only Ledger Verification |

---

## 🌐 FastAPI REST Microservice Endpoints

OpenAPI Swagger documentation is accessible at `http://localhost:8000/docs`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | System health, loaded ML models & database backend status |
| `POST` | `/api/v1/auth/register` | Register new user account with password policy check |
| `POST` | `/api/v1/auth/login` | Authenticate user credentials & issue session token |
| `POST` | `/api/v1/auth/demo-login` | 1-click Quick Demo Login preset |
| `POST` | `/api/v1/predict/traffic` | ML Traffic Congestion Index prediction |
| `POST` | `/api/v1/traffic/optimize-signal` | Adaptive Signal Timing Phase Allocation |
| `POST` | `/api/v1/traffic/ev-balance` | EV Charging Queue Load Shedding & Balancing |
| `POST` | `/api/v1/ai/copilot` | AI Copilot Q&A with Executive Summary & Action Plan |
| `POST` | `/api/v1/currency/convert` | Instant multi-country currency conversion |
| `POST` | `/api/v1/predict/load` | Live ML Grid Load demand prediction |
| `POST` | `/api/v1/scada/bft-consensus` | Evaluate 3/3 BFT Consensus vote on proposed action |
| `GET` | `/api/v1/ledger` | Verify SHA-256 ledger block chain integrity |
| `POST` | `/api/v1/ml/retrain` | Trigger automated Kaggle model retraining pipeline |

---

## 🚀 Deployment & Quickstart Guide

### Option 1: Local Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Train Kaggle Machine Learning Models:**
   ```bash
   python -m ml_engine.train_models
   ```

3. **Run Automated Test Suite:**
   ```bash
   python -m pytest tests/test_suite.py
   ```

4. **Launch Application Services:**
   - **Streamlit Web UI Command Cockpit (Port 8501):**
     ```bash
     streamlit run app.py
     ```
   - **FastAPI REST API Server (Port 8000):**
     ```bash
     uvicorn api.server:app --reload --port 8000
     ```

### Option 2: Docker Containerization

```bash
docker-compose up --build
```
Access the Streamlit Command Cockpit at `http://localhost:8501` and FastAPI OpenAPI Docs at `http://localhost:8000/docs`.

---

## 👤 Developer Profile

**Developed by Shambhu Shekhar Sinha**, Computer Science & Engineering student specializing in Artificial Intelligence and Machine Learning.

### 📄 License
Licensed under the [MIT License](LICENSE).
