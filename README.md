# 🚍 Smart College Bus ETA & Tracking System

An engineering project built for **Shri Madhwa Vadiraja Institute of Technology and Management (SMVITM)**, Bantakal.

This system provides real-time stop-to-stop ETA prediction for college buses using scheduled timetable matrices, dynamic route stop filtering, crossed-stop validation, and simulated GPS geolocation lookup.

---

## 💡 Project Naming & Interview Defense Guide

### ❓ Question from External Examiner / Interviewer:
> *"Is this really an AI model, or is it an algorithmic timetable/spatial tracking system?"*

### 🗣️ Perfect Technical Answer:

> *"You are absolutely right, sir/ma'am. In this implementation phase, we built a **Smart Algorithmic Baseline System** using deterministic schedule time deltas and a **spatial k-Nearest Neighbor (Haversine) algorithm** for GPS geolocation mapping.*
>
> *We chose this approach over a Machine Learning model because our current dataset consists of fixed timetable schedules rather than historical GPS delay logs. For fixed college bus timetables, deterministic calculations are **100% accurate and mathematically exact**.*
>
> *In a future deployment with live GPS hardware, an ML model (like Random Forest or XGBoost) can be trained on historical traffic congestion and weather features to predict real-time delay offsets relative to our baseline."*

---

## 📌 Recommended Project Titles

1. **Smart College Bus ETA & Tracking System** *(Recommended - 100% technically accurate & safe from tricky examiner questions)*
2. **Intelligent Timetable & Geolocation College Bus Tracker**
3. **AI-Based College Bus Tracking System (Phase 1 Baseline)**

---

## 🔥 Key Features

- **Dynamic Route Filtering**: Selecting a bus route automatically updates the available current location and destination stop dropdowns for all 9 SMVITM routes.
- **Stop-to-Stop Timetable ETA**: Calculates exact arrival time differences and remaining route distance (`26.0 km` for Hiriadka $\rightarrow$ SMVITM).
- **Crossed-Stop Detection**: Alerts the user with `⚠ Bus has already crossed your stop` if the current bus position is past the student's stop.
- **Visual Bus Route Tracker**: Displays an interactive horizontal stepper highlighting origin, live position, destination stop, and SMVITM campus.
- **Simulated GPS Geolocation Module**: Demonstrates real-world hardware integration by converting Latitude/Longitude GPS telemetry into the nearest timetable bus stop using spatial distance calculations.

---

## 🚀 How to Run the Application

```bash
pip install -r requirements.txt
python process_user_data.py
streamlit run dashboard.py
```
