# main.py
# ---------------------------------------------------------------------------
#
#   SupplyChain Guardian
#   Supply Chain Disruption & Fleet Intelligence Platform
#
# ---------------------------------------------------------------------------
# Entry point for the full platform.
# Run with:   python main.py
#
# Modules available:
#   [1] Disruption Monitor   — detect affected shipments
#   [2] Route Optimizer      — cargo-aware alternative routes
#   [3] Fleet Optimizer      — idle asset detection + redeployment matching
#   [4] Cold Chain Monitor   — temperature excursion detection
#   [5] Operations Dashboard — compact summary (Full Platform Run)
#   [0] Exit
# ---------------------------------------------------------------------------

from modules.disruption_monitor import detect_affected_shipments, print_disruption_report
from modules.route_optimizer    import recommend_routes
from modules.fleet_optimizer    import find_idle_assets, match_assets_to_shipments, print_fleet_report
from modules.cold_chain_monitor import analyse_all_readings, print_cold_chain_report

from data.fleet_data  import FLEET_ASSETS
from data.sensor_data import SENSOR_READINGS


# ---------------------------------------------------------------------------
# Active disruption configuration
# Change these two values to simulate a different disruption event.
# ---------------------------------------------------------------------------
DISRUPTION_LOCATION = "Suez Canal"
DISRUPTION_REASON   = "Geopolitical conflict causing route blockage"


# ---------------------------------------------------------------------------
# HELPER: banner
# ---------------------------------------------------------------------------
def banner():
    """Prints the SupplyChain Guardian product header."""
    print()
    print("=" * 65)
    print("   SupplyChain Guardian")
    print("   Supply Chain Disruption & Fleet Intelligence Platform")
    print("=" * 65)
    print(f"   Active Disruption : {DISRUPTION_LOCATION}")
    print(f"   Reason            : {DISRUPTION_REASON}")
    print("=" * 65)
    print()


def section(title):
    """Prints a visible section divider between modules."""
    print()
    print("┌" + "─" * 63 + "┐")
    print("│  " + title.ljust(61) + "│")
    print("└" + "─" * 63 + "┘")
    print()


# ---------------------------------------------------------------------------
# MODULE RUNNERS
# Each function runs exactly one module and nothing else.
# ---------------------------------------------------------------------------

def run_disruption_monitor():
    """Module 1 — Detect affected shipments (no route recommendations)."""
    section("MODULE 1 — DISRUPTION MONITOR")
    affected, safe = detect_affected_shipments(DISRUPTION_LOCATION, DISRUPTION_REASON)
    # Print without alternatives so this module stands alone
    print_disruption_report(DISRUPTION_LOCATION, DISRUPTION_REASON, affected, safe)


def run_route_optimizer():
    """Module 2 — Cargo-aware alternative route recommendations."""
    section("MODULE 2 — ROUTE OPTIMIZER")
    affected, safe = detect_affected_shipments(DISRUPTION_LOCATION, DISRUPTION_REASON)
    affected = recommend_routes(affected)
    print_disruption_report(DISRUPTION_LOCATION, DISRUPTION_REASON, affected, safe)


def run_fleet_optimizer():
    """Module 3 — Idle asset report (no shipment context)."""
    section("MODULE 3 — FLEET OPTIMIZER")
    idle = find_idle_assets(FLEET_ASSETS)
    print_fleet_report(FLEET_ASSETS, idle)


def run_cold_chain_monitor():
    """Module 4 — Temperature excursion detection."""
    section("MODULE 4 — COLD CHAIN MONITOR")
    grouped = analyse_all_readings(SENSOR_READINGS)
    print_cold_chain_report(grouped)


# ---------------------------------------------------------------------------
# HELPER: get_severity
# ---------------------------------------------------------------------------
def get_severity(affected_count):
    """
    Derives a simple severity label from the number of affected shipments.

    0 affected   → LOW
    1-2 affected → MEDIUM
    3+ affected  → HIGH

    Parameters:
        affected_count (int): number of disrupted shipments

    Returns:
        label (str): "LOW", "MEDIUM", or "HIGH"
        icon  (str): matching indicator symbol
    """
    if affected_count == 0:
        return "LOW",    "●"
    elif affected_count <= 2:
        return "MEDIUM", "●"
    else:
        return "HIGH",   "●"


# ---------------------------------------------------------------------------
# HELPER: get_worst_cold_chain_readings
# ---------------------------------------------------------------------------
def get_worst_cold_chain_readings(grouped):
    """
    For each shipment in the grouped sensor data, returns the single worst
    reading (highest priority: CRITICAL > WARNING > NORMAL).
    Shipments with an all-NORMAL record are excluded.

    Parameters:
        grouped (dict): output of analyse_all_readings()

    Returns:
        alerts (list): list of the worst reading dict per problem shipment,
                       sorted so CRITICAL comes before WARNING
    """
    PRIORITY = {"NORMAL": 0, "WARNING": 1, "CRITICAL": 2}
    alerts = []

    for sid, readings in grouped.items():
        # Find the single reading with the highest priority in this shipment
        worst = max(readings, key=lambda r: PRIORITY[r["status"]])
        if worst["status"] != "NORMAL":
            alerts.append(worst)

    # Sort so CRITICAL rows appear before WARNING rows in the table
    alerts.sort(key=lambda r: PRIORITY[r["status"]], reverse=True)
    return alerts


