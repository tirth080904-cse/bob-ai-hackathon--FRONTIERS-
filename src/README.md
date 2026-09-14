# src/ — Source Code

This folder contains the complete R.E.A.C.T. application in two independently
runnable forms: a browser dashboard and a Python CLI. Both implement the same
four analytical modules against the same data.

## How to run

- **Browser:** open `dashboard.html` directly in any modern browser — no server,
  no build step, no install required.
- **Python CLI:** `cd src && python main.py` (Python 3.8+, no third-party
  packages needed).

See [`docs/setup-guide.md`](../docs/setup-guide.md) for full instructions and
troubleshooting.

---

## Folder structure

```
src/
├── dashboard.html      Single-page browser app — all six screens, the Leaflet
│                       map, and the Guardian AI chat widget in one self-contained
│                       HTML/CSS/JS file. Contains its own inline copies of the
│                       data and logic so it runs without a server.
│
├── main.py             Python CLI entry point. Interactive menu that lets you
│                       run any of the four modules individually or as a combined
│                       Operations Dashboard summary.
│
├── data/               Static data records (Python dicts/lists — no database).
│   ├── __init__.py
│   ├── shipments.py    8 active shipment records (origin, destination, route,
│   │                   cargo, cargo_type, status) + the ALTERNATIVE_ROUTES
│   │                   lookup table keyed by corridor and cargo type.
│   ├── fleet_data.py   12 fleet asset records (trucks, containers, vessels)
│   │                   with status, capacity_tons, and suitable_for list.
│   └── sensor_data.py  12 cold-chain temperature readings across 5 shipments
│                       (vaccines, frozen seafood, fresh produce, industrial
│                       chemicals, blood samples), each with a safe-range pair.
│
└── modules/            Four analytical modules, each independently runnable.
    ├── __init__.py
    ├── disruption_monitor.py   Module 1 — detects which shipments are exposed
    │                           to the active disruption (route substring match).
    ├── route_optimizer.py      Module 2 — cargo-aware alternative route
    │                           recommendations (perishable/hazardous first,
    │                           universal fallbacks always appended).
    ├── fleet_optimizer.py      Module 3 — idle asset detection and cargo-
    │                           compatibility matching to affected shipments.
    └── cold_chain_monitor.py   Module 4 — three-tier temperature classification
                                (NORMAL / WARNING / CRITICAL, 3 °C threshold).
```

---

## Module dependency map

```
main.py
 ├── modules/disruption_monitor  ←  data/shipments
 ├── modules/route_optimizer     ←  data/shipments  (ALTERNATIVE_ROUTES)
 ├── modules/fleet_optimizer     ←  data/fleet_data
 └── modules/cold_chain_monitor  ←  data/sensor_data
```

`dashboard.html` re-implements the same pipeline in JavaScript (inline, no
imports). Changes to `src/data/` must be manually reflected in the JS data
arrays inside `dashboard.html`.

---

## No environment variables, no API keys

Neither the dashboard nor the Python CLI reads any environment variable or
requires any API key. The Leaflet map uses OpenStreetMap tiles loaded from CDN —
no token required. There is no `.env` file.
