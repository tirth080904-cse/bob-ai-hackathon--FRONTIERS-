# Solution Overview

## How R.E.A.C.T. Works — As Actually Implemented in `src/`

The platform is built around a single, linear reasoning pipeline that runs every
time the operator selects or changes the active disruption. Each stage feeds its
output directly into the next. There is no AI inference, no external API call, and
no database query — all four stages run in-process, either as Python functions
(CLI path via `src/main.py`) or as JavaScript functions in the browser (dashboard
path via `src/dashboard.html`). Both paths implement identical logic from the same
source-of-truth data.

---

## The Five-Stage Pipeline

### Stage 1 — Disruption Selection

The operator (or Guardian AI, via a chat command) selects one of four active
disruption zones:

| Disruption zone | Corridors covered |
|---|---|
| Suez Canal | Egypt – Red Sea passage |
| Strait of Malacca | Singapore – Indian Ocean chokepoint |
| Pacific Ocean | Trans-Pacific routes |
| Atlantic Ocean | Trans-Atlantic routes |

The selected zone is held as `currentDisruption` in the dashboard and as
`DISRUPTION_LOCATION` in `src/main.py`. Every downstream stage reads from this
single value — changing it re-runs the entire pipeline automatically.

---

### Stage 2 — Shipment Exposure Detection (`disruption_monitor.py`)

**What runs:**
[`detect_affected_shipments(disruption_location, disruption_reason)`](../src/modules/disruption_monitor.py)

**Exact logic:** a case-insensitive substring match of `disruption_location`
against each shipment's `route` field. If the disruption location string is
contained in the route string, the shipment is **Affected**; otherwise it is
**Safe**.

```
"Suez Canal" ∈ "Suez Canal"  → Affected  (SHP-001, SHP-002, SHP-004, SHP-007, SHP-008)
"Suez Canal" ∈ "Pacific Ocean" → Safe    (SHP-003)
```

**Output:** two lists — `affected` (mutable copies, ready to be enriched by
Stage 3) and `safe`. The Operations Dashboard immediately reflects these counts
in four headline metric cards: Affected Shipments, Safe Shipments, Idle Fleet
Assets, Cold-Chain Alerts.

**What this stage deliberately does not do:** it does not recommend routes. That
separation is explicit in the module's opening comment and enforced by the
function signature — `detect_affected_shipments` returns lists with no
`alternatives` key. Route reasoning is handled exclusively in Stage 3.

---

### Stage 3 — Cargo-Aware Route Recommendations (`route_optimizer.py`)

**What runs:**
[`recommend_routes(affected_shipments)`](../src/modules/route_optimizer.py)

**Exact logic:** for each affected shipment, the function looks up its `route`
key in `ALTERNATIVE_ROUTES` (defined in `src/data/shipments.py`). The lookup
table is a two-level dict:

```
ALTERNATIVE_ROUTES[route][cargo_type]  → cargo-specific alternatives (shown first)
ALTERNATIVE_ROUTES[route]["all"]       → universal alternatives (always appended)
```

Cargo-specific keys currently defined: `"perishable"` and `"hazardous"`. A
shipment whose `cargo_type` matches one of these keys receives those options
prepended before the universal fallbacks:

| `cargo_type` | Gets first | Then gets |
|---|---|---|
| `perishable` | Air freight option (fastest, time-sensitive) | Cape of Good Hope / Trans-Siberian / etc. |
| `hazardous` | Hazmat-certified corridor | Universal sea alternatives |
| `general` / `heavy` | *(no specific key)* | Universal alternatives only |

If a route is not in the lookup table at all, the shipment gets the string
`"No pre-defined alternative on file — manual review required"` — so the output
always has an `alternatives` key; no shipment is ever silently left without
guidance.

**Output:** the same `affected` list, each dict now enriched with an
`"alternatives"` key containing an ordered list of route recommendation strings.
This enriched list is what the Route Optimizer screen renders, and what the
Action Table on the Operations Dashboard uses for its "Recommended Action" column.

---

### Stage 4 — Fleet Compatibility Matching (`fleet_optimizer.py`)

**What runs:**
[`find_idle_assets(assets)`](../src/modules/fleet_optimizer.py) →
[`match_assets_to_shipments(idle_assets, affected_shipments)`](../src/modules/fleet_optimizer.py)

**Exact logic, step by step:**

1. `find_idle_assets` filters the full fleet list (`src/data/fleet_data.py`,
   12 assets across trucks, containers, and vessels) to only those where
   `status == "Idle"`.

2. `match_assets_to_shipments` iterates over every affected shipment and, for
   each, filters the idle list to assets whose `suitable_for` list contains that
   shipment's `cargo_type`. This produces a dict keyed by shipment ID:

   ```
   { "SHP-007": [CON-003, VSL-001], "SHP-002": [CON-001, VSL-001], ... }
   ```

3. If no idle asset is compatible with a shipment's cargo type, the entry maps to
   an empty list and the report states "No compatible idle asset found — manual
   sourcing needed."

**Asset types and locations in the current data:**

| Type | Locations | Cargo capabilities |
|---|---|---|
| Truck | Mumbai Depot, Delhi Warehouse, Chennai Port, Kolkata Hub | general, perishable, heavy |
| Container | Shanghai Terminal, Rotterdam Port, Dubai Freezone, Los Angeles Dock | general, heavy, perishable (CON-003 is refrigerated), hazardous (CON-004 certified) |
| Vessel | Singapore Anchorage, Hamburg Port, New York Harbor, Cape Town Port | general, heavy, perishable, hazardous |

