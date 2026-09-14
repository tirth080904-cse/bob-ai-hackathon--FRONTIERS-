# data/fleet_data.py
# ---------------------------------------------------------------------------
# SupplyChain Guardian — Fleet Asset Data
# ---------------------------------------------------------------------------
# Stores all fleet asset records.
#
# Changes from the original fleet.py:
#   - Added "capacity_tons" field — lets Fleet Optimizer match assets to
#     shipment size rather than just listing idle assets.
#   - Added "suitable_for" field — lists cargo types this asset can carry.
#     Values: "general", "perishable", "hazardous", "heavy"
#     (a single asset can be suitable for multiple types)
# ---------------------------------------------------------------------------

FLEET_ASSETS = [
    # ---- Trucks ----
    {
        "id": "TRK-001",
        "type": "Truck",
        "location": "Mumbai Depot",
        "status": "Idle",
        "capacity_tons": 20,
        "suitable_for": ["general", "perishable"],
    },
    {
        "id": "TRK-002",
        "type": "Truck",
        "location": "Delhi Warehouse",
        "status": "In Use",
        "capacity_tons": 20,
        "suitable_for": ["general", "perishable"],
    },
    {
        "id": "TRK-003",
        "type": "Truck",
        "location": "Chennai Port",
        "status": "Idle",
        "capacity_tons": 30,
        "suitable_for": ["general", "heavy"],
    },
    {
        "id": "TRK-004",
        "type": "Truck",
        "location": "Kolkata Hub",
        "status": "In Use",
        "capacity_tons": 15,
        "suitable_for": ["general"],
    },

    # ---- Containers ----
    {
        "id": "CON-001",
        "type": "Container",
        "location": "Shanghai Terminal",
        "status": "Idle",
        "capacity_tons": 25,
        "suitable_for": ["general", "heavy"],
    },
    {
        "id": "CON-002",
        "type": "Container",
        "location": "Rotterdam Port",
        "status": "In Use",
        "capacity_tons": 25,
        "suitable_for": ["general", "heavy"],
    },
    {
        "id": "CON-003",
        "type": "Container",
        "location": "Dubai Freezone",
        "status": "Idle",
        "capacity_tons": 20,
        "suitable_for": ["general", "perishable"],   # refrigerated container
    },
    {
        "id": "CON-004",
        "type": "Container",
        "location": "Los Angeles Dock",
        "status": "Idle",
        "capacity_tons": 20,
        "suitable_for": ["hazardous"],               # certified for dangerous goods
    },

    # ---- Vessels ----
    {
        "id": "VSL-001",
        "type": "Vessel",
        "location": "Singapore Anchorage",
        "status": "Idle",
        "capacity_tons": 5000,
        "suitable_for": ["general", "heavy", "perishable"],
    },
    {
        "id": "VSL-002",
        "type": "Vessel",
        "location": "Hamburg Port",
        "status": "In Use",
        "capacity_tons": 8000,
        "suitable_for": ["general", "heavy"],
    },
    {
        "id": "VSL-003",
        "type": "Vessel",
        "location": "New York Harbor",
        "status": "In Use",
        "capacity_tons": 6000,
        "suitable_for": ["general", "perishable"],
    },
    {
        "id": "VSL-004",
        "type": "Vessel",
        "location": "Cape Town Port",
        "status": "Idle",
        "capacity_tons": 4000,
        "suitable_for": ["general", "hazardous"],    # hazmat-certified vessel
    },
]
