# data/shipments.py
# ---------------------------------------------------------------------------
# SupplyChain Guardian — Shipment & Route Data
# ---------------------------------------------------------------------------
# Stores all shipment records and the alternative-route lookup table.
#
# Changes from the original data.py:
#   - Added "cargo_type" field to every shipment.
#     This lets the Route Optimizer suggest cargo-appropriate alternatives.
#     Values: "general", "perishable", "hazardous", "heavy"
#
#   - ALTERNATIVE_ROUTES now maps to a dict per route instead of a plain list.
#     Each entry has:
#       "all"         → alternatives suitable for any cargo
#       "perishable"  → alternatives specifically suitable for cold-chain cargo
#       "hazardous"   → alternatives for chemicals / dangerous goods
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# SHIPMENTS
# Each shipment dictionary fields:
#   id          - unique identifier
#   origin      - departure location
#   destination - arrival location
#   route       - the corridor/waterway the shipment passes through
#   cargo       - what is being shipped (human-readable label)
#   cargo_type  - category: general | perishable | hazardous | heavy
#   status      - In Transit | Pending | Delayed
# ---------------------------------------------------------------------------

SHIPMENTS = [
    {
        "id": "SHP-001",
        "origin": "Shanghai",
        "destination": "New York",
        "route": "Suez Canal",
        "cargo": "Electronics",
        "cargo_type": "general",
        "status": "In Transit",
    },
    {
        "id": "SHP-002",
        "origin": "Mumbai",
        "destination": "Rotterdam",
        "route": "Suez Canal",
        "cargo": "Textiles",
        "cargo_type": "general",
        "status": "In Transit",
    },
    {
        "id": "SHP-003",
        "origin": "Los Angeles",
        "destination": "Tokyo",
        "route": "Pacific Ocean",
        "cargo": "Automotive Parts",
        "cargo_type": "heavy",
        "status": "In Transit",
    },
    {
        "id": "SHP-004",
        "origin": "Hamburg",
        "destination": "Dubai",
        "route": "Suez Canal",
        "cargo": "Machinery",
        "cargo_type": "heavy",
        "status": "Pending",
    },
    {
        "id": "SHP-005",
        "origin": "Singapore",
        "destination": "London",
        "route": "Strait of Malacca",
        "cargo": "Chemicals",
        "cargo_type": "hazardous",
        "status": "In Transit",
    },
    {
        "id": "SHP-006",
        "origin": "New York",
        "destination": "Cape Town",
        "route": "Atlantic Ocean",
        "cargo": "Medical Supplies",
        "cargo_type": "perishable",
        "status": "In Transit",
    },
    {
        "id": "SHP-007",
        "origin": "Dubai",
        "destination": "Mumbai",
        "route": "Suez Canal",
        "cargo": "Vaccines",
        "cargo_type": "perishable",
        "status": "In Transit",
    },
    {
        "id": "SHP-008",
        "origin": "Rotterdam",
        "destination": "Singapore",
        "route": "Suez Canal",
        "cargo": "Industrial Chemicals",
        "cargo_type": "hazardous",
        "status": "Pending",
    },
]


# ---------------------------------------------------------------------------
# ALTERNATIVE_ROUTES
# ---------------------------------------------------------------------------
# Maps a disrupted route to a dict of alternatives, split by cargo type.
#
# Keys inside each route entry:
#   "all"        → safe for any cargo type
#   "perishable" → preferred for cold-chain / time-sensitive cargo
#   "hazardous"  → certified for dangerous goods
#
# If a shipment's cargo_type has a specific key, that list is shown first.
# The "all" list is always shown as a fallback.
# ---------------------------------------------------------------------------

ALTERNATIVE_ROUTES = {
    "Suez Canal": {
        "all": [
            "Cape of Good Hope route (adds ~7-10 days, fully open)",
            "Trans-Siberian rail corridor (adds ~14 days, land-only)",
        ],
        "perishable": [
            "Air freight via Dubai Hub (fastest, premium cost)",
        ],
        "hazardous": [
            "Cape of Good Hope route — certified hazmat vessels available",
        ],
    },
    "Strait of Malacca": {
        "all": [
            "Lombok Strait (adds ~1-2 days, open to all vessels)",
            "Sunda Strait (shorter detour, smaller vessels only)",
        ],
        "perishable": [
            "Air freight via Singapore Changi (fastest option)",
        ],
        "hazardous": [
            "Lombok Strait — hazmat-cleared corridor",
        ],
    },
    "Pacific Ocean": {
        "all": [
            "Panama Canal route (adds ~3-5 days)",
            "Arctic Northern Sea Route (seasonal, ice-free months only)",
        ],
        "perishable": [
            "Air freight via Los Angeles LAX or Tokyo Narita",
        ],
        "hazardous": [
            "Panama Canal route — hazmat documentation required at entry",
        ],
    },
    "Atlantic Ocean": {
        "all": [
            "Cape Horn route (longer, suitable for bulk and heavy cargo)",
        ],
        "perishable": [
            "Air freight via JFK or Heathrow (recommended for cold chain)",
        ],
        "hazardous": [
            "Cape Horn route — consult port authority for hazmat clearance",
        ],
    },
}
