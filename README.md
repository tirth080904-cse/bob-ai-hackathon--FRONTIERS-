# R.E.A.C.T. — Resilient Engine for Adaptive Cargo & Transport

> **IBM Bob AI Hackathon — FRONTIERS**
> A supply-chain control tower for India operations: one view that connects
> disruption detection → shipment exposure → alternative routes → fleet
> redeployment → cold-chain temperature status.

---

## Team

| Field | Value |
|---|---|
| **Team name** | Frontiers |
| **Track** | AI |
| **Team lead** | Tirth Makwana — tirth080904@gmail.com |
| **Members** | Tirth Makwana, Kunj Patel (kunj275patel@gmail.com), Mihir Rana (ranamihir2008@gmail.com), Jaini Khandhar (jaini.khandhar@gmail.com) |

---

## Problem Statement

Global and India-focused supply chains face frequent, high-impact disruptions —
port closures, geopolitical route blockages (e.g. Suez Canal), and carrier
shortages — that operators currently manage reactively and in silos. There is no
single interface that simultaneously shows which active shipments are exposed,
which fleet assets are available to redeploy, whether perishable or pharma cargo
is still within safe temperature ranges, and what alternative routes are feasible
for each cargo type. The result is costly delays, spoiled cargo, and decisions
made without full situational awareness.

---

## Solution

R.E.A.C.T. is a single-page, browser-based supply-chain control tower for India
operations. It combines four analytical engines — disruption detection,
cargo-aware route optimisation, fleet utilisation, and cold-chain temperature
monitoring — surfaced through six dedicated screens and a live interactive map,
with a conversational "Guardian AI" assistant that operators can query in plain
English. All logic runs client-side with no installation required; the same
engines are also available as a standalone Python CLI (`src/main.py`).

---

## Key Features

### 1 · Disruption Monitor
Scans all active shipments and classifies each as **Affected** or **Safe** based
on whether its route corridor (Suez Canal, Strait of Malacca, Pacific Ocean,
Atlantic Ocean) matches the active disruption location. The sidebar permanently
shows the current disruption zone and reason; the Disruption Monitor screen
lists every exposed shipment with origin, destination, cargo type, and status.

### 2 · Cargo-Aware Route Optimizer
For every affected shipment, recommends alternative routes **tailored to the
cargo type** (general, perishable, hazardous, heavy). Perishable shipments
receive air-freight options first (e.g. air via Dubai Hub or Singapore Changi);
hazardous cargo receives hazmat-certified corridor alternatives. Universal
fallbacks (Cape of Good Hope, Trans-Siberian rail, Lombok Strait, Panama Canal)
are always appended so no shipment is ever left without an option.

### 3 · Fleet Optimizer with Cargo-Compatibility Matching
Identifies all **Idle** fleet assets (trucks, reefer containers, hazmat-certified
vessels) across Indian depots and global ports, then matches each idle asset to
affected shipments by comparing the asset's `suitable_for` list against the
shipment's `cargo_type`. Produces a redeployment recommendation table so
operators can act on idle capacity immediately.

### 4 · Cold-Chain Monitor — Three-Tier Temperature Classification
Classifies every sensor reading for sensitive cargo (vaccines, frozen seafood,
fresh produce, blood samples, industrial chemicals) as **NORMAL**, **WARNING**,
or **CRITICAL**. Warning triggers when the breach is ≤ 3 °C outside the safe
range; Critical triggers above 3 °C, prompting immediate action. Alert badge
counts in the sidebar reflect the worst reading per shipment in real time.

### 5 · Guardian AI Conversational Assistant
A floating chat widget that operators can query in plain English — no external
API, no server call. It answers questions about affected/safe shipments, specific
shipment details by ID, idle fleet and vessel counts, India port status (JNPT,
Chennai, Cochin, Mundra, Kolkata), alternative routes, cold-chain alerts, and
full dashboard summaries. It also switches the active disruption zone (Suez,
Malacca, Pacific, Atlantic, Arabian Sea) on command, re-rendering the entire
dashboard in response.

> **Honest note:** Guardian AI is currently a **rule-based, client-side keyword
> matcher** built entirely in vanilla JavaScript inside `src/dashboard.html`.
> There is **no IBM Bob / watsonx.ai integration** in the codebase at this time.
> Replacing the keyword engine with a real IBM watsonx.ai or Bob-powered LLM
> backend is the top-priority next step.

