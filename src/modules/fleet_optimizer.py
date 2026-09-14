# modules/fleet_optimizer.py
# ---------------------------------------------------------------------------
# SupplyChain Guardian — Module 3: Fleet Optimizer
# ---------------------------------------------------------------------------
# Identifies idle assets and recommends which ones could cover
# affected shipments based on cargo compatibility.
#
# What's new vs the original fleet.py:
#   - match_assets_to_shipments(): for each affected shipment, finds idle
#     assets whose "suitable_for" list includes that shipment's cargo_type.
#   - print_fleet_report() now includes a redeployment recommendation section.
# ---------------------------------------------------------------------------

from data.fleet_data import FLEET_ASSETS


def find_idle_assets(assets):
    """
    Returns only assets with status "Idle".

    Parameters:
        assets (list): full fleet asset list

    Returns:
        idle (list): assets where status == "Idle"
    """
    return [asset for asset in assets if asset["status"] == "Idle"]


def match_assets_to_shipments(idle_assets, affected_shipments):
    """
    For each affected shipment, finds idle assets that are suitable
    for carrying that shipment's cargo type.

    Logic:
      - Checks if the shipment's cargo_type appears in the asset's
        "suitable_for" list.
      - Returns a dict: { shipment_id → list of matching asset dicts }

    Parameters:
        idle_assets         (list): output of find_idle_assets()
        affected_shipments  (list): output of detect_affected_shipments()

    Returns:
        matches (dict): { "SHP-001": [asset_dict, ...], ... }
    """
    matches = {}

    for shipment in affected_shipments:
        sid        = shipment["id"]
        cargo_type = shipment["cargo_type"]

        # Keep only idle assets whose suitable_for list includes this cargo type
        compatible = [
            asset for asset in idle_assets
            if cargo_type in asset["suitable_for"]
        ]

        matches[sid] = compatible

    return matches


def print_fleet_report(all_assets, idle_assets, matches=None):
    """
    Prints the fleet utilisation report.
    If matches are provided (from match_assets_to_shipments), also prints
    a redeployment recommendation section.

    Parameters:
        all_assets  (list): full fleet list
        idle_assets (list): idle assets only
        matches     (dict or None): optional — shipment-to-asset matches
    """
    total        = len(all_assets)
    idle_count   = len(idle_assets)
    in_use_count = total - idle_count

    print("=" * 65)
    print("  FLEET OPTIMIZER")
    print("=" * 65)
    print(f"  Total Assets : {total}  |  In Use : {in_use_count}  |  Idle : {idle_count}")
    print("=" * 65)

    # ---- Idle assets grouped by type ----
    print(f"\n  🚚  IDLE ASSETS — AVAILABLE FOR REDEPLOYMENT ({idle_count}):\n")

    if idle_assets:
        # Group by asset type
        grouped = {}
        for asset in idle_assets:
            t = asset["type"]
            if t not in grouped:
                grouped[t] = []
            grouped[t].append(asset)

        for asset_type, group in grouped.items():
            print(f"    [ {asset_type}s ]")
            for asset in group:
                suitable = ", ".join(asset["suitable_for"])
                print(f"      {asset['id']}  —  {asset['location']}")
                print(f"             Capacity    : {asset['capacity_tons']} tons")
                print(f"             Suitable for: {suitable}")
            print()
    else:
        print("    No idle assets — all fleet is currently deployed.\n")

    # ---- Redeployment recommendations (only shown when called from main) ----
    if matches:
        print("  🔁  REDEPLOYMENT RECOMMENDATIONS FOR AFFECTED SHIPMENTS:\n")
        for shipment_id, assets in matches.items():
            if assets:
                print(f"    Shipment {shipment_id} can be covered by:")
                for asset in assets:
                    print(f"      → {asset['id']} ({asset['type']}) at {asset['location']}")
            else:
                print(f"    Shipment {shipment_id}: No compatible idle asset found — manual sourcing needed.")
            print()

    print("=" * 65)


# ---------------------------------------------------------------------------
# Standalone run:  python -m modules.fleet_optimizer
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    idle = find_idle_assets(FLEET_ASSETS)
    print_fleet_report(FLEET_ASSETS, idle)