# ---------------------------------------------------------------------------
# HELPER: get_next_action
# ---------------------------------------------------------------------------
def get_next_action(affected, matches):
    """
    Picks the single most urgent shipment and builds one plain-English
    recommended action sentence.

    Priority: perishable or hazardous cargo on a blocked route comes first
    (because delay has the highest real-world cost). If none, use the first
    affected shipment.

    Parameters:
        affected (list): enriched affected shipments (with "alternatives")
        matches  (dict): { shipment_id: [matching_asset, ...] }

    Returns:
        action_line (str): one sentence the operator should act on now
    """
    if not affected:
        return "No disruptions detected. All systems normal."

    # Find the highest-priority shipment to act on
    priority_types = ["perishable", "hazardous"]
    urgent = None
    for shipment in affected:
        if shipment["cargo_type"] in priority_types:
            urgent = shipment
            break

    # Fall back to first affected shipment if no priority cargo found
    if urgent is None:
        urgent = affected[0]

    sid        = urgent["id"]
    cargo      = urgent["cargo"]
    cargo_type = urgent["cargo_type"]

    # Use the first alternative recommendation already computed
    first_alt = urgent["alternatives"][0] if urgent["alternatives"] else "manual review required"

    # Mention the matched fleet asset if one is available
    fleet_assets = matches.get(sid, [])
    fleet_note   = f" Deploy {fleet_assets[0]['id']} ({fleet_assets[0]['type']})." if fleet_assets else ""

    return (
        f"Reroute {sid} ({cargo} / {cargo_type}) immediately.\n"
        f"             Recommended: {first_alt}.{fleet_note}"
    )


