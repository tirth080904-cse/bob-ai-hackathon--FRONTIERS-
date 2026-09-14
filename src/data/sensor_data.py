# data/sensor_data.py
# ---------------------------------------------------------------------------
# SupplyChain Guardian — Cold-Chain Sensor Data
# ---------------------------------------------------------------------------
# Stores all temperature sensor readings for sensitive shipments.
#
# Every reading has:
#   shipment_id - which shipment this reading belongs to
#   cargo       - what is being carried
#   temperature - recorded temperature in °C
#   timestamp   - when the reading was taken (plain string)
#   temp_min    - lowest safe temperature for this cargo (°C)
#   temp_max    - highest safe temperature for this cargo (°C)
# ---------------------------------------------------------------------------

SENSOR_READINGS = [
    # Vaccines — strict range: 2°C to 8°C
    {
        "shipment_id": "SHP-101",
        "cargo": "Vaccines",
        "temperature": 5.2,
        "timestamp": "2026-09-13 08:00",
        "temp_min": 2.0,
        "temp_max": 8.0,
    },
    {
        "shipment_id": "SHP-101",
        "cargo": "Vaccines",
        "temperature": 9.8,
        "timestamp": "2026-09-13 10:30",
        "temp_min": 2.0,
        "temp_max": 8.0,
    },
    {
        "shipment_id": "SHP-101",
        "cargo": "Vaccines",
        "temperature": 14.5,
        "timestamp": "2026-09-13 12:00",
        "temp_min": 2.0,
        "temp_max": 8.0,
    },

    # Frozen Seafood — must stay below -15°C
    {
        "shipment_id": "SHP-102",
        "cargo": "Frozen Seafood",
        "temperature": -18.0,
        "timestamp": "2026-09-13 07:00",
        "temp_min": -25.0,
        "temp_max": -15.0,
    },
    {
        "shipment_id": "SHP-102",
        "cargo": "Frozen Seafood",
        "temperature": -13.5,
        "timestamp": "2026-09-13 09:45",
        "temp_min": -25.0,
        "temp_max": -15.0,
    },

    # Fresh Produce — keep between 2°C and 6°C
    {
        "shipment_id": "SHP-103",
        "cargo": "Fresh Produce",
        "temperature": 4.1,
        "timestamp": "2026-09-13 06:30",
        "temp_min": 2.0,
        "temp_max": 6.0,
    },
    {
        "shipment_id": "SHP-103",
        "cargo": "Fresh Produce",
        "temperature": 1.0,
        "timestamp": "2026-09-13 11:00",
        "temp_min": 2.0,
        "temp_max": 6.0,
    },

    # Industrial Chemicals — keep between 15°C and 25°C
    {
        "shipment_id": "SHP-104",
        "cargo": "Industrial Chemicals",
        "temperature": 20.0,
        "timestamp": "2026-09-13 08:15",
        "temp_min": 15.0,
        "temp_max": 25.0,
    },
    {
        "shipment_id": "SHP-104",
        "cargo": "Industrial Chemicals",
        "temperature": 30.5,
        "timestamp": "2026-09-13 13:00",
        "temp_min": 15.0,
        "temp_max": 25.0,
    },
    {
        "shipment_id": "SHP-104",
        "cargo": "Industrial Chemicals",
        "temperature": 42.0,
        "timestamp": "2026-09-13 15:30",
        "temp_min": 15.0,
        "temp_max": 25.0,
    },

    # Blood Samples — very strict: 2°C to 6°C
    {
        "shipment_id": "SHP-105",
        "cargo": "Blood Samples",
        "temperature": 3.5,
        "timestamp": "2026-09-13 09:00",
        "temp_min": 2.0,
        "temp_max": 6.0,
    },
    {
        "shipment_id": "SHP-105",
        "cargo": "Blood Samples",
        "temperature": 5.9,
        "timestamp": "2026-09-13 11:30",
        "temp_min": 2.0,
        "temp_max": 6.0,
    },
]
