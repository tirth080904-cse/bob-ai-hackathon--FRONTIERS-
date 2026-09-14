# modules/cold_chain_monitor.py
# ---------------------------------------------------------------------------
# SupplyChain Guardian — Module 4: Cold Chain Monitor
# ---------------------------------------------------------------------------
# Monitors temperature sensor readings for sensitive shipments and
# classifies each reading as NORMAL, WARNING, or CRITICAL.
#
# Classification rule (unchanged from original sensor.py):
#   breach = how many degrees outside the allowed range
#   breach == 0            → NORMAL
#   0 < breach ≤ 3.0°C    → WARNING
#   breach > 3.0°C         → CRITICAL
# ---------------------------------------------------------------------------

from data.sensor_data import SENSOR_READINGS

# Breach threshold that separates WARNING from CRITICAL
WARNING_MARGIN = 3.0   # degrees Celsius


def classify_reading(reading):
    """
    Classifies one sensor reading and returns it enriched with:
      status        - "NORMAL", "WARNING", or "CRITICAL"
      breach_amount - how many degrees outside range (0 if normal)
      direction     - "TOO HIGH", "TOO LOW", or "OK"
      reason        - plain-English explanation

    Parameters:
        reading (dict): one entry from SENSOR_READINGS

    Returns:
        result (dict): original fields + status, breach_amount, direction, reason
    """
    temp     = reading["temperature"]
    temp_min = reading["temp_min"]
    temp_max = reading["temp_max"]

    if temp < temp_min:
        breach_amount = temp_min - temp
        direction     = "TOO LOW"
    elif temp > temp_max:
        breach_amount = temp - temp_max
        direction     = "TOO HIGH"
    else:
        breach_amount = 0.0
        direction     = "OK"

    if breach_amount == 0.0:
        status = "NORMAL"
        reason = (
            f"Temperature {temp}°C is within the safe range "
            f"({temp_min}°C – {temp_max}°C)."
        )
    elif breach_amount <= WARNING_MARGIN:
        status = "WARNING"
        reason = (
            f"Temperature {temp}°C is {direction} by {breach_amount:.1f}°C. "
            f"Safe range: {temp_min}°C – {temp_max}°C. "
            f"Monitor closely — cargo may be at risk."
        )
    else:
        status = "CRITICAL"
        reason = (
            f"Temperature {temp}°C is {direction} by {breach_amount:.1f}°C. "
            f"Safe range: {temp_min}°C – {temp_max}°C. "
            f"Immediate action required — cargo integrity compromised."
        )

    result = dict(reading)
    result["status"]        = status
    result["breach_amount"] = breach_amount
    result["direction"]     = direction
    result["reason"]        = reason
    return result


def analyse_all_readings(readings):
    """
    Classifies every reading and groups results by shipment_id.

    Parameters:
        readings (list): full SENSOR_READINGS list

    Returns:
        grouped (dict): { shipment_id: [classified_reading, ...] }
    """
    grouped = {}
    for reading in readings:
        classified = classify_reading(reading)
        sid = classified["shipment_id"]
        if sid not in grouped:
            grouped[sid] = []
        grouped[sid].append(classified)
    return grouped


def print_cold_chain_report(grouped):
    """
    Prints the full cold-chain temperature monitoring report.

    Parameters:
        grouped (dict): output of analyse_all_readings()
    """
    ICONS    = {"NORMAL": "✅", "WARNING": "⚠️ ", "CRITICAL": "🔴"}
    PRIORITY = {"NORMAL": 0, "WARNING": 1, "CRITICAL": 2}

    print("=" * 65)
    print("  COLD CHAIN MONITOR")
    print("=" * 65)

    problem_shipments = []

    for shipment_id, readings in grouped.items():
        worst_status = max(readings, key=lambda r: PRIORITY[r["status"]])["status"]
        if worst_status != "NORMAL":
            problem_shipments.append(shipment_id)

        cargo = readings[0]["cargo"]
        icon  = ICONS[worst_status]

        print(f"\n  {icon} Shipment {shipment_id}  |  Cargo: {cargo}  |  Status: {worst_status}")
        print(f"     {len(readings)} reading(s) recorded:\n")

        for r in readings:
            reading_icon = ICONS[r["status"]]
            print(f"     {reading_icon} [{r['timestamp']}]  {r['temperature']}°C  →  {r['status']}")
            if r["status"] != "NORMAL":
                print(f"        Reason: {r['reason']}")

        print()

    print("=" * 65)
    if problem_shipments:
        print(f"\n  SHIPMENTS REQUIRING ATTENTION ({len(problem_shipments)}):\n")
        for sid in problem_shipments:
            readings       = grouped[sid]
            cargo          = readings[0]["cargo"]
            warn_count     = sum(1 for r in readings if r["status"] == "WARNING")
            critical_count = sum(1 for r in readings if r["status"] == "CRITICAL")
            print(f"    • {sid} ({cargo})")
            if critical_count:
                print(f"        🔴 {critical_count} CRITICAL reading(s)")
            if warn_count:
                print(f"        ⚠️  {warn_count} WARNING reading(s)")
        print()
    else:
        print("\n  ✅ All shipments within safe temperature ranges.\n")

    print("=" * 65)


# ---------------------------------------------------------------------------
# Standalone run:  python -m modules.cold_chain_monitor
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    grouped = analyse_all_readings(SENSOR_READINGS)
    print_cold_chain_report(grouped)
