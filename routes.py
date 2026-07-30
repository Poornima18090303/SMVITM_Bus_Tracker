"""
routes.py
---------
Module to handle SMVITM bus dataset loading, route lookup, and stop management.
Seamlessly reads the user's actual Excel dataset from D:\\Bus_tracking\\SMVITM_BUS_DATASETS.xlsx.
"""

import os
import pandas as pd
import process_user_data

PRIMARY_USER_EXCEL = r"D:\Bus_tracking\SMVITM_BUS_DATASETS.xlsx"
LOCAL_EXCEL = r"D:\Bus_tracker\SMVITM_BUS_DATASETS.xlsx"


def load_dataset() -> pd.DataFrame:
    """Loads and returns the cleaned dataframe from user's Excel file."""
    if os.path.exists(PRIMARY_USER_EXCEL):
        try:
            return process_user_data.load_and_clean_user_dataset()
        except Exception as e:
            print(f"Warning: Could not process {PRIMARY_USER_EXCEL} directly ({e}). Loading local Excel...")

    if os.path.exists(LOCAL_EXCEL):
        df = pd.read_excel(LOCAL_EXCEL, engine="openpyxl")
        df["Time"] = df["Time"].astype(str).str.zfill(5)
        df["Route"] = df["Route"].astype(str)
        df["Stop"] = df["Stop"].astype(str)
        return df

    # Fallback to creating clean dataset
    return process_user_data.load_and_clean_user_dataset()


def ensure_dataset_exists() -> pd.DataFrame:
    """Ensure dataset is loaded and available."""
    return load_dataset()


def get_all_routes(df: pd.DataFrame) -> list:
    """Returns sorted list of unique routes (e.g. Route 1, Route 2, ..., Route 9)."""
    # Sort naturally by route number
    def get_route_num(r_str):
        try:
            return int(str(r_str).replace("Route ", "").strip())
        except Exception:
            return 99
            
    routes = sorted(df["Route"].unique().tolist(), key=get_route_num)
    return routes


def get_stops_for_route(df: pd.DataFrame, route_name: str) -> list:
    """Returns exact list of stops for the specified route in schedule order."""
    route_df = df[df["Route"] == route_name]
    return route_df["Stop"].tolist()


def get_stop_details(df: pd.DataFrame, route_name: str, stop_name: str) -> dict:
    """Get timetable record for a specific route and stop."""
    match = df[(df["Route"] == route_name) & (df["Stop"] == stop_name)]
    if not match.empty:
        return match.iloc[0].to_dict()
    return {}
