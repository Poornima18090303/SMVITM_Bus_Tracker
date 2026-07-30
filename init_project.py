import os
import shutil
import pandas as pd
import routes

def main():
    print("Re-generating SMVITM Bus ETA Project dataset cleanly...")
    df = routes.create_fresh_excel()
    print(f"Dataset successfully created with {len(df)} records across {df['Route'].nunique()} routes.")
    for route in routes.get_all_routes(df):
        stops = routes.get_stops_for_route(df, route)
        print(f"  - {route}: {stops}")
    
    # Ensure assets directory exists
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    brain_logo = r"C:\Users\chait\.gemini\antigravity\brain\91a94f99-8685-44e2-b2b8-c7d7be932de8\bus_tracker_logo_1785046546103.png"
    target_logo = os.path.join(assets_dir, "logo.png")
    
    if os.path.exists(brain_logo):
        shutil.copy(brain_logo, target_logo)
        print(f"Copied logo to {target_logo}")

if __name__ == "__main__":
    main()