---

## Tech Stack

Everything that is **actually present in `src/`** — nothing assumed:

| Layer | Technology | Version / Notes |
|---|---|---|
| Dashboard UI | HTML5 + CSS3 + Vanilla JavaScript | Single self-contained file (`src/dashboard.html`) |
| Interactive map | [Leaflet.js](https://leafletjs.com/) | 1.9.4 via unpkg CDN |
| Map tiles | OpenStreetMap (via Leaflet default tile layer) | Loaded at runtime |
| Typography | Inter & Nunito | Google Fonts CDN |
| Python CLI | Python 3 | `src/main.py` + four modules under `src/modules/` |
| Python data layer | Plain Python dicts / lists | `src/data/` — no database, no ORM |
| Dark / Light theme | CSS custom properties (`data-theme` attribute toggle) | No framework |
| No build tool | — | No npm, webpack, bundler, or transpiler |
| No backend | — | App opens directly as a local HTML file |
| No external AI API | — | Guardian AI is vanilla JS keyword matching |

---

## Repository Structure

```
src/
├── dashboard.html          ← R.E.A.C.T. single-page app (open in any browser)
├── main.py                 ← Python CLI entry point
├── data/
│   ├── fleet_data.py       ← Fleet asset records (trucks, containers, vessels)
│   ├── sensor_data.py      ← Cold-chain temperature sensor readings
│   └── shipments.py        ← Shipment records + ALTERNATIVE_ROUTES lookup table
└── modules/
    ├── disruption_monitor.py   ← Module 1: shipment exposure detection
    ├── route_optimizer.py      ← Module 2: cargo-aware alternative routes
    ├── fleet_optimizer.py      ← Module 3: idle asset detection + matching
    └── cold_chain_monitor.py   ← Module 4: temperature classification
submission.yaml
README.md
```

---

## How to Run

See **[`docs/setup-guide.md`](docs/setup-guide.md)** for full setup instructions.

**Quick start (browser):**
Open `src/dashboard.html` directly in any modern browser — no installation,
no server, no build step required. An internet connection is needed to load
Leaflet tiles and Google Fonts from CDN.

**Quick start (Python CLI):**
```bash
cd src
python main.py
```
Python 3.8+ required. No external packages needed.

---

## Demo

- **Video:** see [`demo/demo-video-link.txt`](demo/demo-video-link.txt)
- **Screenshots:** see [`demo/screenshots/`](demo/screenshots/)

---

## What We're Most Proud Of

The **end-to-end connected pipeline in a single view**: a single disruption event
— say, a Suez Canal blockage — immediately cascades through every layer of the
platform. You can see which shipments are exposed, which feasible alternative
routes exist for each specific cargo type, which idle fleet assets at Indian
depots can be redeployed to cover the gap, and whether any of those shipments'
perishable cargo has already breached safe temperature thresholds — all without
switching screens. That chain of reasoning (disruption → exposure → route →
fleet → cold-chain) is what "control tower" actually means, and it is fully
wired in both the browser dashboard and the Python CLI.

---

## Known Limitations

- **No real AI / LLM integration.** Guardian AI is a client-side keyword
  matcher. IBM watsonx.ai / Bob integration is planned as the next step.
- **Static data.** Shipment, fleet, and sensor records are hardcoded Python
  dicts and JavaScript arrays — there is no live data feed or database
  connection.
- **No authentication / multi-user support.** The login screen in the
  dashboard is purely cosmetic; there is no backend session management.
- **No persistence.** Changing the active disruption zone via the UI or
  Guardian AI resets on page reload.
- **Demo scope.** Route corridor data covers four major global corridors
  (Suez Canal, Strait of Malacca, Pacific Ocean, Atlantic Ocean). Indian
  coastal and road-freight routes are not yet modelled.

---

## Next Steps

1. Replace Guardian AI keyword engine with **IBM watsonx.ai / Bob** for natural
   language understanding and contextual multi-turn conversation.
2. Connect to **live AIS / port-authority feeds** for real shipment tracking.
3. Add a **lightweight backend** (e.g. FastAPI) to persist disruption events,
   fleet state changes, and cold-chain readings across sessions.
4. Expand route data to cover **Indian coastal shipping** and road-freight
   corridors between major depots.

---

*Built for the IBM Bob AI Hackathon — FRONTIERS.*