**Output:** a `matches` dict fed directly into the Action Table (which fleet asset
is available per affected shipment) and the Fleet Optimizer screen (redeployment
recommendation section).

---

### Stage 5 — Cold-Chain Temperature Classification (`cold_chain_monitor.py`)

**What runs:**
[`analyse_all_readings(readings)`](../src/modules/cold_chain_monitor.py)
→ [`classify_reading(reading)`](../src/modules/cold_chain_monitor.py) per reading

**Exact logic:** each reading has a `temperature`, `temp_min`, and `temp_max`.
The breach amount is calculated as degrees outside the safe range. Classification
uses a single constant — `WARNING_MARGIN = 3.0` °C — as the threshold:

```
breach == 0             → NORMAL   (temperature within range)
0 < breach ≤ 3.0 °C    → WARNING  ("monitor closely — cargo may be at risk")
breach > 3.0 °C         → CRITICAL ("immediate action required — cargo integrity compromised")
```

Direction is also recorded (`TOO HIGH` / `TOO LOW` / `OK`), producing a
plain-English reason string with the exact temperature and the safe range
quoted — so the operator sees not just a status badge but the numbers that
produced it.

**Current sensor data** covers five shipments and 11 readings:

| Shipment | Cargo | Safe range | Worst status in data |
|---|---|---|---|
| SHP-101 | Vaccines | 2–8 °C | CRITICAL (14.5 °C → +6.5 °C breach) |
| SHP-102 | Frozen Seafood | −25 to −15 °C | WARNING (−13.5 °C → +1.5 °C breach) |
| SHP-103 | Fresh Produce | 2–6 °C | WARNING (1.0 °C → −1.0 °C breach) |
| SHP-104 | Industrial Chemicals | 15–25 °C | CRITICAL (42.0 °C → +17.0 °C breach) |
| SHP-105 | Blood Samples | 2–6 °C | NORMAL (both readings within range) |

**Output:** a `grouped` dict (shipment ID → list of classified readings). The
worst status per shipment drives the badge count in the sidebar (`nav-badge-dis`,
`nav-badge` on the Cold-Chain nav button) and the Cold-Chain Alerts table on the
Operations Dashboard.

---

## The Connected View — What Makes This Different from a Static Tool

A static spreadsheet or a plain map with shipment pins answers at most one
question per view. R.E.A.C.T.'s Operations Dashboard answers all five at once and
keeps them consistent:

```
[ Disruption selector ]
        │
        ▼
[ Stage 2: Affected vs Safe count ]───────────────────────┐
        │                                                  │
        ▼                                                  ▼
[ Stage 3: Alternative routes per shipment ]    [ Stage 4: Idle fleet + match ]
        │                                                  │
        └──────────────────────────┬───────────────────────┘
                                   ▼
                    [ Action Table: shipment + action + fleet ]
                                   │
                    [ Stage 5: Cold-chain alerts table ]
                                   │
                    [ Priority Actions: next recommended step ]
```

The key difference from a naive alternative is **recomputation on a single
input change**. Switching the disruption selector from "Suez Canal" to "Strait
of Malacca" triggers a single call that re-runs all five stages and re-renders
every card, table, map layer, badge, and sidebar count in one pass. The operator
sees a consistent state across all panels, not a patchwork of figures from
different manual updates at different times.

The Live Route Map adds spatial context: disrupted corridors render in red,
alternative routes in green, safe routes in blue, Indian port and depot pins
pinned by name — all driven by the same disruption selector, so the map always
matches the tables.

---

## The Guardian AI Assistant — What It Actually Is

The floating chat widget (`src/dashboard.html`, `guardianAI()` function) is a
**client-side, keyword-based response engine** — there is no call to IBM
watsonx.ai, IBM Bob, or any external API. It uses `q.match(/regex/)` pattern
matching to route the user's lowercase query to one of ~15 response branches,
each of which reads from the same JavaScript data arrays and computed state
(affected shipments, idle fleet, cold-chain alerts) that the rest of the
dashboard already holds.

What it can answer correctly, because it reads live computed state:
- How many shipments are affected / safe right now
- Details for a specific shipment ID (e.g. "SHP-007")
- Which fleet assets are idle and their locations
- Alternative routes for the active disruption, split by cargo type
- Cold-chain alert count and per-cargo temperatures
- A compact dashboard summary
- Switch the active disruption zone, which re-renders the entire dashboard

What it cannot do:
- Maintain context across turns (each message is stateless)
- Answer free-form questions outside its ~15 matched patterns
- Connect to any live external data source
- Use natural language understanding

**IBM watsonx.ai / Bob integration is not present in this version of the code and
is the explicitly planned next step.** This is not a gap to hide — it is the
single most impactful upgrade on the roadmap.

---

## What Is Not in `src/` (Honest Scope Statement)

| Item | Status |
|---|---|
| Live AIS / port-authority data feed | Not present — all shipment, fleet, and sensor data is hardcoded in `src/data/` |
| Backend server / API | Not present — the dashboard opens as a local HTML file; `src/main.py` is a CLI, not an HTTP server |
| Database or persistence layer | Not present — state resets on page reload |
| Authentication | Login screen is cosmetic only; no session validation exists in the code |
| Indian coastal / road-freight route data | Not modelled — four global sea corridors only |
| IBM watsonx.ai or LLM integration | Not present — Guardian AI is vanilla JS keyword matching |
