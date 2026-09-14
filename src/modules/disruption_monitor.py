# modules/disruption_monitor.py
# ---------------------------------------------------------------------------
# SupplyChain Guardian — Module 1: Disruption Monitor
# ---------------------------------------------------------------------------
# Detects which shipments are affected by an active disruption.
#
# A shipment is affected when the disruption_location matches (or is contained
# in) the shipment's route field.
#
# This module only detects — it does NOT recommend routes.
# Route recommendations are handled by modules/route_optimizer.py.
# ---------------------------------------------------------------------------

from data.shipments import SHIPMENTS


def detect_affected_shipments(disruption_location, disruption_reason):
    """
    Scans all shipments and splits them into affected and safe lists.

    Parameters:
        disruption_location (str): the disrupted route, e.g. "Suez Canal"
        disruption_reason   (str): plain-English description of the event

    Returns:
        affected (list): shipments whose route passes through the disruption
        safe     (list): shipments that are unaffected
    """
    affected = []
    safe     = []

    for shipment in SHIPMENTS:
        # Case-insensitive substring match so partial names still work
        if disruption_location.lower() in shipment["route"].lower():
            affected.append(dict(shipment))   # copy so we can enrich safely
        else:
            safe.append(shipment)

    return affected, safe


def print_disruption_report(disruption_location, disruption_reason, affected, safe):
    """
    Prints the disruption detection section of the report.
    Affected shipments are expected to already have an "alternatives" key
    added by route_optimizer.recommend_routes() before this is called.

    Parameters:
        disruption_location (str)
        disruption_reason   (str)
        affected            (list): enriched by route_optimizer
        safe                (list)
    """
    print("=" * 65)
    print("  DISRUPTION MONITOR")
    print("=" * 65)
    print(f"  Active Disruption : {disruption_location}")
    print(f"  Reason            : {disruption_reason}")
    print(f"  Affected          : {len(affected)} shipment(s)  |  Safe: {len(safe)}")
    print("=" * 65)

    # ---- Affected shipments ----
    print(f"\n  ⚠️  AFFECTED SHIPMENTS ({len(affected)}):\n")
    if affected:
        for s in affected:
            print(f"    [{s['id']}]  {s['origin']} → {s['destination']}")
            print(f"           Cargo      : {s['cargo']}  [{s['cargo_type']}]")
            print(f"           Route      : {s['route']}")
            print(f"           Status     : {s['status']}")

            # Alternatives are added by route_optimizer — print if present
            if "alternatives" in s:
                print(f"           Alternatives:")
                for i, alt in enumerate(s["alternatives"], start=1):
                    print(f"             {i}) {alt}")
            print()
    else:
        print("    None — no shipments are affected.\n")

    # ---- Safe shipments ----
    print(f"  ✅  SAFE SHIPMENTS ({len(safe)}):\n")
    if safe:
        for s in safe:
            print(f"    [{s['id']}]  {s['origin']} → {s['destination']}")
            print(f"           Cargo  : {s['cargo']}  [{s['cargo_type']}]")
            print(f"           Route  : {s['route']}")
            print()
    else:
        print("    None.\n")

    print("=" * 65)


# ---------------------------------------------------------------------------
# Standalone run:  python -m modules.disruption_monitor
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from modules.route_optimizer import recommend_routes

    LOCATION = "Suez Canal"
    REASON   = "Geopolitical conflict causing route blockage"

    affected, safe = detect_affected_shipments(LOCATION, REASON)
    affected = recommend_routes(affected)
    print_disruption_report(LOCATION, REASON, affected, safe)
