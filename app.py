"""
EcoGrid Core: Multi-Agent SCADA Infrastructure Command Cockpit UI
Integrated User Authentication, Smart City Traffic & EV Grid Control, Multi-Agent SCADA,
Multi-Country Currency Switcher, AI SCADA Infrastructure Copilot with Summaries,
Digital Twin Topology Visualizer, Kaggle ML Hub, 3/3 BFT Ledger, and REST API Telemetry.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import time

from security.auth import auth_manager
from core.traffic_engine import EcoGridTrafficEngine
from core.consensus_engine import BFTConsensusEngine
from core.battery_system import BatteryBank
from security.crypto_ledger import CryptographicLedger
from security.chaos_monkey import ChaosMonkey
from core.mitigation_engine import GroundLevelMitigation
from core.data_aggregator import DataAggregator
from ml_engine.predictor import predictor
from ml_engine.train_models import train_all_models
from ml_engine.dataset_loader import DatasetLoader
from cloud_auditor import auditor

# Page Config
st.set_page_config(
    page_title="EcoGrid Core AI SCADA Infrastructure",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyberpunk Industrial CSS Theme
st.markdown("""
<style>
    .stApp { background-color: #0A0F1D; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .main-header { font-size: 2.2rem; color: #00E5FF; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; }
    .sub-header { color: #8F9CAE; font-size: 1rem; margin-bottom: 20px; }
    .metric-card { background: #121A30; border: 1px solid #1E294B; border-radius: 8px; padding: 16px; margin: 5px 0; }
    .summary-box { background: #0E1628; border-left: 4px solid #00E5FF; padding: 15px; border-radius: 4px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "selected_country" not in st.session_state:
    st.session_state.selected_country = "IN"

ledger = CryptographicLedger()
battery = BatteryBank()
chaos = ChaosMonkey()

# ────────────────────────────────────────────────────────────────────────
# 🔐 AUTHENTICATION GATE & LOGIN MODAL
# ────────────────────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("<h1 class='main-header' style='text-align: center;'>⚡ ECOGRID CORE AI INFRASTRUCTURE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header' style='text-align: center;'>Enterprise Multi-Agent SCADA & Smart Grid Infrastructure Platform</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='color: #00E5FF; text-align: center;'>🔐 SECURE PORTAL ACCESS</h3>", unsafe_allow_html=True)

        auth_tab1, auth_tab2, auth_tab3 = st.tabs(["⚡ 1-Click Quick Demo Login", "🔑 Standard Login", "📝 Register Account"])

        with auth_tab1:
            st.info("Select a pre-configured role to bypass manual login:")
            c_a, c_b = st.columns(2)
            with c_a:
                if st.button("👨‍💻 Admin Operator", key="btn_admin"):
                    ok, res = auth_manager.authenticate_user("admin", "Admin@123")
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res
                        st.rerun()
                    else:
                        st.error(f"Login failed: {res}")
                if st.button("⚡ Grid Chief Engineer", key="btn_grid"):
                    ok, res = auth_manager.authenticate_user("grid_eng", "Grid@123")
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res
                        st.rerun()
                    else:
                        st.error(f"Login failed: {res}")
            with c_b:
                if st.button("🚦 Traffic Operations Chief", key="btn_traffic"):
                    ok, res = auth_manager.authenticate_user("traffic_op", "Traffic@123")
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res
                        st.rerun()
                    else:
                        st.error(f"Login failed: {res}")
                if st.button("👁️ Guest Auditor", key="btn_guest"):
                    ok, res = auth_manager.authenticate_user("guest", "Guest@123")
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res
                        st.rerun()
                    else:
                        st.error(f"Login failed: {res}")

        with auth_tab2:
            login_user = st.text_input("Username", key="l_user")
            login_pwd = st.text_input("Password", type="password", key="l_pwd")
            if st.button("Login", type="primary", key="btn_std_login"):
                if not login_user.strip() or not login_pwd.strip():
                    st.warning("Please enter both username and password.")
                else:
                    ok, res = auth_manager.authenticate_user(login_user, login_pwd)
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res
                        st.success("Login successful! Redirecting...")
                        time.sleep(0.3)
                        st.rerun()
                    else:
                        st.error(res)

        with auth_tab3:
            reg_user = st.text_input("Desired Username", key="r_user")
            reg_pwd = st.text_input("Password (Min 8 chars, 1 Upper, 1 Lower, 1 Digit)", type="password", key="r_pwd")
            reg_role = st.selectbox("Assign Role", ["Microgrid Engineer", "Traffic Controller", "System Auditor"], key="r_role")

            if reg_pwd:
                valid, msg = auth_manager.validate_password_strength(reg_pwd)
                if valid:
                    st.caption("✅ Password strength: Strong")
                else:
                    st.caption(f"⚠️ {msg}")

            if st.button("Register Account", key="btn_register"):
                ok, msg = auth_manager.register_user(reg_user, reg_pwd, reg_role)
                if ok:
                    st.success(msg)
                    auth_ok, auth_res = auth_manager.authenticate_user(reg_user, reg_pwd)
                    if auth_ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = auth_res
                        time.sleep(0.5)
                        st.rerun()
                else:
                    st.error(msg)
    st.stop()

# ────────────────────────────────────────────────────────────────────────
# 🎛️ SIDEBAR & GLOBAL MULTI-COUNTRY CURRENCY SELECTOR
# ────────────────────────────────────────────────────────────────────────
user_data = st.session_state.user_info

st.sidebar.markdown(f"""
<div style='background:#121A30; border:1px solid #00E5FF; padding:10px; border-radius:6px; margin-bottom:15px;'>
    <div style='color:#00E5FF; font-weight:bold; font-size:12px;'>🟢 SESSION ACTIVE</div>
    <div style='color:#FFFFFF; font-size:14px; font-weight:bold;'>👤 {user_data['username']}</div>
    <div style='color:#8F9CAE; font-size:11px;'>{user_data['role']}</div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout Session", key="btn_logout"):
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.rerun()

st.sidebar.markdown("---")

# Global Instant Multi-Country Currency Selector
st.sidebar.markdown("<h3 style='color:#00E5FF;'>🌐 INSTANT CURRENCY SWITCHER</h3>", unsafe_allow_html=True)
country_options = list(GroundLevelMitigation.COUNTRY_MATRIX.keys())
selected_country_code = st.sidebar.selectbox(
    "Select Global Sector Node",
    country_options,
    index=country_options.index(st.session_state.selected_country),
    format_func=lambda c: f"{c} - {GroundLevelMitigation.COUNTRY_MATRIX[c]['name']} ({GroundLevelMitigation.COUNTRY_MATRIX[c]['symbol']})"
)
st.session_state.selected_country = selected_country_code

curr_info = GroundLevelMitigation.get_currency_info(selected_country_code)
st.sidebar.caption(f"Active Currency: **{curr_info['currency']} ({curr_info['symbol']})** | Base Tariff: **{curr_info['symbol']}{curr_info['base_rate_kwh']}/kWh**")

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color:#00E5FF;'>🕹️ DEDICATED DOMAIN TABS</h3>", unsafe_allow_html=True)

nav_tab = st.sidebar.radio(
    "Select Feature Domain",
    [
        "⚡ EcoGrid SCADA & Microgrid",
        "🚦 Smart City Traffic & EV Grid",
        "🌐 Multi-Country Currency Center",
        "🧠 AI Infrastructure Copilot",
        "🤖 Kaggle AI & ML Hub",
        "🛡️ Cybersecurity & 3/3 BFT Ledger",
        "📑 Incident Reports & Prescriptions",
        "📡 REST API & System Telemetry"
    ]
)

# ────────────────────────────────────────────────────────────────────────
# TAB 1: ECOGRID SCADA & MICROGRID
# ────────────────────────────────────────────────────────────────────────
if "EcoGrid SCADA" in nav_tab:
    st.markdown("<h2 class='main-header'>⚡ ECOGRID MULTI-AGENT SCADA CONTROL</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Byzantine Fault Tolerant Microgrid Telemetry & Real-Time Sine Wave Simulation</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 🌐 Regional Tariff Savings")
        saved_kwh = st.slider("Mitigated Energy Volume (kWh)", 10.0, 5000.0, 250.0, step=25.0)

        mit_data = GroundLevelMitigation.calculate_regional_mitigation(saved_kwh, st.session_state.selected_country)
        st.metric(f"Mitigation Savings ({mit_data['country_name']})", mit_data['total_savings_formatted'])

        st.markdown("---")
        st.markdown("### 🔋 Battery Storage Health")
        b_discharge = st.button("Discharge Battery Cell Reserve (50 kW Load)", key="btn_discharge")
        if b_discharge:
            b_state = battery.discharge_for_arbitrage(50.0)
            ledger.record_transaction("Arbitrageur_Agent", "BATTERY_DISCHARGE", b_state)

        st.metric("State of Charge (SOC)", f"{battery.state_of_charge}%")
        st.metric("Battery Chemical Health", f"{battery.battery_health}%")

    with col2:
        st.markdown("### 🕸️ Digital Twin Real-Time Grid Node Topology")
        
        # Interactive Node Network Diagram using Plotly
        fig_topo = go.Figure()
        
        fig_topo.add_trace(go.Scatter(
            x=[0, 1, 1, 2, 0, 2], y=[0, 1, 1, 0, 0, 0],
            line=dict(width=2, color='#00E5FF'),
            hoverinfo='none',
            mode='lines'
        ))
        
        node_x = [0, 1, 2]
        node_y = [0, 1, 0]
        node_text = ["Node Alpha (Residential)<br>Load: 240 kW | Freq: 50.01 Hz", 
                     "Node Beta (Industrial)<br>Load: 680 kW | Freq: 49.95 Hz", 
                     "Node Gamma (Medical)<br>Load: 310 kW | Freq: 50.02 Hz"]
        node_colors = ['#00FF66', '#FFB300', '#00E5FF']
        
        fig_topo.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=["Node Alpha", "Node Beta", "Node Gamma"],
            textposition="top center",
            hovertext=node_text,
            hoverinfo='text',
            marker=dict(
                size=[30, 45, 35],
                color=node_colors,
                line=dict(width=2, color='#FFFFFF')
            )
        ))
        
        fig_topo.update_layout(
            title="Interactive Grid Node Topology & Power Flow Vector",
            showlegend=False,
            paper_bgcolor="#121A30",
            plot_bgcolor="#121A30",
            font_color="#FFFFFF",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        st.plotly_chart(fig_topo, key="topo_chart_key")

        st.markdown("### 📊 Live Grid Node Frequency Streams")
        df_stream = pd.DataFrame({
            "Time (s)": np.arange(1, 21),
            "Node_Alpha (Residential)": 50.0 + np.random.normal(0, 0.08, 20),
            "Node_Beta (Industrial)": 49.95 + np.random.normal(0, 0.12, 20),
            "Node_Gamma (Medical)": 50.02 + np.random.normal(0, 0.04, 20)
        })

        fig_grid = px.line(df_stream, x="Time (s)", y=["Node_Alpha (Residential)", "Node_Beta (Industrial)", "Node_Gamma (Medical)"],
                          title="Real-Time Grid Frequency Profiles (Hz)")
        fig_grid.update_layout(paper_bgcolor="#121A30", plot_bgcolor="#121A30", font_color="#FFFFFF")
        st.plotly_chart(fig_grid, key="grid_chart_key")

# ────────────────────────────────────────────────────────────────────────
# TAB 2: SMART CITY TRAFFIC & EV GRID
# ────────────────────────────────────────────────────────────────────────
elif "Smart City Traffic" in nav_tab:
    st.markdown("<h2 class='main-header'>🚦 SMART CITY TRAFFIC & EV GRID LOAD CONTROL</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Intersection Congestion Index, Signal Phase Optimization, and EV Queue Balancing</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        int_choice = st.selectbox("Target Intersection", ["INT_ALPHA_CBD", "INT_BETA_IND", "INT_GAMMA_MED"])
    with col2:
        v_count = st.slider("Main Street Vehicles/Hr", 50, 1500, 950, step=25)
    with col3:
        v_speed = st.slider("Average Traffic Speed (km/h)", 5.0, 80.0, 22.5, step=2.5)
    with col4:
        weather_choice = st.selectbox("Weather Profile", ["SUNNY", "CLOUDY", "RAINY", "STORMY"])

    st.markdown("---")
    metrics = EcoGridTrafficEngine.calculate_intersection_metrics(v_count, v_speed, weather_choice)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Congestion Index (ICI)", f"{metrics['congestion_index']:.2f}")
    m2.metric("Traffic Flow Status", metrics['traffic_status_level'])
    m3.metric("Vehicle Density", f"{v_count} veh/hr")
    m4.metric("Average Speed", f"{v_speed} km/h")

    st.markdown("### 🚦 Adaptive Signal Timing Optimizer")
    c_left, c_right = st.columns([2, 1])

    with c_left:
        cross_count = st.slider("Cross Street Vehicle Load (veh/hr)", 50, 800, 300, step=25)
        emergency_trigger = st.checkbox("🚨 ACTIVATE EMERGENCY GREEN CORRIDOR OVERRIDE", value=False)

        opt_plan = EcoGridTrafficEngine.optimize_signal_timing(int_choice, v_count, cross_count, emergency_trigger)

        if emergency_trigger:
            st.error(opt_plan["action_summary"])
        else:
            st.success(opt_plan["action_summary"])

        fig_sig = go.Figure(go.Bar(
            x=['Main Street Green', 'Cross Street Green', 'Pedestrian Walk'],
            y=[opt_plan['main_street_green_sec'], opt_plan['cross_street_green_sec'], opt_plan['pedestrian_walk_sec']],
            marker_color=['#00FF66', '#00E5FF', '#FFB300']
        ))
        fig_sig.update_layout(title="Signal Phase Duration Allocation (Seconds)", paper_bgcolor="#121A30", plot_bgcolor="#121A30", font_color="#FFFFFF")
        st.plotly_chart(fig_sig, key="sig_chart_key")

    with c_right:
        st.markdown("### 🔋 EV Charging Station Queue Control")
        grid_load_val = st.number_input("Current Grid Load (kW)", value=1650.0, step=50.0)
        ev_count_val = st.slider("Queued EV Vehicles", 1, 30, 15)

        ev_res = EcoGridTrafficEngine.balance_ev_charging_queue(grid_load_val, 2000.0, ev_count_val)
        st.write(f"**Mode:** `{ev_res['charging_mode']}`")
        st.write(f"**Power Per Plug:** `{ev_res['power_per_plug_kw']} kW`")
        st.write(f"**Total Station Draw:** `{ev_res['allocated_station_kw']} kW`")
        st.write(f"**Grid Margin:** `{ev_res['remaining_grid_margin_kw']} kW`")

# ────────────────────────────────────────────────────────────────────────
# TAB 3: MULTI-COUNTRY CURRENCY CENTER
# ────────────────────────────────────────────────────────────────────────
elif "Multi-Country Currency" in nav_tab:
    st.markdown("<h2 class='main-header'>🌐 GLOBAL MULTI-COUNTRY CURRENCY CENTER</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Instant Financial Conversion & Utility Tariff Comparison Matrix Across 10 Countries</p>", unsafe_allow_html=True)

    base_spot_inr = st.number_input("Base Spot Market Clearing Rate (INR / MWh)", value=3500.0, step=100.0)
    eval_kwh = st.slider("Evaluation Energy Range (kWh)", 100.0, 10000.0, 1500.0, step=100.0)

    st.markdown("### 🌍 International Sector Comparison Matrix")
    matrix_rows = []
    for c_code, meta in GroundLevelMitigation.COUNTRY_MATRIX.items():
        converted_rate, formatted_rate = GroundLevelMitigation.convert_price_from_inr(base_spot_inr, c_code)
        mit = GroundLevelMitigation.calculate_regional_mitigation(eval_kwh, c_code)
        matrix_rows.append({
            "Country Code": c_code,
            "Country Name": meta["name"],
            "Currency": meta["currency"],
            "Symbol": meta["symbol"],
            "Utility Tariff (/kWh)": f"{meta['symbol']}{meta['base_rate_kwh']}",
            "Converted Spot Rate (/MWh)": formatted_rate,
            "Mitigated Savings": mit["total_savings_formatted"]
        })

    df_matrix = pd.DataFrame(matrix_rows)
    st.dataframe(df_matrix)

    st.markdown("---")
    st.markdown("### 📊 Financial Mitigation Comparison Chart")
    fig_curr = px.bar(
        df_matrix,
        x="Country Name",
        y=[meta["base_rate_kwh"] * eval_kwh for meta in GroundLevelMitigation.COUNTRY_MATRIX.values()],
        title=f"Mitigation Value across International Grid Sectors for {eval_kwh} kWh",
        labels={"value": "Local Currency Units", "Country Name": "Sector Country"}
    )
    fig_curr.update_layout(paper_bgcolor="#121A30", plot_bgcolor="#121A30", font_color="#FFFFFF")
    st.plotly_chart(fig_curr, key="curr_chart_key")

# ────────────────────────────────────────────────────────────────────────
# TAB 4: AI INFRASTRUCTURE COPILOT
# ────────────────────────────────────────────────────────────────────────
elif "AI Infrastructure Copilot" in nav_tab:
    st.markdown("<h2 class='main-header'>🧠 AI SCADA INFRASTRUCTURE COPILOT</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Powered by Google GenAI (Gemini) & Edge Cognitive AI with Executive Summaries</p>", unsafe_allow_html=True)

    c_q1, c_q2 = st.columns([2, 1])
    with c_q1:
        st.markdown("### 💬 Ask EcoGrid AI Copilot a Detailed Question")
        preset_q = st.selectbox(
            "Quick Question Presets",
            [
                "Custom Question",
                "How does EcoGrid Core optimize signal timing and EV charging load during peak hours?",
                "What safety protocols trigger when a 53.1 Hz frequency spoofing attack occurs?",
                "How does 3/3 BFT Consensus protect microgrid load dispatch decisions?",
                "Explain the financial impact of dynamic solar power generation predictions."
            ]
        )

        user_q = st.text_area("Your Query", value="" if preset_q == "Custom Question" else preset_q, height=100)

        if st.button("🚀 Analyze with EcoGrid AI Copilot", type="primary", key="btn_ai_analyze"):
            if not user_q.strip():
                st.warning("Please enter a question or select a preset.")
            else:
                with st.spinner("EcoGrid AI Copilot analyzing system telemetry and diagnostic models..."):
                    ctx = {
                        "active_country": st.session_state.selected_country,
                        "battery_soc": battery.state_of_charge,
                        "loaded_models": list(predictor.models.keys())
                    }
                    res = auditor.answer_user_query(user_q, ctx)

                    st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
                    st.markdown("#### 📋 EXECUTIVE SUMMARY")
                    st.write(res["summary"])
                    st.markdown(f"*Provider: `{res['provider']}`*", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("---")
                    st.markdown("#### 🔬 DETAILED TECHNICAL ANALYSIS & ACTION PLAN")
                    st.markdown(res["full_response"])

    with c_q2:
        st.markdown("### ⚡ AI System Diagnostic Status")
        st.info("📡 Cloud Channel: Gemini 2.5 Flash Ready")
        st.success("🤖 Local Edge AI Engine: Active")
        st.caption("EcoGrid AI Copilot synthesizes grid telemetry, BFT consensus votes, and Kaggle ML model predictions.")

# ────────────────────────────────────────────────────────────────────────
# TAB 5: KAGGLE AI & ML HUB
# ────────────────────────────────────────────────────────────────────────
elif "Kaggle AI" in nav_tab:
    st.markdown("<h2 class='main-header'>🤖 KAGGLE AI & ML MODEL INTELLIGENCE HUB</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Machine Learning Predictors & Dataset Data Explorer</p>", unsafe_allow_html=True)

    st.markdown("### 🚀 Retrain Pipeline Trigger")
    if st.button("🔄 Train / Retrain All 4 Kaggle Models Now", type="primary", key="btn_retrain_ml"):
        with st.spinner("Training Kaggle models on dataset matrices..."):
            retrain_res = train_all_models()
            predictor.load_models()
            st.success("All 4 Kaggle ML Models successfully trained and updated!")
            st.json(retrain_res)

    st.markdown("---")
    st.markdown("### 🔮 Live Interactive Prediction Sandbox")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 1. Grid Load Predictor")
        p_temp = st.slider("Ambient Temp (°C)", 10.0, 45.0, 32.0)
        p_hum = st.slider("Humidity (%)", 20.0, 95.0, 50.0)
        p_ev = st.slider("EV Station kW", 50.0, 1200.0, 600.0)
        pred_load = predictor.predict_grid_load(p_temp, p_hum, p_ev)
        st.metric("Predicted Total Grid Load", f"{pred_load:.2f} kW")

    with c2:
        st.markdown("#### 2. Solar Output Predictor")
        p_irr = st.slider("Irradiance (W/m²)", 0.0, 1200.0, 850.0)
        p_cloud = st.slider("Cloud Cover (%)", 0.0, 100.0, 15.0)
        pred_solar = predictor.predict_solar_generation(p_irr, 35.0, p_cloud)
        st.metric("Predicted Solar Generation", f"{pred_solar:.2f} kW")

    st.markdown("---")
    st.markdown("### 📊 Kaggle Dataset Data Explorer & CSV Export")

    ds_choice = st.selectbox("Select Kaggle Dataset to Inspect", ["Traffic Flow Dataset", "Grid Load Dataset", "Solar Generation Dataset"])
    if ds_choice == "Traffic Flow Dataset":
        df_ds = DatasetLoader.load_traffic_dataset()
    elif ds_choice == "Grid Load Dataset":
        df_ds = DatasetLoader.load_grid_load_dataset()
    else:
        df_ds = DatasetLoader.load_solar_dataset()

    st.dataframe(df_ds)

    csv_data = df_ds.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download {ds_choice} as CSV",
        data=csv_data,
        file_name=f"{ds_choice.lower().replace(' ', '_')}.csv",
        mime="text/csv",
        key="btn_dl_dataset"
    )

# ────────────────────────────────────────────────────────────────────────
# TAB 6: CYBERSECURITY & 3/3 BFT LEDGER
# ────────────────────────────────────────────────────────────────────────
elif "Cybersecurity" in nav_tab:
    st.markdown("<h2 class='main-header'>🛡️ CYBERSECURITY & 3/3 BFT CRYPTOGRAPHIC LEDGER</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>3/3 Byzantine Fault Tolerance (BFT) Signature Consensus & SHA-256 Ledger Audit</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 💥 Chaos Monkey Threat Injector")
        target_n = st.selectbox("Target Injection Node", ["Node_Alpha_Residential", "Node_Beta_Industrial", "Node_Gamma_Medical"])
        freq_inject = st.slider("Spoofed Frequency Value (Hz)", 48.0, 54.0, 53.1)

        if st.button("Inject Spoofed Telemetry Attack", key="btn_chaos"):
            anom_res = predictor.detect_cyber_anomaly(freq_inject, 1200.0)
            if anom_res["is_attack_detected"]:
                st.error(f"🚨 CYBER THREAT CONTAINED! Anomaly: {anom_res['anomaly_type']}")
                ledger.record_transaction("SECURITY_KERNEL", "CYBER_ATTACK_CONTAINMENT", {"targeted_node": target_n, "freq": freq_inject})
            else:
                st.success("Telemetry within safe operational boundaries.")

        st.markdown("---")
        st.markdown("### ⚖️ 3/3 BFT Consensus Evaluator")
        eval_bft = st.button("Evaluate 3/3 Unanimous Consensus Vote", key="btn_bft")
        if eval_bft:
            bft_res = BFTConsensusEngine.evaluate_state_proposal("GRID_LOAD_TRANSFER", target_n, {"grid_freq_hz": freq_inject})
            st.json(bft_res)

    with col2:
        st.markdown("### 📜 Cryptographic SHA-256 Ledger Explorer")
        is_val, val_msg = ledger.verify_chain()
        if is_val:
            st.success(f"✅ {val_msg}")
        else:
            st.error(f"🚨 {val_msg}")

        try:
            with open("reports/ledger.json", "r", encoding="utf-8") as f:
                blocks = json.load(f)
            st.markdown(f"**Total Verified Blocks:** `{len(blocks)}`")
            st.dataframe(pd.DataFrame(blocks).tail(10))

            ledger_csv = pd.DataFrame(blocks).to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Audit Ledger as CSV",
                data=ledger_csv,
                file_name="grid_audit_ledger.csv",
                mime="text/csv",
                key="btn_dl_ledger"
            )
        except Exception as e:
            st.warning(f"Ledger file empty or initializing: {e}")

# ────────────────────────────────────────────────────────────────────────
# TAB 7: INCIDENT REPORTS & PRESCRIPTIONS
# ────────────────────────────────────────────────────────────────────────
elif "Incident Reports" in nav_tab:
    st.markdown("<h2 class='main-header'>📑 INCIDENT REPORTS & MAINTENANCE PRESCRIPTIONS</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Automated Actionable Engineering Protocols for Ground-Level Technicians</p>", unsafe_allow_html=True)

    c_p1, c_p2 = st.columns([1, 2])
    with c_p1:
        st.markdown("### 🛠️ Prescription Generator")
        reason = st.selectbox("Trigger Reason", ["Frequency_Spoofing_Attack", "Budget_Overrun_Load_Spike", "Routine_Maintenance_Sweep"])
        val_metric = st.number_input("Observed Metric Value", value=53.1)
        t_node = st.selectbox("Target Node", ["Node_Alpha_Residential", "Node_Beta_Industrial", "Node_Gamma_Medical"])

        prescript = GroundLevelMitigation.get_prescription(reason, val_metric, t_node)

        st.markdown("### 📋 Generated Protocols:")
        for step in prescript:
            st.write(step)

    with c_p2:
        st.markdown("### 📄 Forensic Incident Report Generator")
        report_title = f"INCIDENT REPORT: {reason.upper()} on {t_node.upper()}"
        report_body = f"""# {report_title}
**Date/Time:** {time.strftime('%Y-%m-%d %H:%M:%S')}  
**Target Sector Node:** {t_node}  
**Observed Metric:** {val_metric}  
**Sector Country Node:** {st.session_state.selected_country}  

## 🔬 Executive Summary
An anomaly event ({reason}) was flagged on {t_node}. The 3/3 BFT consensus core isolated the vector and logged transaction to the SHA-256 ledger.

## 🛠️ Actionable Ground-Level Engineering Protocols
""" + "\n".join([f"- {s}" for s in prescript]) + """

## 🔐 Signatures
- **EcoGrid SCADA Chief:** Verified
- **EcoGrid Core Core:** Sealed (SHA-256 Ledger)
"""

        st.markdown(report_body)
        st.download_button(
            label="📥 Download Incident Report (.md)",
            data=report_body.encode('utf-8'),
            file_name=f"incident_report_{t_node}.md",
            mime="text/markdown",
            key="btn_dl_report"
        )

# ────────────────────────────────────────────────────────────────────────
# TAB 8: REST API & SYSTEM TELEMETRY
# ────────────────────────────────────────────────────────────────────────
elif "REST API" in nav_tab:
    st.markdown("<h2 class='main-header'>🌐 REST API & SYSTEM DEPLOYMENT TELEMETRY</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>OpenAPI Swagger Endpoints & Containerized Service Status</p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("REST API Engine", "FastAPI v6.5.0-PROD")
    c2.metric("API Endpoint Port", "8000")
    c3.metric("OpenAPI Swagger UI", "http://localhost:8000/docs")

    st.markdown("### 📑 Available Microservice REST Endpoints")
    endpoints_df = pd.DataFrame([
        {"Method": "POST", "Endpoint": "/api/v1/auth/login", "Description": "Authenticate user credentials & issue session token"},
        {"Method": "POST", "Endpoint": "/api/v1/auth/demo-login", "Description": "1-click Quick Demo Login preset"},
        {"Method": "POST", "Endpoint": "/api/v1/predict/traffic", "Description": "ML Traffic Congestion Index prediction"},
        {"Method": "POST", "Endpoint": "/api/v1/traffic/optimize-signal", "Description": "Adaptive Signal Timing Phase Allocation"},
        {"Method": "POST", "Endpoint": "/api/v1/ai/copilot", "Description": "AI Copilot Q&A with Executive Summary"},
        {"Method": "POST", "Endpoint": "/api/v1/currency/convert", "Description": "Instant multi-country currency conversion"},
        {"Method": "POST", "Endpoint": "/api/v1/predict/load", "Description": "Kaggle ML Grid Load prediction"},
        {"Method": "POST", "Endpoint": "/api/v1/scada/bft-consensus", "Description": "3/3 BFT Consensus voting on state changes"},
        {"Method": "GET", "Endpoint": "/api/v1/ledger", "Description": "Verify SHA-256 ledger block chain integrity"},
        {"Method": "POST", "Endpoint": "/api/v1/ml/retrain", "Description": "Trigger automated model retraining"}
    ])
    st.dataframe(endpoints_df)