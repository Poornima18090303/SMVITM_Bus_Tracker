"""
dashboard.py
------------
Streamlit Web Application for the AI-Based College Bus ETA Prediction System.
Designed for SMVITM (Shri Madhwa Vadiraja Institute of Technology and Management).
"""

import os
import streamlit as st
import pandas as pd
from datetime import datetime

import routes
import utils

# Page Configuration
st.set_page_config(
    page_title="SMVITM College Bus ETA Predictor",
    page_icon="🚍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Glassmorphic Aesthetic
st.markdown("""
<style>
    /* Main Theme Variables */
    :root {
        --primary-bg: #0e1117;
        --card-bg: rgba(22, 27, 34, 0.75);
        --accent-green: #10b981;
        --accent-blue: #3b82f6;
        --accent-orange: #f59e0b;
        --accent-red: #ef4444;
        --text-main: #f3f4f6;
    }

    /* Streamlit Container Enhancements */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #0d1322 100%);
        color: var(--text-main);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Glassmorphic Cards applied to Streamlit native border containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(30, 41, 59, 0.45) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 20px 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(59, 130, 246, 0.3) !important;
    }

    /* Header Styling */
    .app-header {
        display: flex;
        align-items: center;
        gap: 20px;
        background: linear-gradient(90deg, rgba(30, 58, 138, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 20px 28px;
        margin-bottom: 25px;
    }

    .app-title {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .app-subtitle {
        font-size: 14px;
        color: #9ca3af;
        margin-top: 4px;
    }

    /* Trip Metric Cards */
    .metric-container {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .metric-container:hover {
        transform: translateY(-2px);
        border-color: rgba(59, 130, 246, 0.4);
    }

    .metric-label {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #9ca3af;
        margin-bottom: 6px;
        font-weight: 600;
    }

    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #38bdf8;
    }

    /* ETA Result Banners */
    .result-banner-success {
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.8) 0%, rgba(16, 185, 129, 0.2) 100%);
        border: 1px solid #10b981;
        border-radius: 16px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.2);
    }

    .result-banner-warning {
        background: linear-gradient(135deg, rgba(127, 29, 29, 0.8) 0%, rgba(239, 68, 68, 0.2) 100%);
        border: 1px solid #ef4444;
        border-radius: 16px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.2);
    }

    .banner-title {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    /* Route Stepper Timeline */
    .timeline-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 25px;
        position: relative;
        padding: 20px 10px;
    }

    .timeline-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        z-index: 2;
        position: relative;
    }

    .step-badge {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 14px;
        background: #1e293b;
        border: 2px solid #475569;
        color: #94a3b8;
    }

    .step-badge.bus-current {
        background: #2563eb;
        border-color: #60a5fa;
        color: #ffffff;
        box-shadow: 0 0 15px #3b82f6;
        animation: pulse 2s infinite;
    }

    .step-badge.user-stop {
        background: #059669;
        border-color: #34d399;
        color: #ffffff;
        box-shadow: 0 0 15px #10b981;
    }

    .step-label {
        font-size: 12px;
        font-weight: 600;
        margin-top: 8px;
        color: #cbd5e1;
        text-align: center;
    }

    .step-time {
        font-size: 11px;
        color: #64748b;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)


def load_bus_dataset():
    """Function to load the bus route timetable dataset from Excel."""
    return routes.ensure_dataset_exists()


def main():
    df = load_bus_dataset()

    # --- Header Section ---
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    
    col_h1, col_h2 = st.columns([1, 6])
    with col_h1:
        if os.path.exists(logo_path):
            st.image(logo_path, width=80)
        else:
            st.markdown("<h1 style='text-align: center;'>🚍</h1>", unsafe_allow_html=True)
    with col_h2:
        st.markdown("""
        <div>
            <h1 class='app-title'>🚍 Smart College Bus ETA & Tracking System</h1>
            <p class='app-subtitle'>Shri Madhwa Vadiraja Institute of Technology and Management (SMVITM), Bantakal</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Available Routes
    all_routes = routes.get_all_routes(df)

    # Initialize Session State
    if "selected_route" not in st.session_state:
        st.session_state.selected_route = "Route 3" if "Route 3" in all_routes else all_routes[0]

    # --- MAIN INTERFACE: Left & Right Columns ---
    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    # ================= LEFT SIDE: BUS DETAILS =================
    with col_left:
        st.markdown("### 🚍 Bus Details")
        with st.container(border=True):
            # 1. Select Bus Route
            selected_route = st.selectbox(
                "Select Bus (Route No.)",
                options=all_routes,
                index=all_routes.index(st.session_state.selected_route) if st.session_state.selected_route in all_routes else 0,
                key="route_selector"
            )
            st.session_state.selected_route = selected_route

            # Dynamic stops for the selected route
            route_stops = routes.get_stops_for_route(df, selected_route)

            # Default stop selections for Route 3 or dynamic defaults
            default_current_idx = 2 if len(route_stops) > 2 else 0  # e.g., Atradi
            default_my_stop_idx = 3 if len(route_stops) > 3 else len(route_stops) - 1  # e.g., Manipal

            # 2. Current Bus Location
            current_bus_location = st.selectbox(
                "Current Bus Location (Student inside the bus)",
                options=route_stops,
                index=default_current_idx,
                key=f"current_loc_{selected_route}"
            )

            # 3. My Bus Stop
            my_bus_stop = st.selectbox(
                "My Bus Stop (Your destination stop)",
                options=route_stops,
                index=default_my_stop_idx,
                key=f"my_stop_{selected_route}"
            )

    # ================= RIGHT SIDE: TRIP DETAILS =================
    with col_right:
        st.markdown("### ⏱ Trip Details")
        with st.container(border=True):
            # Calculate trip details dynamically
            current_stop_details = routes.get_stop_details(df, selected_route, current_bus_location)
            my_stop_details = routes.get_stop_details(df, selected_route, my_bus_stop)
            terminal_stop_details = routes.get_stop_details(df, selected_route, "SMVITM")

            # Current Live Clock Time (Defaulting to live time or morning college bus hours)
            live_now_str = datetime.now().strftime("%I:%M %p")

            # Calculate remaining distance
            cur_dist = float(current_stop_details.get("Distance_km", 0.0))
            my_dist = float(my_stop_details.get("Distance_km", 0.0))
            dist_remaining = max(0.0, round(my_dist - cur_dist, 1))

            # Metric Display Cards
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-label'>Current Time</div>
                    <div class='metric-value'>🕒 {live_now_str}</div>
                </div>
                """, unsafe_allow_html=True)

            with m_col2:
                st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-label'>Distance Remaining</div>
                    <div class='metric-value'>📍 {dist_remaining} km</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            st.markdown(f"**Route Selected**: `{selected_route}`")
            st.markdown(f"**Current Bus Location**: `{current_bus_location}`")
            st.markdown(f"**Your Stop**: `{my_bus_stop}`")
            st.markdown(f"📍 **Distance ({current_bus_location} → {my_bus_stop})**: `{dist_remaining} km`")

    # ================= BOTTOM SECTION: ACTION & ETA RESULT =================
    st.markdown("---")
    
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        predict_clicked = st.button("🔍 Predict ETA", use_container_width=True, type="primary")

    # Automatically compute ETA or when button clicked
    eta_result = utils.calculate_eta_details(df, selected_route, current_bus_location, my_bus_stop)

    if eta_result["status"] == "SUCCESS":
        st.markdown(f"""
        <div class='result-banner-success'>
            <div class='banner-title'>{eta_result['message']}</div>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-top: 15px;'>
                <div><strong>Current Bus Location:</strong> {eta_result['current_stop']}</div>
                <div><strong>Your Stop:</strong> {eta_result['my_stop']}</div>
                <div><strong>Expected Arrival:</strong> {eta_result['expected_arrival']}</div>
                <div><strong>Distance Remaining:</strong> {eta_result['distance_km']} km</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif eta_result["status"] == "CROSSED":
        st.markdown(f"""
        <div class='result-banner-warning'>
            <div class='banner-title' style='color: #f87171;'>{eta_result['message']}</div>
            <p>The bus passed <strong>{eta_result['my_stop']}</strong> at scheduled time <strong>{eta_result['my_scheduled_time_str']}</strong> and is currently at <strong>{eta_result['current_stop']}</strong> ({eta_result['current_time_str']}).</p>
        </div>
        """, unsafe_allow_html=True)

    elif eta_result["status"] == "ARRIVING_NOW":
        st.markdown(f"""
        <div class='result-banner-success'>
            <div class='banner-title'>{eta_result['message']}</div>
            <p>Please board the bus at <strong>{current_bus_location}</strong>. Scheduled departure: <strong>{eta_result['expected_arrival']}</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- VISUAL ROUTE TIMELINE STEPPER ---
    st.markdown("### 🗺 Route Timeline & Live Tracker")
    with st.container(border=True):
        route_full_df = df[df["Route"] == selected_route].reset_index(drop=True)
        
        # Render timeline steps
        cols = st.columns(len(route_full_df))
        for i, row in route_full_df.iterrows():
            stop_name = row["Stop"]
            time_str = utils.format_minutes_to_ampm(utils.parse_time_to_minutes(row["Time"]))

            badge_class = ""
            badge_symbol = str(i + 1)

            if stop_name == current_bus_location:
                badge_class = "bus-current"
                badge_symbol = "🚍"
            elif stop_name == my_bus_stop:
                badge_class = "user-stop"
                badge_symbol = "📍"

            with cols[i]:
                st.markdown(f"""
                <div class='timeline-step'>
                    <div class='step-badge {badge_class}'>{badge_symbol}</div>
                    <div class='step-label'>{stop_name}</div>
                    <div class='step-time'>{time_str}</div>
                </div>
                """, unsafe_allow_html=True)

    # --- SIMULATED GPS SECTION ---
    with st.expander("🛰️ Simulated GPS Geolocation Module (For Demonstration & Interview)"):
        st.markdown("""
        *This module demonstrates how live hardware GPS coordinates (Latitude & Longitude) received from the bus tracker device 
        are mapped to the nearest timetable bus stop using the Haversine distance algorithm.*
        """)

        g_col1, g_col2 = st.columns([1, 1])

        # Preset test coordinates around Udupi/Manipal
        preset_coords = {
            "Atradi Junction (Near Stop)": (13.3411, 74.8455),
            "Manipal Tiger Circle": (13.3525, 74.7928),
            "Katapadi NH-66 Cross": (13.2925, 74.7788),
            "Hiriyadka Market": (13.3444, 74.8824),
            "SMVITM Campus Gate": (13.2384, 74.8028)
        }

        with g_col1:
            selected_preset = st.selectbox("Select Preset GPS Location", list(preset_coords.keys()))
            preset_lat, preset_lon = preset_coords[selected_preset]

            custom_lat = st.number_input("Latitude", value=preset_lat, format="%.4f")
            custom_lon = st.number_input("Longitude", value=preset_lon, format="%.4f")

        with g_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🛰️ Detect Nearest Bus Stop"):
                route_df = df[df["Route"] == selected_route]
                nearest_stop, distance_km = utils.find_nearest_bus_stop(custom_lat, custom_lon, route_df)

                st.success(f"**GPS Resolution Result:**")
                st.write(f"- **Nearest Bus Stop**: `{nearest_stop}`")
                st.write(f"- **Distance from GPS Ping**: `{distance_km} km`")
                st.info(f"Setting Current Bus Location to **{nearest_stop}** for Route `{selected_route}`.")


if __name__ == "__main__":
    main()