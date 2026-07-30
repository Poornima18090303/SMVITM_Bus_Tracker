"""
utils.py
--------
Utility functions for time parsing, ETA calculation, crossed stop detection,
GPS Haversine distance, and nearest bus stop resolution.
"""

import math
from typing import Dict, Any, Tuple


def parse_time_to_minutes(time_str: str) -> int:
    """
    Converts time string 'HH:MM' or 'HH:MM:SS' into minutes from midnight.
    Example: '08:20' -> 500 minutes
    """
    clean_str = str(time_str).strip()
    parts = clean_str.split(":")
    hours = int(parts[0])
    minutes = int(parts[1]) if len(parts) > 1 else 0
    return hours * 60 + minutes


def format_minutes_to_ampm(total_minutes: int) -> str:
    """
    Converts total minutes from midnight into 12-hour AM/PM string.
    Example: 510 -> '8:30 AM'
    """
    total_minutes = total_minutes % (24 * 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    period = "AM" if hours < 12 else "PM"
    
    display_hour = hours % 12
    if display_hour == 0:
        display_hour = 12
        
    return f"{display_hour}:{minutes:02d} {period}"


def calculate_eta_details(df, route_name: str, current_stop: str, my_stop: str) -> Dict[str, Any]:
    """
    Calculates ETA, distance remaining, and arrival time based on the timetable dataset.
    Detects if the bus has already crossed the student's stop.
    """
    route_df = df[df["Route"] == route_name].reset_index(drop=True)
    
    # Locate stop indices
    current_idx_list = route_df.index[route_df["Stop"] == current_stop].tolist()
    my_idx_list = route_df.index[route_df["Stop"] == my_stop].tolist()
    
    if not current_idx_list or not my_idx_list:
        return {
            "status": "ERROR",
            "message": "Selected stops are not found in the timetable."
        }
        
    current_idx = current_idx_list[0]
    my_idx = my_idx_list[0]
    
    current_row = route_df.iloc[current_idx]
    my_row = route_df.iloc[my_idx]
    
    current_time_min = parse_time_to_minutes(current_row["Time"])
    my_time_min = parse_time_to_minutes(my_row["Time"])
    
    current_dist = float(current_row.get("Distance_km", 0.0))
    my_dist = float(my_row.get("Distance_km", 0.0))
    
    # Case 1: Bus already crossed student's stop
    if current_idx > my_idx:
        return {
            "status": "CROSSED",
            "message": "⚠ Bus has already crossed your stop.",
            "current_stop": current_stop,
            "my_stop": my_stop,
            "current_time_str": format_minutes_to_ampm(current_time_min),
            "my_scheduled_time_str": format_minutes_to_ampm(my_time_min),
        }
    
    # Case 2: Student is currently at the bus stop (ETA = 0)
    if current_idx == my_idx:
        return {
            "status": "ARRIVING_NOW",
            "message": "🎉 Bus is currently at your stop!",
            "eta_minutes": 0,
            "distance_km": 0.0,
            "expected_arrival": format_minutes_to_ampm(my_time_min),
            "current_stop": current_stop,
            "my_stop": my_stop,
        }
        
    # Case 3: Bus is on the way (Normal ETA calculation)
    eta_minutes = my_time_min - current_time_min
    distance_remaining = max(0.0, my_dist - current_dist)
    expected_arrival_str = format_minutes_to_ampm(my_time_min)
    
    return {
        "status": "SUCCESS",
        "eta_minutes": eta_minutes,
        "distance_km": round(distance_remaining, 1),
        "expected_arrival": expected_arrival_str,
        "current_stop": current_stop,
        "my_stop": my_stop,
        "current_time_str": format_minutes_to_ampm(current_time_min),
        "stops_between": my_idx - current_idx,
        "message": f"✅ Bus will arrive at {my_stop} in {eta_minutes} minutes"
    }


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the great-circle distance between two points on the Earth in kilometers.
    """
    R = 6371.0  # Earth's radius in km
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def find_nearest_bus_stop(lat: float, lon: float, route_df) -> Tuple[str, float]:
    """
    Finds the closest bus stop from a set of route stops given GPS coordinates.
    Returns (stop_name, distance_in_km).
    """
    min_dist = float("inf")
    nearest_stop = None
    
    for _, row in route_df.iterrows():
        stop_lat = float(row["Latitude"])
        stop_lon = float(row["Longitude"])
        dist = haversine_distance(lat, lon, stop_lat, stop_lon)
        if dist < min_dist:
            min_dist = dist
            nearest_stop = row["Stop"]
            
    return nearest_stop, round(min_dist, 2)
