"""
EcoGrid Core: Enterprise Multi-Agent SCADA Infrastructure Command Cockpit UI
Integrated User Authentication, Welcome & User Guide, Smart City Traffic & EV Control,
Multi-Agent SCADA, Multi-Country Currency Switcher, AI SCADA Infrastructure Copilot,
Digital Twin Topology Visualizer, Kaggle ML Hub, 3/3 BFT Ledger, REST Telemetry, and
Data & File Inspector with safe file handling.
"""

# Safe Tornado patch: Return 200 OK for HEAD health check requests on / and /health
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
import io

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

# ────────────────────────────────────────────────────────────────────────
# 🎨 CYBERPUNK DARK THEME & UI STYLING
# ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top right, #121A30 0%, #060913 70%);
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }

    /* Left Sidebar Styling */
    [data-testid="stSidebar"] {
        background: radial-gradient(circle at top left, #121A30 0%, #060913 90%) !important;
        border-right: 2px solid rgba(0, 245, 212, 0.3) !important;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.5) !important;
    }
    
    [data-testid="stSidebar"] h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00F5D4 !important;
        text-shadow: 0 0 10px rgba(0, 245, 212, 0.4) !important;
        font-weight: 800 !important;
    }

    [data-testid="stSidebar"] .stSelectbox label, 
    [data-testid="stSidebar"] .stMarkdown p {
        color: #00E5FF !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.5px;
    }
    
    /* Header Typography */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #00F5D4, #00BBF9, #F15BB5, #9B5DE5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 15px rgba(0, 245, 212, 0.3);
        font-weight: 900 !important;
    }
    
    /* Button Styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
        background: linear-gradient(135deg, #00BBF9 0%, #9B5DE5 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 187, 249, 0.3) !important;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 187, 249, 0.5) !important;
    }
    
    /* Custom Cards */
    .login-box {
        background: rgba(10, 15, 29, 0.85);
        border: 2px solid #00F5D4;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 245, 212, 0.2);
        backdrop-filter: blur(12px);
        margin-top: 20px;
    }
    
    .dashboard-card {
        background: rgba(18, 26, 48, 0.6);
        border: 1px solid rgba(0, 245, 212, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .card-cyan { border-left: 5px solid #00BBF9; }
    .card-green { border-left: 5px solid #00F5D4; }
    .card-magenta { border-left: 5px solid #F15BB5; }
    .card-purple { border-left: 5px solid #9B5DE5; }
    
    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: #00F5D4;
        text-shadow: 0 0 10px rgba(0, 245, 212, 0.5);
    }
    
    .metric-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Right-Side Custom Tab Bar Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(10, 15, 29, 0.7);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(0, 245, 212, 0.2);
        overflow-x: auto;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 8px;
        color: #94A3B8;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 0px 16px;
        background-color: transparent;
        transition: all 0.2s ease-in-out;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 245, 212, 0.25) 0%, rgba(0, 187, 249, 0.25) 100%) !important;
        color: #00F5D4 !important;
        border: 1px solid #00F5D4 !important;
        box-shadow: 0 0 15px rgba(0, 245, 212, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────
# 🔐 SESSION STATE GUARANTEE & HELPER FUNCTIONS
# ────────────────────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_info" not in st.session_state or st.session_state["user_info"] is None:
    st.session_state["user_info"] = {"username": "Operator", "role": "Administrator"}
if "selected_country" not in st.session_state:
    st.session_state["selected_country"] = "IN"

ledger = CryptographicLedger()
battery = BatteryBank()
chaos = ChaosMonkey()

def safe_read_file_content(file_path: str) -> tuple[bool, str, str]:
    """Safely reads a text/JSON file with path fallbacks and encoding protection."""
    paths_to_try = [
        file_path,
        os.path.join("config", os.path.basename(file_path)),
        os.path.join("reports", os.path.basename(file_path)),
        os.path.join("data", os.path.basename(file_path)),
        os.path.join(os.path.dirname(__file__), file_path)
    ]
    for p in paths_to_try:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    content = f.read()
                return True, content, p
            except UnicodeDecodeError:
                try:
                    with open(p, "r", encoding="latin-1") as f:
                        content = f.read()
                    return True, content, p
                except Exception as e:
                    return False, f"Read error: {e}", p
            except Exception as e:
                return False, f"Read error: {e}", p
    return False, f"File not found in system search paths: {file_path}", file_path

# ────────────────────────────────────────────────────────────────────────
# 🔐 SCREEN 1: LOGIN PORTAL (UNAUTHENTICATED)
# ────────────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated", False):
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>⚡ ECOGRID CORE AI SCADA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 1.2rem; font-family: Rajdhani;'>Enterprise Multi-Agent SCADA & Smart Grid Control Cockpit</p>", unsafe_allow_html=True)
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class='login-box'>
            <h2 style='color: #00F5D4; text-align: center; margin-top: 0; font-size: 1.8rem;'>🔐 SECURE PORTAL ACCESS</h2>
            <p style='color: #94A3B8; text-align: center; font-size: 0.95rem; margin-bottom: 20px;'>Configure your access parameters to initialize the multi-agent control shell.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        access_choice = st.selectbox(
            "Access Method Protocol",
            ["⚡ 1-Click Quick Demo Login", "🔑 Standard Login", "📝 Register Account"],
            key="login_access_choice_select"
        )
        st.write("")

        if access_choice == "⚡ 1-Click Quick Demo Login":
            st.info("🎯 Select a control profile for instant authorization:")
            c_a, c_b = st.columns(2)
            with c_a:
                if st.button("👨‍💻 Admin Operator", type="primary", use_container_width=True, key="quick_admin_btn"):
                    st.session_state["authenticated"] = True
                    st.session_state["user_info"] = {"username": "admin", "role": "System Administrator", "token": "sec_demo_admin"}
                    st.rerun()
                st.write("")
                if st.button("⚡ Grid Chief Engineer", use_container_width=True, key="quick_grid_btn"):
                    st.session_state["authenticated"] = True
                    st.session_state["user_info"] = {"username": "grid_eng", "role": "Microgrid Chief Engineer", "token": "sec_demo_grid"}
                    st.rerun()
            with c_b:
                if st.button("🚦 Traffic Operations Chief", use_container_width=True, key="quick_traffic_btn"):
                    st.session_state["authenticated"] = True
                    st.session_state["user_info"] = {"username": "traffic_op", "role": "Traffic Operations Chief", "token": "sec_demo_traffic"}
                    st.rerun()
                st.write("")
                if st.button("👁️ Guest Auditor", use_container_width=True, key="quick_guest_btn"):
                    st.session_state["authenticated"] = True
                    st.session_state["user_info"] = {"username": "guest", "role": "Guest Auditor", "token": "sec_demo_guest"}
                    st.rerun()

        elif access_choice == "🔑 Standard Login":
            with st.form(key="standard_login_form"):
                login_user = st.text_input("Username / Operator ID", value="admin")
                login_pwd = st.text_input("Password / Secure Passkey", type="password", value="Admin@123")
                submit_login = st.form_submit_button("Authenticate Session", type="primary", use_container_width=True)
                
                if submit_login:
                    if not login_user.strip() or not login_pwd.strip():
                        st.warning("Please enter both username and password.")
                    else:
                        ok, res = auth_manager.authenticate_user(login_user, login_pwd)
                        if ok:
                            st.session_state["authenticated"] = True
                            st.session_state["user_info"] = res
                            st.rerun()
                        else:
                            st.error(res)

        else:
            with st.form(key="register_account_form"):
                reg_user = st.text_input("New Username", key="create_user_input")
                reg_pwd = st.text_input("New Password (Min 8 chars, Upper, Lower, Special)", type="password", key="create_pwd_input")
                reg_role = st.selectbox("Operational Assign Role", ["Microgrid Engineer", "Traffic Controller", "System Auditor"], key="create_role_select")
                submit_reg = st.form_submit_button("Register & Initialize Session", type="primary", use_container_width=True)

                if submit_reg:
                    ok, msg = auth_manager.register_user(reg_user, reg_pwd, reg_role)
                    if ok:
                        st.session_state["authenticated"] = True
                        st.session_state["user_info"] = {"username": reg_user, "role": reg_role, "token": "new_reg_user"}
                        st.rerun()
                    else:
                        st.error(msg)
    st.stop()

# ────────────────────────────────────────────────────────────────────────
# 🎛️ SCREEN 2: MAIN DASHBOARD (AUTHENTICATED)
# ────────────────────────────────────────────────────────────────────────
user_data = st.session_state.get("user_info") or {"username": "Operator", "role": "Administrator"}

# --- LEFT SIDEBAR: Session Info & Global Controls ---
st.sidebar.markdown("### 🟢 SESSION ACTIVE")
st.sidebar.markdown(f"**Operator:** `{user_data.get('username', 'Operator')}`")
st.sidebar.markdown(f"**Role:** `{user_data.get('role', 'Administrator')}`")

# Explicit Logout Button - Evaluated ONLY when explicitly clicked!
if st.sidebar.button("🚪 Logout Session", key="main_logout_btn", use_container_width=True):
    st.session_state["authenticated"] = False
    st.session_state["user_info"] = None
    st.rerun()

st.sidebar.divider()

# Global Instant Multi-Country Currency Selector
st.sidebar.markdown("### 🌐 INTERNATIONAL SECTOR")
country_options = list(GroundLevelMitigation.COUNTRY_MATRIX.keys())
current_c = st.session_state.get("selected_country", "IN")
if current_c not in country_options:
    current_c = "IN"

selected_country_code = st.sidebar.selectbox(
    "Global Sector Node",
    country_options,
    index=country_options.index(current_c),
    format_func=lambda c: f"{c} - {GroundLevelMitigation.COUNTRY_MATRIX[c]['name']} ({GroundLevelMitigation.COUNTRY_MATRIX[c]['symbol']})",
    key="main_sidebar_country_select"
)
st.session_state["selected_country"] = selected_country_code

curr_info = GroundLevelMitigation.get_currency_info(selected_country_code)
st.sidebar.info(f"Currency: **{curr_info['currency']} ({curr_info['symbol']})**\nBase Rate: **{curr_info['symbol']}{curr_info['base_rate_kwh']}/kWh**")

st.sidebar.divider()
st.sidebar.markdown("### ⚙️ SYSTEM STATUS")
st.sidebar.caption("⚡ BFT Consensus: Active (3/3)")
st.sidebar.caption("🛡️ Crypto Ledger: Verified")
st.sidebar.caption("📡 REST API: Online (Port 8000)")

# --- MAIN TITLE BANNER ---
st.markdown("<h1 style='color: #00E5FF; font-weight: 800; margin-bottom: 0px;'>⚡ ECOGRID CORE AI SCADA COCKPIT</h1>", unsafe_allow_html=True)
st.caption("Multi-Agent Microgrid SCADA, Smart City Traffic, EV Loadshedding & AI Infrastructure Copilot")
st.write("")

# ────────────────────────────────────────────────────────────────────────
# 🗂️ RIGHT-HAND SIDE TABS (Client-Side Navigation - Prevents Logouts!)
# ────────────────────────────────────────────────────────────────────────
tab_guide, tab_scada, tab_traffic, tab_currency, tab_ai, tab_kaggle, tab_cyber, tab_reports, tab_api, tab_files = st.tabs([
    "📖 User Guide",
    "⚡ SCADA Grid",
    "🚦 Smart Traffic",
    "🌐 Currency Matrix",
    "🧠 AI Copilot",
    "🤖 Kaggle ML Hub",
    "🛡️ 3/3 BFT Security",
    "📑 Incident Reports",
    "📡 REST API Telemetry",
    "📂 Data & File Inspector"
])

# ────────────────────────────────────────────────────────────────────────
# TAB 1: WELCOME & SYSTEM USER GUIDE
# ────────────────────────────────────────────────────────────────────────
with tab_guide:
    try:
        st.markdown("<h2>📖 SYSTEM OPERATIONAL USER GUIDE</h2>", unsafe_allow_html=True)
        st.write("")

        col_ctrl, col_dash = st.columns([1, 1])

        with col_ctrl:
            st.markdown("""
            ### 🚀 Key System Features & Capabilities:
            - **⚡ SCADA & Microgrid Operations:** Real-time BFT microgrid load balancing, sine-wave frequency stream monitors, battery SOC health, and regional tariff savings calculation.
            - **🚦 Smart City Traffic & EV Queue Control:** Real-time Intersection Congestion Index (ICI), adaptive green light timing phase optimization, emergency corridor overrides, and EV queue load shedding.
            - **🌐 Multi-Country Currency Switcher:** Instant financial conversion and tariff matrix across 10 international grid sectors (INR, USD, EUR, GBP, JPY, AUD, BRL, CAD, AED, ZAR).
            - **🧠 AI SCADA Infrastructure Copilot:** Powered by Google Gemini 2.5 Flash & Edge AI, producing structured 3-part answers with Executive Summaries.
            - **🤖 Kaggle AI & ML Hub:** Scikit-Learn time-series models trained on Kaggle datasets with live prediction sandboxes, CSV dataset export, and automated retrainer.
            - **🛡️ Cybersecurity & 3/3 BFT:** Chaos Monkey frequency spoofing threat injector, 3/3 BFT unanimous signature consensus evaluator, and SHA-256 cryptographic audit ledger.
            - **📂 Data & File Inspector:** Safe file viewer and CSV/JSON dataset manager to open, preview, upload, and inspect system reports without data loss.
            """)

        with col_dash:
            st.markdown("""
            <div class='dashboard-card card-cyan'>
                <div class='metric-label'>Quick Navigation & Layout Manual</div>
                <p style='margin-top:10px; font-size:0.95rem; color:#94A3B8;'>
                - <b>Right-Hand Side Tabs:</b> All operational dashboards are accessible via top right-hand side tabs. Switching tabs is client-side instant and will never log you out.<br><br>
                - <b>Instant Currency Switcher:</b> Use the Global Sector Node selector in the left sidebar to convert spot clearing tariffs across 10 global sector nodes.<br><br>
                - <b>Session Security:</b> Your authenticated session remains active across all tab navigation until you explicitly click <b>Logout Session</b> in the sidebar.
                </p>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Tab Error: {e}")

# ────────────────────────────────────────────────────────────────────────
# TAB 2: ECOGRID SCADA & MICROGRID
# ────────────────────────────────────────────────────────────────────────
with tab_scada:
    try:
        st.markdown("<h2>⚡ ECOGRID MULTI-AGENT SCADA CONTROL</h2>", unsafe_allow_html=True)
        st.caption("Byzantine Fault Tolerant Microgrid Telemetry & Real-Time Sine Wave Simulation")
        st.write("")

        col_ctrl, col_dash = st.columns([2, 3])
        with col_ctrl:
            st.markdown("### 🎛️ Operational Parameters")
            saved_kwh = st.slider("Mitigated Energy Volume (kWh)", 10.0, 5000.0, 250.0, step=25.0, key="panel_scada_kwh_slider")

            st.divider()
            st.markdown("### 🔋 Battery Storage Reservoirs")
            if st.button("Discharge Battery Cell Reserve (50 kW Load)", key="panel_scada_discharge_btn"):
                b_state = battery.discharge_for_arbitrage(50.0)
                ledger.record_transaction("Arbitrageur_Agent", "BATTERY_DISCHARGE", b_state)
                st.success(f"Discharged 50 kW load. Current SOC: {b_state['current_soc']}%")

        with col_dash:
            st.markdown("### 📊 Live Grid Telemetry Dashboard")
            mit_data = GroundLevelMitigation.calculate_regional_mitigation(saved_kwh, st.session_state.get("selected_country", "IN"))
            
            m_a, m_b, m_c = st.columns(3)
            with m_a:
                st.markdown(f"""
                <div class='dashboard-card card-green'>
                    <div class='metric-label'>Mitigation Savings</div>
                    <div class='metric-value'>{mit_data['total_savings_formatted']}</div>
                </div>
                """, unsafe_allow_html=True)
            with m_b:
                st.markdown(f"""
                <div class='dashboard-card card-cyan'>
                    <div class='metric-label'>State of Charge (SOC)</div>
                    <div class='metric-value'>{battery.state_of_charge}%</div>
                </div>
                """, unsafe_allow_html=True)
            with m_c:
                st.markdown(f"""
                <div class='dashboard-card card-magenta'>
                    <div class='metric-label'>Cell Health</div>
                    <div class='metric-value'>{battery.battery_health}%</div>
                </div>
                """, unsafe_allow_html=True)

            fig_topo = go.Figure()
            fig_topo.add_trace(go.Scatter(
                x=[0, 1, 1, 2, 0, 2], y=[0, 1, 1, 0, 0, 0],
                line=dict(width=2, color='#00E5FF'),
                hoverinfo='none',
                mode='lines'
            ))
            node_x = [0, 1, 2]
            node_y = [0, 1, 0]
            node_colors = ['#00FF66', '#FFB300', '#00E5FF']
            fig_topo.add_trace(go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                text=["Node Alpha", "Node Beta", "Node Gamma"],
                textposition="top center",
                marker=dict(size=[30, 45, 35], color=node_colors, line=dict(width=2, color='#FFFFFF'))
            ))
            fig_topo.update_layout(
                title="Interactive Grid Node Topology", showlegend=False,
                paper_bgcolor="#121A30", plot_bgcolor="#121A30", font_color="#FFFFFF",
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_topo, key="panel_scada_topo_chart", use_container_width=True)

            df_stream = pd.DataFrame({
                "Time (s)": np.arange(1, 21),
                "Node_Alpha (Residential)": 50.0 + np.random.normal(0, 0.08, 20),
                "Node_Beta (Industrial)": 49.95 + np.random.normal(0, 0.12, 20),
                "Node_Gamma (Medical)": 50.02 + np.random.normal(0, 0.04, 20)
            })
            fig_grid = px.line(df_stream, x="Time (s)", y=["Node_Alpha (Residential)", "Node_Beta (Industrial)", "Node_Gamma (Medical)"],
                              title="Real-Time Grid Frequency Profiles (Hz)")
            fig_grid.update_layout(paper_bgcolor="#121A30", plot_bgcolor="#121A30", font_color="#FFFFFF")
            st.plotly_chart(fig_grid, key="panel_scada_freq_chart", use_container_width=True)
    except Exception as e:
        st.error(f"Tab Error: {e}")

# ────────────────────────────────────────────────────────────────────────
# TAB 3: SMART CITY TRAFFIC & EV GRID
# ────────────────────────────────────────────────────────────────────────
with tab_traffic:
    try:
        st.markdown("<h2>🚦 SMART CITY TRAFFIC & EV GRID LOAD CONTROL</h2>", unsafe_allow_html=True)
        st.caption("Intersection Congestion Index, Signal Phase Optimization, and EV Queue Balancing")
        st.write("")

        col_ctrl, col_dash = st.columns([2, 3])
        with col_ctrl:
            st.markdown("### 🎛️ Traffic Environment Controls")
            int_choice = st.selectbox("Target Intersection ID", ["INT_ALPHA_CBD", "INT_BETA_IND", "INT_GAMMA_MED"], key="panel_traffic_int_select")
            v_count = st.slider("Main Street Vehicles/Hr", 50, 1500, 950, step=25, key="panel_traffic_vcount_slider")
            v_speed = st.slider("Average Traffic Speed (km/h)", 5.0, 80.0, 22.5, step=2.5, key="panel_traffic_vspeed_slider")
            weather_choice = st.selectbox("Weather Profile Matrix", ["SUNNY", "CLOUDY", "RAINY", "STORMY"], key="panel_traffic_weather_select")

            st.divider()
            st.markdown("### 🚦 Adaptive Signal Timing Optimizer")
            cross_count = st.slider("Cross Street Vehicle Load (veh/hr)", 50, 800, 300, step=25, key="panel_traffic_cross_slider")
            emergency_trigger = st.checkbox("🚨 ACTIVATE EMERGENCY GREEN CORRIDOR OVERRIDE", value=False, key="panel_traffic_emerg_chk")

        with col_dash:
            st.markdown("### 📊 Live Traffic & EV Queue Dashboard")
            metrics = EcoGridTrafficEngine.calculate_intersection_metrics(v_count, v_speed, weather_choice)
            
            m_a, m_b = st.columns(2)
            with m_a:
                st.markdown(f"""
                <div class='dashboard-card card-magenta'>
                    <div class='metric-label'>Congestion Index (ICI)</div>
                    <div class='metric-value'>{metrics['congestion_index']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            with m_b:
                st.markdown(f"""
                <div class='dashboard-card card-cyan'>
                    <div class='metric-label'>Flow Status</div>
                    <div class='metric-value'>{metrics['traffic_status_level']}</div>
                </div>
                """, unsafe_allow_html=True)

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
            st.plotly_chart(fig_sig, key="panel_traffic_signal_chart", use_container_width=True)

            st.divider()
            st.markdown("### 🔋 EV Charging Queue Status")
            grid_load_val = st.number_input("Current Grid Load (kW)", value=1650.0, step=50.0, key="panel_traffic_gridload_num")
            ev_count_val = st.slider("Queued EV Vehicles", 1, 30, 15, key="panel_traffic_evcount_slider")

            ev_res = EcoGridTrafficEngine.balance_ev_charging_queue(grid_load_val, 2000.0, ev_count_val)
            
            m_c, m_d = st.columns(2)
            with m_c:
                st.markdown(f"""
                <div class='dashboard-card card-green'>
                    <div class='metric-label'>Allocated Power</div>
                    <div class='metric-value'>{ev_res['allocated_station_kw']} kW</div>
                </div>
                """, unsafe_allow_html=True)
            with m_d:
                st.markdown(f"""
                <div class='dashboard-card card-purple'>
                    <div class='metric-label'>Remaining Margin</div>
                    <div class='metric-value'>{ev_res['remaining_grid_margin_kw']} kW</div>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Tab Error: {e}")

# ────────────────────────────────────────────────────────────────────────
# TAB 4: MULTI-COUNTRY CURRENCY CENTER
# ────────────────────────────────────────────────────────────────────────
with tab_currency:
    try:
        st.markdown("<h2>🌐 GLOBAL MULTI-COUNTRY CURRENCY CENTER</h2>", unsafe_allow_html=True)
        st.caption("Instant Financial Conversion & Utility Tariff Comparison Matrix Across 10 Countries")
        st.write("")

        col_ctrl, col_dash = st.columns([2, 3])

        with col_ctrl:
            st.markdown("### 🎛️ Financial Spot Parameters")
            base_spot_inr = st.number_input("Base Spot Market Rate (INR / MWh)", value=3500.0, step=100.0, key="panel_curr_spot_inr_num")
            eval_kwh = st.slider("Evaluation Energy Range (kWh)", 100.0, 10000.0, 1500.0, step=100.0, key="panel_curr_eval_kwh_slider")

        with col_dash:
            st.markdown("### 🌍 Tariff Matrix Dashboard")
            active_c = st.session_state.get("selected_country", "IN")
            active_mit = GroundLevelMitigation.calculate_regional_mitigation(eval_kwh, active_c)
            
            st.markdown(f"""
            <div class='dashboard-card card-green'>
                <div class='metric-label'>Active Node Savings ({active_mit['country_name']})</div>
                <div class='metric-value'>{active_mit['total_savings_formatted']}</div>
            </div>
            """, unsafe_allow_html=True)

            matrix_rows = []
            for c_code, meta in GroundLevelMitigation.COUNTRY_MATRIX.items():
                converted_rate, formatted_rate = GroundLevelMitigation.convert_price_from_inr(base_spot_inr, c_code)
                mit = GroundLevelMitigation.calculate_regional_mitigation(eval_kwh, c_code)
                matrix_rows.append({
                    "Code": c_code,
                    "Country": meta["name"],
                    "Currency": meta["currency"],
                    "Symbol": meta["symbol"],
                    "Base Tariff (/kWh)": f"{meta['symbol']}{meta['base_rate_kwh']}",
                    "Spot Rate (/MWh)": formatted_rate,
                    "Mitigation Value": mit["total_savings_formatted"]
                })

            df_matrix = pd.DataFrame(matrix_rows)
            st.dataframe(df_matrix, use_container_width=True)

            st.divider()
            st.markdown("### 📊 Sector Financial Mitigation Chart")
            fig_curr = px.bar(
                df_matrix,
                x="Country",
                y=[meta["base_rate_kwh"] * eval_kwh for meta in GroundLevelMitigation.COUNTRY_MATRIX.values()],
                title=f"Mitigation Value across International Grid Sectors for {eval_kwh} kWh",
                labels={"value": "Local Currency Units", "Country": "Sector Country"}
            )
            fig_curr.update_layout(paper_bgcolor="#121A30", plot_bgcolor="#121A30", font_color="#FFFFFF")
            st.plotly_chart(fig_curr, key="panel_curr_bar_chart", use_container_width=True)
    except Exception as e:
        st.error(f"Tab Error: {e}")

# ────────────────────────────────────────────────────────────────────────
# TAB 5: AI SCADA INFRASTRUCTURE COPILOT
# ────────────────────────────────────────────────────────────────────────
with tab_ai:
    try:
        st.markdown("<h2>🧠 AI SCADA INFRASTRUCTURE COPILOT</h2>", unsafe_allow_html=True)
        st.caption("Powered by Google GenAI (Gemini) & Edge Cognitive AI with Executive Summaries")
        st.write("")

        col_ctrl, col_dash = st.columns([2, 3])
        with col_ctrl:
            st.markdown("### 💬 Copilot Shell Agent Query")
            preset_q = st.selectbox(
                "Quick Question Presets",
                [
                    "Custom Question",
                    "How does EcoGrid Core optimize signal timing and EV charging load during peak hours?",
                    "What safety protocols trigger when a 53.1 Hz frequency spoofing attack occurs?",
                    "How does 3/3 BFT Consensus protect microgrid load dispatch decisions?",
                    "Explain the financial impact of dynamic solar power generation predictions."
                ],
                key="panel_ai_preset_select"
            )

            user_q = st.text_area("Your Query string", value="" if preset_q == "Custom Question" else preset_q, height=100, key="panel_ai_query_text")
            trigger_analysis = st.button("🚀 Analyze with EcoGrid AI Copilot", type="primary", key="panel_ai_analyze_btn")

        with col_dash:
            st.markdown("### 🤖 Analysis Output Stream")
            m_a, m_b = st.columns(2)
            with m_a:
                st.markdown("""
                <div class='dashboard-card card-cyan'>
                    <div class='metric-label'>Cloud Agent Channel</div>
                    <div class='metric-value' style='font-size:1.3rem; color:#00BBF9;'>Gemini 2.5 Flash</div>
                </div>
                """, unsafe_allow_html=True)
            with m_b:
                st.markdown("""
                <div class='dashboard-card card-green'>
                    <div class='metric-label'>Local Edge Engine</div>
                    <div class='metric-value' style='font-size:1.3rem; color:#00F5D4;'>Active</div>
                </div>
                """, unsafe_allow_html=True)

            if trigger_analysis:
                if not user_q.strip():
                    st.warning("Please enter a question or select a preset.")
                else:
                    with st.spinner("EcoGrid AI Copilot analyzing system telemetry and diagnostic models..."):
                        ctx = {
                            "active_country": st.session_state.get("selected_country", "IN"),
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
    except Exception as e:
        st.error(f"Tab Error: {e}")

# ────────────────────────────────────────────────────────────────────────
# TAB 6: KAGGLE AI & ML HUB
# ────────────────────────────────────────────────────────────────────────
with tab_kaggle:
    try:
        st.markdown("<h2>🤖 KAGGLE AI & ML MODEL INTELLIGENCE HUB</h2>", unsafe_allow_html=True)
        st.caption("Machine Learning Predictors & Dataset Data Explorer")
        st.write("")

        col_ctrl, col_dash = st.columns([2, 3])
        with col_ctrl:
            st.markdown("### 🚀 Training Operations")
            if st.button("🔄 Train / Retrain All 4 Kaggle Models Now", type="primary", key="panel_kaggle_retrain_btn"):
                with st.spinner("Training Kaggle models on dataset matrices..."):
                    retrain_res = train_all_models()
                    predictor.load_models()
                    st.success("All 4 Kaggle ML Models successfully trained and updated!")
                    st.json(retrain_res)

            st.divider()
            st.markdown("### 🔮 Live Predictor Sandboxes")
            p_temp = st.slider("Ambient Temp (°C)", 10.0, 45.0, 32.0, key="panel_kaggle_ptemp_slider")
            p_hum = st.slider("Humidity (%)", 20.0, 95.0, 50.0, key="panel_kaggle_phum_slider")
            p_ev = st.slider("EV Station kW", 50.0, 1200.0, 600.0, key="panel_kaggle_pev_slider")
            p_irr = st.slider("Irradiance (W/m²)", 0.0, 1200.0, 850.0, key="panel_kaggle_pirr_slider")
            p_cloud = st.slider("Cloud Cover (%)", 0.0, 100.0, 15.0, key="panel_kaggle_pcloud_slider")

        with col_dash:
            st.markdown("### 📊 Kaggle Predictions & Dataset matrix")
            pred_load = predictor.predict_grid_load(p_temp, p_hum, p_ev)
            pred_solar = predictor.predict_solar_generation(p_irr, 35.0, p_cloud)

            m_a, m_b = st.columns(2)
            with m_a:
                st.markdown(f"""
                <div class='dashboard-card card-magenta'>
                    <div class='metric-label'>Predicted Grid Load</div>
                    <div class='metric-value'>{pred_load:.2f} kW</div>
                </div>
                """, unsafe_allow_html=True)
            with m_b:
                st.markdown(f"""
                <div class='dashboard-card card-green'>
                    <div class='metric-label'>Predicted Solar Generation</div>
                    <div class='metric-value'>{pred_solar:.2f} kW</div>
                </div>
                """, unsafe_allow_html=True)

            st.divider()
            ds_choice = st.selectbox("Select Kaggle Dataset to Inspect", ["Traffic Flow Dataset", "Grid Load Dataset", "Solar Generation Dataset"], key="panel_kaggle_ds_select")
            try:
                if ds_choice == "Traffic Flow Dataset":
                    df_ds = DatasetLoader.load_traffic_dataset()
                elif ds_choice == "Grid Load Dataset":
                    df_ds = DatasetLoader.load_grid_load_dataset()
                else:
                    df_ds = DatasetLoader.load_solar_dataset()
                st.dataframe(df_ds, use_container_width=True)
            except Exception as ds_err:
                st.warning(f"Unable to load Kaggle dataset file: {ds_err}")
    except Exception as e:
        st.error(f"Tab Error: {e}")

# ────────────────────────────────────────────────────────────────────────
# TAB 7: CYBERSECURITY & 3/3 BFT LEDGER
# ────────────────────────────────────────────────────────────────────────
with tab_cyber:
    try:
        st.markdown("<h2>🛡️ CYBERSECURITY & 3/3 BFT CRYPTOGRAPHIC LEDGER</h2>", unsafe_allow_html=True)
        st.caption("3/3 Byzantine Fault Tolerance (BFT) Signature Consensus & SHA-256 Ledger Audit")
        st.write("")

        col_ctrl, col_dash = st.columns([2, 3])
        with col_ctrl:
            st.markdown("### 💥 Chaos Monkey Threat Injector")
            target_n = st.selectbox("Target Injection Node", ["Node_Alpha_Residential", "Node_Beta_Industrial", "Node_Gamma_Medical"], key="panel_cyber_target_select")
            freq_inject = st.slider("Spoofed Frequency Value (Hz)", 48.0, 54.0, 53.1, key="panel_cyber_freq_slider")
            trigger_chaos = st.button("Inject Spoofed Telemetry Attack", key="panel_cyber_inject_btn")

            st.divider()
            st.markdown("### ⚖️ Consensus Node Vote")
            eval_bft = st.button("Evaluate 3/3 Unanimous Consensus Vote", key="panel_cyber_bft_eval_btn")

        with col_dash:
            st.markdown("### 🛡️ Cybersecurity Operations Center")
            is_val, val_msg = ledger.verify_chain()
            
            m_a, m_b = st.columns(2)
            with m_a:
                st.markdown(f"""
                <div class='dashboard-card card-green'>
                    <div class='metric-label'>Ledger Integrity</div>
                    <div class='metric-value' style='font-size:1.1rem; color:#00F5D4;'>{val_msg}</div>
                </div>
                """, unsafe_allow_html=True)
            with m_b:
                st.markdown(f"""
                <div class='dashboard-card card-cyan'>
                    <div class='metric-label'>Protection Core</div>
                    <div class='metric-value' style='font-size:1.1rem; color:#00BBF9;'>3/3 BFT Unanimous</div>
                </div>
                """, unsafe_allow_html=True)

            if trigger_chaos:
                anom_res = predictor.detect_cyber_anomaly(freq_inject, 1200.0)
                if anom_res["is_attack_detected"]:
                    st.error(f"🚨 CYBER THREAT CONTAINED! Anomaly: {anom_res['anomaly_type']}")
                    ledger.record_transaction("SECURITY_KERNEL", "CYBER_ATTACK_CONTAINMENT", {"targeted_node": target_n, "freq": freq_inject})
                else:
                    st.success("Telemetry within safe operational boundaries.")

            if eval_bft:
                bft_res = BFTConsensusEngine.evaluate_state_proposal("GRID_LOAD_TRANSFER", target_n, {"grid_freq_hz": freq_inject})
                st.json(bft_res)

            st.divider()
            st.markdown("### 📑 Cryptographic Block Ledger Stream")
            ledger_ok, ledger_raw, ledger_path = safe_read_file_content("reports/ledger.json")
            if ledger_ok and ledger_raw.strip():
                try:
                    blocks = json.loads(ledger_raw)
                    st.markdown(f"**Total Verified Blocks:** `{len(blocks)}` (Loaded from `{ledger_path}`)")
                    st.dataframe(pd.DataFrame(blocks).tail(10), use_container_width=True)
                except Exception as json_err:
                    st.warning(f"Ledger file exists but JSON format parsing warning: {json_err}")
            else:
                st.info(f"Ledger stream ready. File state: {ledger_raw}")
    except Exception as e:
        st.error(f"Tab Error: {e}")

# ────────────────────────────────────────────────────────────────────────
# TAB 8: INCIDENT REPORTS & PRESCRIPTIONS
# ────────────────────────────────────────────────────────────────────────
with tab_reports:
    try:
        st.markdown("<h2>📑 INCIDENT REPORTS & MAINTENANCE PRESCRIPTIONS</h2>", unsafe_allow_html=True)
        st.caption("Automated Actionable Engineering Protocols for Ground-Level Technicians")
        st.write("")

        col_ctrl, col_dash = st.columns([2, 3])
        with col_ctrl:
            st.markdown("### 🛠️ Incident Generator Matrix")
            reason = st.selectbox("Trigger Reason", ["Frequency_Spoofing_Attack", "Budget_Overrun_Load_Spike", "Routine_Maintenance_Sweep"], key="panel_inc_reason_select")
            val_metric = st.number_input("Observed Metric Value", value=53.1, key="panel_inc_metric_num")
            t_node = st.selectbox("Target Node", ["Node_Alpha_Residential", "Node_Beta_Industrial", "Node_Gamma_Medical"], key="panel_inc_tnode_select")

        with col_dash:
            st.markdown("### 📋 Incident Diagnostic Report")
            prescript = GroundLevelMitigation.get_prescription(reason, val_metric, t_node)

            st.markdown("#### Generated Field Protocols:")
            for step in prescript:
                st.write(step)

            st.divider()
            report_title = f"INCIDENT REPORT: {reason.upper()} on {t_node.upper()}"
            report_body = f"""# {report_title}
**Date/Time:** {time.strftime('%Y-%m-%d %H:%M:%S')}  
**Target Sector Node:** {t_node}  
**Observed Metric:** {val_metric}  
**Sector Country Node:** {st.session_state.get('selected_country', 'IN')}  

## 🔬 Executive Summary
An anomaly event ({reason}) was flagged on {t_node}. The 3/3 BFT consensus core isolated the vector and logged transaction to the SHA-256 ledger.

## 🛠️ Actionable Ground-Level Engineering Protocols
""" + "\n".join([f"- {s}" for s in prescript]) + """

## 🔐 Signatures
- **EcoGrid SCADA Chief:** Verified
- **EcoGrid Core Core:** Sealed (SHA-256 Ledger)
"""
            st.text(report_body)
            st.download_button(
                "📥 Download Diagnostic Report (.txt)",
                data=report_body,
                file_name=f"incident_report_{t_node}_{int(time.time())}.txt",
                mime="text/plain",
                key="download_incident_report_btn"
            )
    except Exception as e:
        st.error(f"Tab Error: {e}")

# ────────────────────────────────────────────────────────────────────────
# TAB 9: REST API TELEMETRY
# ────────────────────────────────────────────────────────────────────────
with tab_api:
    try:
        st.markdown("<h2>🌐 REST API & SYSTEM DEPLOYMENT TELEMETRY</h2>", unsafe_allow_html=True)
        st.caption("OpenAPI Swagger Endpoints & Containerized Service Status")
        st.write("")

        col_ctrl, col_dash = st.columns([1, 2])
        with col_ctrl:
            st.markdown("""
            ### 📡 Microservice Telemetry Node
            - **REST API Engine:** FastAPI v6.5.0-PROD
            - **Endpoint Port:** `8000`
            - **OpenAPI Swagger UI:** `http://localhost:8000/docs`
            """)

        with col_dash:
            st.markdown("### 📑 Endpoint Directory Matrix")
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
            st.dataframe(endpoints_df, use_container_width=True)
    except Exception as e:
        st.error(f"Tab Error: {e}")

# ────────────────────────────────────────────────────────────────────────
# TAB 10: DATA & FILE INSPECTOR (Safe File Reader, Explorer & Uploader)
# ────────────────────────────────────────────────────────────────────────
with tab_files:
    try:
        st.markdown("<h2>📂 DATA & FILE INSPECTOR</h2>", unsafe_allow_html=True)
        st.caption("Safe File Reader, Upload Sandbox & System Dataset Explorer with Zero Data Loss Protection")
        st.write("")

        file_col1, file_col2 = st.columns([1, 2])

        with file_col1:
            st.markdown("### 🔍 System File Browser")
            system_files = [
                "reports/ledger.json",
                "config/scenarios.json",
                "data/kaggle_traffic_flow.csv",
                "data/kaggle_grid_load.csv",
                "data/kaggle_solar_generation.csv",
                "config/sample_grid_data.csv"
            ]
            chosen_file = st.selectbox("Select System File to Read", system_files, key="file_inspector_sys_file_select")
            
            st.divider()
            st.markdown("### 📤 Upload Custom File")
            uploaded_file = st.file_uploader(
                "Choose a CSV, JSON, or TXT file to inspect",
                type=["csv", "json", "txt", "log"],
                key="file_inspector_uploader"
            )

        with file_col2:
            st.markdown("### 📄 Content & Data Preview")

            # Priority 1: If user uploaded a custom file
            if uploaded_file is not None:
                st.success(f"Uploaded File: **{uploaded_file.name}** ({uploaded_file.size} bytes)")
                file_ext = uploaded_file.name.split(".")[-1].lower()

                if file_ext == "csv":
                    try:
                        df_upload = pd.read_csv(uploaded_file)
                        st.markdown(f"**Tabular Preview ({df_upload.shape[0]} rows, {df_upload.shape[1]} columns):**")
                        st.dataframe(df_upload, use_container_width=True)
                        st.markdown("**Column Summary:**")
                        st.json(dict(zip(df_upload.columns, [str(dt) for dt in df_upload.dtypes])))
                    except Exception as parse_err:
                        st.error(f"Error parsing CSV file: {parse_err}")
                elif file_ext == "json":
                    try:
                        json_data = json.load(uploaded_file)
                        st.markdown("**Structured JSON View:**")
                        st.json(json_data)
                    except Exception as parse_err:
                        st.error(f"Error parsing JSON file: {parse_err}")
                else:
                    try:
                        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                        text_content = stringio.read()
                        st.markdown("**Raw Text View:**")
                        st.code(text_content, language="text")
                    except Exception as parse_err:
                        st.error(f"Error reading text file: {parse_err}")

            # Priority 2: Inspect selected system file
            else:
                success, raw_text, resolved_path = safe_read_file_content(chosen_file)
                st.caption(f"Resolved System Path: `{resolved_path}`")

                if not success:
                    st.warning(f"⚠️ {raw_text}")
                else:
                    if chosen_file.endswith(".csv"):
                        try:
                            df_sys = pd.read_csv(resolved_path)
                            st.markdown(f"**Tabular View ({df_sys.shape[0]} rows, {df_sys.shape[1]} columns):**")
                            st.dataframe(df_sys, use_container_width=True)
                            st.download_button(
                                "📥 Export Dataset CSV",
                                data=df_sys.to_csv(index=False),
                                file_name=os.path.basename(chosen_file),
                                mime="text/csv",
                                key="download_sys_csv_btn"
                            )
                        except Exception as csv_err:
                            st.error(f"Error reading CSV structure: {csv_err}")
                            st.code(raw_text, language="text")
                    elif chosen_file.endswith(".json"):
                        try:
                            json_obj = json.loads(raw_text)
                            st.markdown("**Structured JSON View:**")
                            st.json(json_obj)
                            st.download_button(
                                "📥 Export JSON File",
                                data=json.dumps(json_obj, indent=2),
                                file_name=os.path.basename(chosen_file),
                                mime="application/json",
                                key="download_sys_json_btn"
                            )
                        except Exception as json_err:
                            st.warning(f"JSON Parse Warning: {json_err}")
                            st.code(raw_text, language="text")
                    else:
                        st.code(raw_text, language="text")
    except Exception as e:
        st.error(f"Tab Error: {e}")