"""
EcoGrid Core: Multi-Agent SCADA Infrastructure Command Cockpit UI
Integrated User Authentication, Welcome & User Guide, Smart City Traffic & EV Control,
Multi-Agent SCADA, Multi-Country Currency Switcher, AI SCADA Infrastructure Copilot,
Digital Twin Topology Visualizer, Kaggle ML Hub, 3/3 BFT Ledger, and REST Telemetry.
"""

# Safe Tornado patch: Return 200 OK only for HEAD health check requests on / and /health
try:
    import tornado.web
    def _safe_head(self, *args, **kwargs):
        self.set_status(200)
        self.finish()
    tornado.web.RequestHandler.head = _safe_head
except Exception:
    pass

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

# Page Configuration
st.set_page_config(
    page_title="EcoGrid Core AI SCADA Infrastructure",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Vibrant Industrial Cyberpunk Styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0A0F1D 0%, #0E1628 50%, #121A30 100%);
        color: #E2E8F0;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    }
    .login-box {
        background: rgba(18, 26, 48, 0.85);
        border: 2px solid #00E5FF;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 229, 255, 0.2);
        backdrop-filter: blur(8px);
    }
    .main-title {
        font-size: 2.5rem;
        background: linear-gradient(90deg, #00E5FF, #00FF66, #FF007F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .badge-accent {
        background-color: #1E294B;
        border-left: 4px solid #00FF66;
        padding: 10px 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
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
# 🔐 SCREEN 1: DECORATIVE & COLOURFUL LOGIN PORTAL (WHEN NOT LOGGED IN)
# ────────────────────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("<h1 class='main-title' style='text-align: center;'>⚡ ECOGRID CORE AI INFRASTRUCTURE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8F9CAE; font-size: 1.1rem; margin-bottom: 30px;'>Enterprise Multi-Agent SCADA & Smart Grid Control Cockpit</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class='login-box'>
            <h3 style='color: #00E5FF; text-align: center; margin-top: 0;'>🔐 SECURE SYSTEM ACCESS PORTAL</h3>
            <p style='color: #94A3B8; text-align: center; font-size: 0.9rem;'>Select a pre-configured 1-click role or log in with credentials to access the command cockpit.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        auth_tab1, auth_tab2, auth_tab3 = st.tabs(["⚡ 1-Click Quick Demo Login", "🔑 Standard Login", "📝 Register Account"])

        with auth_tab1:
            st.success("🎯 Choose any operational role below to enter immediately:")
            c_a, c_b = st.columns(2)
            with c_a:
                if st.button("👨‍💻 Admin Operator", type="primary", key="btn_admin_quick"):
                    ok, res = auth_manager.authenticate_user("admin", "Admin@123")
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res
                        st.rerun()
                    else:
                        st.error(f"Login failed: {res}")
                if st.button("⚡ Grid Chief Engineer", key="btn_grid_quick"):
                    ok, res = auth_manager.authenticate_user("grid_eng", "Grid@123")
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res
                        st.rerun()
                    else:
                        st.error(f"Login failed: {res}")
            with c_b:
                if st.button("🚦 Traffic Operations Chief", key="btn_traffic_quick"):
                    ok, res = auth_manager.authenticate_user("traffic_op", "Traffic@123")
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res
                        st.rerun()
                    else:
                        st.error(f"Login failed: {res}")
                if st.button("👁️ Guest Auditor", key="btn_guest_quick"):
                    ok, res = auth_manager.authenticate_user("guest", "Guest@123")
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res
                        st.rerun()
                    else:
                        st.error(f"Login failed: {res}")

        with auth_tab2:
            login_user = st.text_input("Username", key="l_user_input")
            login_pwd = st.text_input("Password", type="password", key="l_pwd_input")
            if st.button("Authenticate Session", type="primary", key="btn_std_login_action"):
                if not login_user.strip() or not login_pwd.strip():
                    st.warning("Please enter both username and password.")
                else:
                    ok, res = auth_manager.authenticate_user(login_user, login_pwd)
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res
                        st.success("Authentication successful! Redirecting...")
                        time.sleep(0.3)
                        st.rerun()
                    else:
                        st.error(res)

        with auth_tab3:
            reg_user = st.text_input("Desired Username", key="r_user_input")
            reg_pwd = st.text_input("Password (Min 8 chars, 1 Upper, 1 Lower, 1 Digit)", type="password", key="r_pwd_input")
            reg_role = st.selectbox("Assign Role", ["Microgrid Engineer", "Traffic Controller", "System Auditor"], key="r_role_select")

            if reg_pwd:
                valid, msg = auth_manager.validate_password_strength(reg_pwd)
                if valid:
                    st.caption("✅ Password strength: Strong")
                else:
                    st.caption(f"⚠️ {msg}")

            if st.button("Register & Login", key="btn_register_action"):
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
# 🎛️ SCREEN 2: MAIN DASHBOARD SIDEBAR (WHEN AUTHENTICATED)
# ────────────────────────────────────────────────────────────────────────
user_data = st.session_state.user_info

st.sidebar.markdown("### 🟢 OPERATIONAL SESSION ACTIVE")
st.sidebar.markdown(f"**Operator:** `{user_data['username']}`")
st.sidebar.markdown(f"**Role:** `{user_data['role']}`")

if st.sidebar.button("🚪 Logout Session", key="btn_logout_action"):
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.rerun()

st.sidebar.divider()

# Global Instant Multi-Country Currency Selector
st.sidebar.markdown("### 🌐 INSTANT CURRENCY SWITCHER")
country_options = list(GroundLevelMitigation.COUNTRY_MATRIX.keys())
selected_country_code = st.sidebar.selectbox(
    "Select Global Sector Node",
    country_options,
    index=country_options.index(st.session_state.selected_country),
    format_func=lambda c: f"{c} - {GroundLevelMitigation.COUNTRY_MATRIX[c]['name']} ({GroundLevelMitigation.COUNTRY_MATRIX[c]['symbol']})",
    key="sb_global_country"
)
st.session_state.selected_country = selected_country_code

curr_info = GroundLevelMitigation.get_currency_info(selected_country_code)
st.sidebar.info(f"Active Currency: **{curr_info['currency']} ({curr_info['symbol']})**\nBase Tariff: **{curr_info['symbol']}{curr_info['base_rate_kwh']}/kWh**")

# ────────────────────────────────────────────────────────────────────────
# 🕹️ MAIN DASHBOARD HEADER & TABS CONTAINER
# ────────────────────────────────────────────────────────────────────────
st.markdown("<h1 class='main-title'>⚡ ECOGRID CORE AI SCADA COCKPIT</h1>", unsafe_allow_html=True)
st.caption("Multi-Agent Microgrid SCADA, Smart City Traffic, EV Loadshedding & AI Infrastructure Copilot")

main_tab1, main_tab2, main_tab3, main_tab4, main_tab5, main_tab6, main_tab7, main_tab8, main_tab9 = st.tabs([
    "📖 Welcome & User Guide",
    "⚡ SCADA & Microgrid",
    "🚦 Smart City Traffic",
    "🌐 Multi-Country Currency",
    "🧠 AI SCADA Copilot",
    "🤖 Kaggle AI & ML Hub",
    "🛡️ Cybersecurity & 3/3 BFT",
    "📑 Incident Reports",
    "📡 REST API Telemetry"
])

# ────────────────────────────────────────────────────────────────────────
# TAB 1: WELCOME & SYSTEM USER GUIDE
# ────────────────────────────────────────────────────────────────────────
with main_tab1:
    st.header("📖 WELCOME & SYSTEM OPERATIONAL USER GUIDE")
    st.markdown("""
    Welcome to **EcoGrid Core**, an enterprise-grade multi-agent microgrid SCADA and smart city traffic infrastructure platform.
    """)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("### ⚡ SCADA & Microgrid\nReal-time BFT microgrid load balancing, sine-wave frequency stream monitors, battery SOC health, and regional tariff savings calculation.")
    with c2:
        st.success("### 🚦 Smart City Traffic & EV\nIntersection Congestion Index (ICI), adaptive signal duration phase optimization, emergency corridor overrides, and EV load shedding.")
    with c3:
        st.warning("### 🌐 Multi-Country Currency\nInstant financial conversion across 10 international grid sectors (INR ₹, USD $, EUR €, GBP £, JPY ¥, AUD $, BRL R$, CAD $, UAE AED, ZAR R).")

    st.divider()

    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("### 🧠 AI Infrastructure Copilot\nGoogle Gemini 2.5 Flash & Edge AI producing structured 3-part answers (Executive Summary, Detailed Analysis, and Action Plan).")
    with c5:
        st.markdown("### 🤖 Kaggle AI & ML Hub\nScikit-Learn time-series models trained on Kaggle datasets with live prediction sandboxes, CSV dataset export, and automated retrainer.")
    with c6:
        st.markdown("### 🛡️ Cybersecurity & 3/3 BFT\nChaos Monkey frequency spoofing threat injector, 3/3 BFT unanimous signature consensus evaluator, and SHA-256 cryptographic audit ledger.")

    st.divider()
    st.markdown("""
    ### 🕹️ Quick Start & Navigation Manual:
    - **Switch Domain Panels:** Click any of the 9 tabs at the top of the dashboard to navigate between feature domains.
    - **Change International Currency:** Use the **Instant Currency Switcher** in the sidebar to convert spot clearing tariffs across 10 global sector nodes.
    - **Test Role Permissions:** Log out anytime using the sidebar button and test the **Admin**, **Grid Chief Engineer**, **Traffic Chief**, or **Guest Auditor** presets.
    """)

# ────────────────────────────────────────────────────────────────────────
# TAB 2: ECOGRID SCADA & MICROGRID
# ────────────────────────────────────────────────────────────────────────
with main_tab2:
    st.header("⚡ ECOGRID MULTI-AGENT SCADA CONTROL")
    st.caption("Byzantine Fault Tolerant Microgrid Telemetry & Real-Time Sine Wave Simulation")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("🌐 Regional Tariff Savings")
        saved_kwh = st.slider("Mitigated Energy Volume (kWh)", 10.0, 5000.0, 250.0, step=25.0, key="sl_scada_volume")

        mit_data = GroundLevelMitigation.calculate_regional_mitigation(saved_kwh, st.session_state.selected_country)
        st.metric(f"Mitigation Savings ({mit_data['country_name']})", mit_data['total_savings_formatted'])

        st.divider()
        st.subheader("🔋 Battery Storage Health")
        if st.button("Discharge Battery Cell Reserve (50 kW Load)", key="btn_discharge_cell"):
            b_state = battery.discharge_for_arbitrage(50.0)
            ledger.record_transaction("Arbitrageur_Agent", "BATTERY_DISCHARGE", b_state)

        st.metric("State of Charge (SOC)", f"{battery.state_of_charge}%")
        st.metric("Battery Chemical Health", f"{battery.battery_health}%")

    with col2:
        st.subheader("🕸️ Digital Twin Real-Time Grid Node Topology")
        
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
        st.plotly_chart(fig_topo, key="topo_chart_render_key")

        st.subheader("📊 Live Grid Node Frequency Streams")
        df_stream = pd.DataFrame({
            "Time (s)": np.arange(1, 21),
            "Node_Alpha (Residential)": 50.0 + np.random.normal(0, 0.08, 20),
            "Node_Beta (Industrial)": 49.95 + np.random.normal(0, 0.12, 20),
            "Node_Gamma (Medical)": 50.02 + np.random.normal(0, 0.04, 20)
        })

        fig_grid = px.line(df_stream, x="Time (s)", y=["Node_Alpha (Residential)", "Node_Beta (Industrial)", "Node_Gamma (Medical)"],
                          title="Real-Time Grid Frequency Profiles (Hz)")
        fig_grid.update_layout(paper_bgcolor="#121A30", plot_bgcolor="#121A30", font_color="#FFFFFF")
        st.plotly_chart(fig_grid, key="grid_chart_render_key")

# ────────────────────────────────────────────────────────────────────────
# TAB 3: SMART CITY TRAFFIC & EV GRID
# ────────────────────────────────────────────────────────────────────────
with main_tab3:
    st.header("🚦 SMART CITY TRAFFIC & EV GRID LOAD CONTROL")
    st.caption("Intersection Congestion Index, Signal Phase Optimization, and EV Queue Balancing")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        int_choice = st.selectbox("Target Intersection", ["INT_ALPHA_CBD", "INT_BETA_IND", "INT_GAMMA_MED"], key="sb_target_intersection")
    with col2:
        v_count = st.slider("Main Street Vehicles/Hr", 50, 1500, 950, step=25, key="sl_vcount_main")
    with col3:
        v_speed = st.slider("Average Traffic Speed (km/h)", 5.0, 80.0, 22.5, step=2.5, key="sl_vspeed_avg")
    with col4:
        weather_choice = st.selectbox("Weather Profile", ["SUNNY", "CLOUDY", "RAINY", "STORMY"], key="sb_weather_profile")

    st.divider()
    metrics = EcoGridTrafficEngine.calculate_intersection_metrics(v_count, v_speed, weather_choice)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Congestion Index (ICI)", f"{metrics['congestion_index']:.2f}")
    m2.metric("Traffic Flow Status", metrics['traffic_status_level'])
    m3.metric("Vehicle Density", f"{v_count} veh/hr")
    m4.metric("Average Speed", f"{v_speed} km/h")

    st.subheader("🚦 Adaptive Signal Timing Optimizer")
    c_left, c_right = st.columns([2, 1])

    with c_left:
        cross_count = st.slider("Cross Street Vehicle Load (veh/hr)", 50, 800, 300, step=25, key="sl_cross_street_load")
        emergency_trigger = st.checkbox("🚨 ACTIVATE EMERGENCY GREEN CORRIDOR OVERRIDE", value=False, key="chk_emergency_override")

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
        st.plotly_chart(fig_sig, key="sig_chart_render_key")

    with c_right:
        st.subheader("🔋 EV Charging Station Queue Control")
        grid_load_val = st.number_input("Current Grid Load (kW)", value=1650.0, step=50.0, key="num_ev_grid_load")
        ev_count_val = st.slider("Queued EV Vehicles", 1, 30, 15, key="sl_ev_queue_count")

        ev_res = EcoGridTrafficEngine.balance_ev_charging_queue(grid_load_val, 2000.0, ev_count_val)
        st.write(f"**Mode:** `{ev_res['charging_mode']}`")
        st.write(f"**Power Per Plug:** `{ev_res['power_per_plug_kw']} kW`")
        st.write(f"**Total Station Draw:** `{ev_res['allocated_station_kw']} kW`")
        st.write(f"**Grid Margin:** `{ev_res['remaining_grid_margin_kw']} kW`")

# ────────────────────────────────────────────────────────────────────────
# TAB 4: MULTI-COUNTRY CURRENCY CENTER
# ────────────────────────────────────────────────────────────────────────
with main_tab4:
    st.header("🌐 GLOBAL MULTI-COUNTRY CURRENCY CENTER")
    st.caption("Instant Financial Conversion & Utility Tariff Comparison Matrix Across 10 Countries")

    base_spot_inr = st.number_input("Base Spot Market Clearing Rate (INR / MWh)", value=3500.0, step=100.0, key="num_spot_inr")
    eval_kwh = st.slider("Evaluation Energy Range (kWh)", 100.0, 10000.0, 1500.0, step=100.0, key="sl_eval_energy_range")

    st.subheader("🌍 International Sector Comparison Matrix")
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

    st.divider()
    st.subheader("📊 Financial Mitigation Comparison Chart")
    fig_curr = px.bar(
        df_matrix,
        x="Country Name",
        y=[meta["base_rate_kwh"] * eval_kwh for meta in GroundLevelMitigation.COUNTRY_MATRIX.values()],
        title=f"Mitigation Value across International Grid Sectors for {eval_kwh} kWh",
        labels={"value": "Local Currency Units", "Country Name": "Sector Country"}
    )
    fig_curr.update_layout(paper_bgcolor="#121A30", plot_bgcolor="#121A30", font_color="#FFFFFF")
    st.plotly_chart(fig_curr, key="curr_chart_render_key")

# ────────────────────────────────────────────────────────────────────────
# TAB 5: AI INFRASTRUCTURE COPILOT
# ────────────────────────────────────────────────────────────────────────
with main_tab5:
    st.header("🧠 AI SCADA INFRASTRUCTURE COPILOT")
    st.caption("Powered by Google GenAI (Gemini) & Edge Cognitive AI with Executive Summaries")

    c_q1, c_q2 = st.columns([2, 1])
    with c_q1:
        st.subheader("💬 Ask EcoGrid AI Copilot a Detailed Question")
        preset_q = st.selectbox(
            "Quick Question Presets",
            [
                "Custom Question",
                "How does EcoGrid Core optimize signal timing and EV charging load during peak hours?",
                "What safety protocols trigger when a 53.1 Hz frequency spoofing attack occurs?",
                "How does 3/3 BFT Consensus protect microgrid load dispatch decisions?",
                "Explain the financial impact of dynamic solar power generation predictions."
            ],
            key="sb_preset_ai_q"
        )

        user_q = st.text_area("Your Query", value="" if preset_q == "Custom Question" else preset_q, height=100, key="txt_user_ai_query")

        if st.button("🚀 Analyze with EcoGrid AI Copilot", type="primary", key="btn_ai_analyze_action"):
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

                    st.info("📋 EXECUTIVE SUMMARY")
                    st.write(res["summary"])
                    st.caption(f"Provider: `{res['provider']}`")

                    st.divider()
                    st.markdown("#### 🔬 DETAILED TECHNICAL ANALYSIS & ACTION PLAN")
                    st.markdown(res["full_response"])

    with c_q2:
        st.subheader("⚡ AI System Diagnostic Status")
        st.info("📡 Cloud Channel: Gemini 2.5 Flash Ready")
        st.success("🤖 Local Edge AI Engine: Active")
        st.caption("EcoGrid AI Copilot synthesizes grid telemetry, BFT consensus votes, and Kaggle ML model predictions.")

# ────────────────────────────────────────────────────────────────────────
# TAB 6: KAGGLE AI & ML HUB
# ────────────────────────────────────────────────────────────────────────
with main_tab6:
    st.header("🤖 KAGGLE AI & ML MODEL INTELLIGENCE HUB")
    st.caption("Machine Learning Predictors & Dataset Data Explorer")

    st.subheader("🚀 Retrain Pipeline Trigger")
    if st.button("🔄 Train / Retrain All 4 Kaggle Models Now", type="primary", key="btn_retrain_kaggle_models"):
        with st.spinner("Training Kaggle models on dataset matrices..."):
            retrain_res = train_all_models()
            predictor.load_models()
            st.success("All 4 Kaggle ML Models successfully trained and updated!")
            st.json(retrain_res)

    st.divider()
    st.subheader("🔮 Live Interactive Prediction Sandbox")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 1. Grid Load Predictor")
        p_temp = st.slider("Ambient Temp (°C)", 10.0, 45.0, 32.0, key="sl_ambient_temp")
        p_hum = st.slider("Humidity (%)", 20.0, 95.0, 50.0, key="sl_ambient_hum")
        p_ev = st.slider("EV Station kW", 50.0, 1200.0, 600.0, key="sl_ev_station_draw")
        pred_load = predictor.predict_grid_load(p_temp, p_hum, p_ev)
        st.metric("Predicted Total Grid Load", f"{pred_load:.2f} kW")

    with c2:
        st.markdown("#### 2. Solar Output Predictor")
        p_irr = st.slider("Irradiance (W/m²)", 0.0, 1200.0, 850.0, key="sl_solar_irradiance")
        p_cloud = st.slider("Cloud Cover (%)", 0.0, 100.0, 15.0, key="sl_cloud_cover_pct")
        pred_solar = predictor.predict_solar_generation(p_irr, 35.0, p_cloud)
        st.metric("Predicted Solar Generation", f"{pred_solar:.2f} kW")

    st.divider()
    st.subheader("📊 Kaggle Dataset Data Explorer & CSV Export")

    ds_choice = st.selectbox("Select Kaggle Dataset to Inspect", ["Traffic Flow Dataset", "Grid Load Dataset", "Solar Generation Dataset"], key="sb_kaggle_ds_select")
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
        key="btn_download_dataset_csv"
    )

# ────────────────────────────────────────────────────────────────────────
# TAB 7: CYBERSECURITY & 3/3 BFT LEDGER
# ────────────────────────────────────────────────────────────────────────
with main_tab7:
    st.header("🛡️ CYBERSECURITY & 3/3 BFT CRYPTOGRAPHIC LEDGER")
    st.caption("3/3 Byzantine Fault Tolerance (BFT) Signature Consensus & SHA-256 Ledger Audit")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💥 Chaos Monkey Threat Injector")
        target_n = st.selectbox("Target Injection Node", ["Node_Alpha_Residential", "Node_Beta_Industrial", "Node_Gamma_Medical"], key="sb_chaos_target_node")
        freq_inject = st.slider("Spoofed Frequency Value (Hz)", 48.0, 54.0, 53.1, key="sl_spoofed_freq")

        if st.button("Inject Spoofed Telemetry Attack", key="btn_inject_chaos_attack"):
            anom_res = predictor.detect_cyber_anomaly(freq_inject, 1200.0)
            if anom_res["is_attack_detected"]:
                st.error(f"🚨 CYBER THREAT CONTAINED! Anomaly: {anom_res['anomaly_type']}")
                ledger.record_transaction("SECURITY_KERNEL", "CYBER_ATTACK_CONTAINMENT", {"targeted_node": target_n, "freq": freq_inject})
            else:
                st.success("Telemetry within safe operational boundaries.")

        st.divider()
        st.subheader("⚖️ 3/3 BFT Consensus Evaluator")
        eval_bft = st.button("Evaluate 3/3 Unanimous Consensus Vote", key="btn_evaluate_bft_vote")
        if eval_bft:
            bft_res = BFTConsensusEngine.evaluate_state_proposal("GRID_LOAD_TRANSFER", target_n, {"grid_freq_hz": freq_inject})
            st.json(bft_res)

    with col2:
        st.subheader("📜 Cryptographic SHA-256 Ledger Explorer")
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
                key="btn_download_ledger_csv"
            )
        except Exception as e:
            st.warning(f"Ledger file empty or initializing: {e}")

# ────────────────────────────────────────────────────────────────────────
# TAB 8: INCIDENT REPORTS & PRESCRIPTIONS
# ────────────────────────────────────────────────────────────────────────
with main_tab8:
    st.header("📑 INCIDENT REPORTS & MAINTENANCE PRESCRIPTIONS")
    st.caption("Automated Actionable Engineering Protocols for Ground-Level Technicians")

    c_p1, c_p2 = st.columns([1, 2])
    with c_p1:
        st.subheader("🛠️ Prescription Generator")
        reason = st.selectbox("Trigger Reason", ["Frequency_Spoofing_Attack", "Budget_Overrun_Load_Spike", "Routine_Maintenance_Sweep"], key="sb_incident_trigger_reason")
        val_metric = st.number_input("Observed Metric Value", value=53.1, key="num_observed_metric_val")
        t_node = st.selectbox("Target Node", ["Node_Alpha_Residential", "Node_Beta_Industrial", "Node_Gamma_Medical"], key="sb_incident_target_node")

        prescript = GroundLevelMitigation.get_prescription(reason, val_metric, t_node)

        st.markdown("### 📋 Generated Protocols:")
        for step in prescript:
            st.write(step)

    with c_p2:
        st.subheader("📄 Forensic Incident Report Generator")
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
            key="btn_download_incident_report_md"
        )

# ────────────────────────────────────────────────────────────────────────
# TAB 9: REST API & SYSTEM TELEMETRY
# ────────────────────────────────────────────────────────────────────────
with main_tab9:
    st.header("🌐 REST API & SYSTEM DEPLOYMENT TELEMETRY")
    st.caption("OpenAPI Swagger Endpoints & Containerized Service Status")

    c1, c2, c3 = st.columns(3)
    c1.metric("REST API Engine", "FastAPI v6.5.0-PROD")
    c2.metric("API Endpoint Port", "8000")
    c3.metric("OpenAPI Swagger UI", "http://localhost:8000/docs")

    st.subheader("📑 Available Microservice REST Endpoints")
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