# ---------------------------------------------------------------------------
# OPERATIONS DASHBOARD
# ---------------------------------------------------------------------------
def run_operations_dashboard():
    """
    Compact Operations Dashboard — the Full Platform Run for operators.

    Collects data from all four modules, then prints a short scannable
    summary instead of four full-length reports. The detailed reports are
    still available via menu options [1]–[4].
    """
    import datetime

    # ── Collect all data ────────────────────────────────────────────────────

    # Module 1 + 2: disruption detection with cargo-aware route recommendations
    affected, safe = detect_affected_shipments(DISRUPTION_LOCATION, DISRUPTION_REASON)
    affected       = recommend_routes(affected)

    # Module 3: fleet idle detection + asset-to-shipment matching
    idle    = find_idle_assets(FLEET_ASSETS)
    matches = match_assets_to_shipments(idle, affected)

    # Module 4: cold-chain classification
    grouped = analyse_all_readings(SENSOR_READINGS)
    alerts  = get_worst_cold_chain_readings(grouped)   # one row per problem shipment

    # ── Compute summary numbers ──────────────────────────────────────────────
    affected_count  = len(affected)
    idle_count      = len(idle)
    alert_count     = len(alerts)
    severity, s_icon = get_severity(affected_count)
    today           = datetime.date.today().strftime("%Y-%m-%d")

    # Width constant — every table/section fits inside this many characters
    W = 65

    # ── Section 1: Header ───────────────────────────────────────────────────
    print()
    print("=" * W)
    print("  SUPPLYCHAIN GUARDIAN — OPERATIONS SUMMARY")
    print(f"  {today}  |  Active Disruption: {DISRUPTION_LOCATION}")
    print("=" * W)

    # ── Section 2: Summary metrics ──────────────────────────────────────────
    # Three equal-width columns inside one row
    col = 19   # width of each metric cell (3 cols × 19 + 4 separators ≈ W)
    print()
    print("  ┌" + "─" * col + "┬" + "─" * col + "┬" + "─" * col + "┐")
    print("  │" + " Affected Shipments".center(col) +
          "│" + " Idle Fleet Assets".center(col) +
          "│" + " Cold-Chain Alerts".center(col) + "│")
    print("  │" + str(affected_count).center(col) +
          "│" + str(idle_count).center(col) +
          "│" + str(alert_count).center(col) + "│")
    print("  └" + "─" * col + "┴" + "─" * col + "┴" + "─" * col + "┘")

    # ── Section 3: Active Disruption ────────────────────────────────────────
    print()
    print("  ACTIVE DISRUPTION")
    print(f"  Location : {DISRUPTION_LOCATION}")
    print(f"  Reason   : {DISRUPTION_REASON}")
    print(f"  Severity : {s_icon} {severity}  ({affected_count} shipment(s) affected)")

    # ── Section 4: Action Table ──────────────────────────────────────────────
    print()
    print("  ACTION TABLE")
    print("  " + "─" * (W - 2))

    # Column widths — must add up to fit inside W
    c1, c2, c3, c4 = 9, 14, 28, 9
    header = (
        f"  {'Shipment':<{c1}} {'Issue':<{c2}} {'Recommended Action':<{c3}} {'Fleet':<{c4}}"
    )
    print(header)
    print("  " + "─" * (W - 2))

    if affected:
        for s in affected:
            sid   = s["id"]
            issue = "Route blocked"

            # First alternative — strip the cargo-type prefix tag if present
            # e.g. "[Recommended for perishable] Air freight..." → "Air freight..."
            raw_alt   = s["alternatives"][0] if s["alternatives"] else "Manual review"
            # Remove the "[Recommended for X] " prefix so the cell stays compact
            if raw_alt.startswith("["):
                closing = raw_alt.find("]")
                raw_alt = raw_alt[closing + 2:] if closing != -1 else raw_alt
            # Truncate to fit the column width, add "…" if cut
            action = (raw_alt[:c3 - 2] + "…") if len(raw_alt) > c3 - 1 else raw_alt

            # First matching fleet asset, or a dash
            fleet_assets = matches.get(sid, [])
            fleet        = fleet_assets[0]["id"] if fleet_assets else "—"

            print(f"  {sid:<{c1}} {issue:<{c2}} {action:<{c3}} {fleet:<{c4}}")
    else:
        print("  No affected shipments.")

    print("  " + "─" * (W - 2))

    # ── Section 5: Cold-Chain Alerts ─────────────────────────────────────────
    print()
    print("  COLD-CHAIN ALERTS")
    print("  " + "─" * (W - 2))

    # Column widths
    a1, a2, a3, a4 = 9, 22, 12, 18
    print(f"  {'Shipment':<{a1}} {'Cargo':<{a2}} {'Status':<{a3}} {'Temperature':<{a4}}")
    print("  " + "─" * (W - 2))

    ICONS = {"WARNING": "⚠️ ", "CRITICAL": "🔴"}

    if alerts:
        for r in alerts:
            icon      = ICONS.get(r["status"], "")
            status    = f"{icon}{r['status']}"
            # Show the recorded temp and which limit it breached
            if r["direction"] == "TOO HIGH":
                temp_note = f"{r['temperature']}°C  (max {r['temp_max']}°C)"
            elif r["direction"] == "TOO LOW":
                temp_note = f"{r['temperature']}°C  (min {r['temp_min']}°C)"
            else:
                temp_note = f"{r['temperature']}°C"

            cargo_short = (r["cargo"][:a2 - 2] + "…") if len(r["cargo"]) > a2 - 1 else r["cargo"]
            print(f"  {r['shipment_id']:<{a1}} {cargo_short:<{a2}} {status:<{a3}} {temp_note:<{a4}}")
    else:
        print("  ✅  No cold-chain alerts. All readings within safe ranges.")

    print("  " + "─" * (W - 2))

    # ── Section 6: Next Action ───────────────────────────────────────────────
    print()
    next_action = get_next_action(affected, matches)
    print("  " + "─" * (W - 2))
    print(f"  NEXT ACTION:  {next_action}")
    print("  " + "─" * (W - 2))
    print()


def run_full_platform():
    """Full Platform Run — shows the compact Operations Dashboard."""
    run_operations_dashboard()


# ---------------------------------------------------------------------------
# MENU
# ---------------------------------------------------------------------------

def show_menu():
    """Prints the interactive menu options."""
    print()
    print("  Select a module to run:")
    print()
    print("    [1]  Disruption Monitor      — Detect affected shipments")
    print("    [2]  Route Optimizer         — Alternative route recommendations")
    print("    [3]  Fleet Optimizer         — Idle asset detection")
    print("    [4]  Cold Chain Monitor      — Temperature excursion alerts")
    print("    [5]  Operations Dashboard    — Compact summary (all modules)")
    print("    [0]  Exit")
    print()


def main():
    """Main loop — shows the menu and dispatches to the chosen module."""
    banner()

    # Map menu choices to runner functions
    options = {
        "1": run_disruption_monitor,
        "2": run_route_optimizer,
        "3": run_fleet_optimizer,
        "4": run_cold_chain_monitor,
        "5": run_full_platform,
    }

    while True:
        show_menu()
        # input() pauses the program and waits for the user to type something
        choice = input("  Enter choice: ").strip()

        if choice == "0":
            print()
            print("  Exiting SupplyChain Guardian. Goodbye.")
            print()
            break
        elif choice in options:
            options[choice]()   # call the matching function
        else:
            print()
            print("  ⚠️  Invalid choice. Please enter a number from the menu.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
