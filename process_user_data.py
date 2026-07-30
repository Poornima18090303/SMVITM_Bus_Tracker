import os
import pandas as pd
import numpy as np
import utils

USER_EXCEL_PATH = r"D:\Bus_tracking\SMVITM_BUS_DATASETS.xlsx"
LOCAL_EXCEL_PATH = r"D:\Bus_tracker\SMVITM_BUS_DATASETS.xlsx"

# Real total route distances in km to SMVITM campus
ROUTE_TOTAL_DISTANCES_KM = {
    "Route 1": 18.0,  # Santhekatte -> SMVITM
    "Route 2": 16.5,  # Rajanagara -> SMVITM
    "Route 3": 26.0,  # Hiriadka -> SMVITM (Exact 26 km as specified by user)
    "Route 4": 28.0,  # Sasthana -> SMVITM
    "Route 5": 35.0,  # Karkala -> SMVITM
    "Route 6": 20.0,  # Muddu Alevoor -> SMVITM
    "Route 7": 48.0,  # Kundapura -> SMVITM
    "Route 8": 22.0,  # Brahmavara -> SMVITM
    "Route 9": 16.0,  # Manipal Tiger Circle -> SMVITM
}

# Known GPS Coordinates for key landmarks around Udupi/Manipal/SMVITM
KNOWN_COORDINATES = {
    "SMVITM": (13.2384, 74.8028),
    "Santhekatte": (13.3768, 74.7645),
    "Ashirwad": (13.3650, 74.7600),
    "Ambagilu": (13.3580, 74.7550),
    "Nittur": (13.3480, 74.7480),
    "Ambalpady": (13.3280, 74.7400),
    "Katapadi": (13.2925, 74.7788),
    "Udyavara": (13.3100, 74.7550),
    "Hiriadka": (13.3444, 74.8824),
    "Atradi": (13.3411, 74.8455),
    "Manipal": (13.3525, 74.7928),
    "Manipal Tiger Circle": (13.3525, 74.7928),
    "Brahmavara": (13.4286, 74.7431),
    "Kundapura": (13.6264, 74.6908),
    "Saligrama": (13.5042, 74.7171),
    "Shirva": (13.2312, 74.8384),
    "Belman": (13.1800, 74.8700),
    "Karkala": (13.2170, 74.9970),
    "City Bus Stand": (13.3409, 74.7421),
    "Service Bus Stand": (13.3400, 74.7430),
    "MGM": (13.3480, 74.7680),
    "Kadiyali": (13.3500, 74.7750),
}


def load_and_clean_user_dataset():
    if not os.path.exists(USER_EXCEL_PATH):
        raise FileNotFoundError(f"Cannot find dataset at {USER_EXCEL_PATH}")

    raw_df = pd.read_excel(USER_EXCEL_PATH, engine="openpyxl")
    raw_df = raw_df.dropna(how="all").reset_index(drop=True)
    raw_df = raw_df[raw_df["ROUTE No."].notna()].copy()

    # Format Route Name
    raw_df["Route"] = "Route " + raw_df["ROUTE No."].astype(int).astype(str)
    raw_df["Stop"] = raw_df["Location"].astype(str).str.strip()

    # Format Time string (HH:MM)
    def clean_time(val):
        s = str(val).strip()
        parts = s.split(":")
        if len(parts) >= 2:
            return f"{int(parts[0]):02d}:{int(parts[1]):02d}"
        return "08:00"

    raw_df["Time"] = raw_df["TIME"].apply(clean_time)

    processed_rows = []

    for route_name, group in raw_df.groupby("Route", sort=False):
        group = group.reset_index(drop=True)
        first_time_min = utils.parse_time_to_minutes(group.iloc[0]["Time"])
        last_time_min = utils.parse_time_to_minutes(group.iloc[-1]["Time"])
        total_time_span = max(1, last_time_min - first_time_min)
        
        total_route_km = ROUTE_TOTAL_DISTANCES_KM.get(route_name, 25.0)

        start_stop = group.iloc[0]["Stop"]
        end_stop = group.iloc[-1]["Stop"]
        
        start_coords = KNOWN_COORDINATES.get(start_stop, (13.3500, 74.7500))
        end_coords = KNOWN_COORDINATES.get(end_stop, (13.2384, 74.8028))

        n_stops = len(group)

        for i, row in group.iterrows():
            stop_name = row["Stop"]
            time_str = row["Time"]
            time_min = utils.parse_time_to_minutes(time_str)

            # Cumulative distance proportionally scaled to total_route_km
            time_fraction = (time_min - first_time_min) / total_time_span
            dist_km = round(time_fraction * total_route_km, 1)

            # Coordinate estimation if not directly in lookup table
            if stop_name in KNOWN_COORDINATES:
                lat, lon = KNOWN_COORDINATES[stop_name]
            else:
                fraction = i / max(1, n_stops - 1)
                lat = round(start_coords[0] + fraction * (end_coords[0] - start_coords[0]), 4)
                lon = round(start_coords[1] + fraction * (end_coords[1] - start_coords[1]), 4)

            processed_rows.append({
                "Route": route_name,
                "Stop": stop_name,
                "Time": time_str,
                "Latitude": lat,
                "Longitude": lon,
                "Distance_km": dist_km
            })

    clean_df = pd.DataFrame(processed_rows)

    # Save to local workspace
    clean_df.to_excel(LOCAL_EXCEL_PATH, index=False, engine="openpyxl")
    return clean_df


if __name__ == "__main__":
    df = load_and_clean_user_dataset()
    print("\nDistance calibration check:")
    for route in sorted(df["Route"].unique()):
        r_df = df[df["Route"] == route]
        first_stop = r_df.iloc[0]["Stop"]
        last_stop = r_df.iloc[-1]["Stop"]
        total_dist = r_df.iloc[-1]["Distance_km"]
        print(f"  {route}: {first_stop} -> {last_stop} = {total_dist} km")
