"""
verify_project.py
-----------------
Sanity checks for routes, utils, dataset integrity, and calculation logic with user's actual dataset.
"""

import routes
import utils

def test_all():
    print("1. Loading user's dataset from D:\\Bus_tracking\\SMVITM_BUS_DATASETS.xlsx...")
    df = routes.ensure_dataset_exists()
    assert not df.empty, "Dataset is empty!"
    print(f"   [PASS] Loaded {len(df)} rows across {df['Route'].nunique()} routes.")

    print("2. Verifying routes...")
    all_routes = routes.get_all_routes(df)
    assert len(all_routes) == 9, f"Expected 9 routes, found {len(all_routes)}"
    print(f"   [PASS] Routes found: {all_routes}")

    print("3. Verifying dynamic stops for Route 3...")
    stops_r3 = routes.get_stops_for_route(df, "Route 3")
    print(f"   [PASS] Route 3 stops ({len(stops_r3)}): {stops_r3}")

    print("4. Testing ETA calculation (Route 3 - Current: Atradi, My Stop: SMVITM)...")
    res_normal = utils.calculate_eta_details(df, "Route 3", "Atradi", "SMVITM")
    assert res_normal["status"] == "SUCCESS", f"Expected SUCCESS, got {res_normal['status']}"
    print(f"   [PASS] ETA result: {res_normal['message']} (Arrival: {res_normal['expected_arrival']})".encode('ascii', 'ignore').decode('ascii'))

    print("5. Testing crossed stop logic (Route 3 - Current: SMVITM, My Stop: Atradi)...")
    res_crossed = utils.calculate_eta_details(df, "Route 3", "SMVITM", "Atradi")
    assert res_crossed["status"] == "CROSSED", f"Expected CROSSED, got {res_crossed['status']}"
    print(f"   [PASS] Crossed message: {res_crossed['message']}".encode('ascii', 'ignore').decode('ascii'))

    print("6. Testing Haversine GPS resolution...")
    r3_df = df[df["Route"] == "Route 3"]
    # Coordinates near Atradi
    stop, dist = utils.find_nearest_bus_stop(13.3411, 74.8455, r3_df)
    assert stop == "Atradi", f"Expected Atradi, got {stop}"
    print(f"   [PASS] Nearest stop resolved to: {stop} ({dist} km away)")

    print("\n[ALL VERIFICATION TESTS PASSED SUCCESSFULLY!]")

if __name__ == "__main__":
    test_all()
