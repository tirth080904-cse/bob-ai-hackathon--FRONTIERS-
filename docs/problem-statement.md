# Problem Statement

## A Disruption Is a Network Event, Not a Single-Shipment Event

When a major shipping corridor goes down — a geopolitical blockage on the Suez
Canal, a port closure at JNPT, a storm forcing vessels off the Strait of Malacca
— the impact is never limited to one shipment. The same corridor carries dozens
of active shipments simultaneously. Each of those shipments has a different cargo
type: general freight, heavy machinery, perishable food or medicine, or hazardous
chemicals. Each requires a different alternative route. Each alternative route may
or may not have a compatible idle fleet asset nearby that could take the cargo.
And for any perishable or pharma cargo on that route, temperature sensors may
already be recording excursions that are quietly compounding the damage while the
team is still arguing over which route to use.

A port closure is not one problem. It is four problems arriving simultaneously:

1. **Which shipments are exposed?** (Detection)
2. **What feasible alternative route exists for each cargo type?** (Route reasoning)
3. **Is there an idle, cargo-compatible fleet asset that can be redeployed?** (Fleet)
4. **Has any temperature-sensitive cargo already been compromised?** (Cold chain)

These four questions are deeply dependent on each other. Answering question 3
requires already knowing the answers to questions 1 and 2. Answering question 4
correctly changes the urgency ranking of questions 2 and 3 — a vaccine shipment
with a rising temperature alert needs a faster (air freight) alternative, not the
cheapest one. No question can be answered well in isolation.

---

## The Audience

R.E.A.C.T. is built for the operators who have to answer all four questions at
once, under time pressure, in a single working session. Based on the roles
modelled in `src/dashboard.html`, the platform serves three distinct users who
currently operate from separate tools:

| Role | Primary concern | What they currently lack |
|---|---|---|
| **Operations Director** (`ops.director`) | Situational overview — how many shipments are exposed, what is the severity, what is the recommended next action | A single summary that aggregates across route, fleet, and cold-chain state without switching between systems |
| **Fleet Commander** (`captain.india`) | Which idle assets are available, which are cargo-compatible, which can be redeployed today | A real-time idle/in-use breakdown that is already filtered by the cargo type of the affected shipment — not a raw fleet list |
| **Route Analyst** (`route.analyst`) | Which alternative corridors are open, whether they are certified for this cargo's hazard or perishability class, and what the added transit time is | An alternative-route lookup that is pre-filtered by cargo type, not a generic list of bypass options |

A fourth implicit audience sits across all three roles: **cold-chain and quality
managers** who monitor temperature sensor feeds for pharma and food shipments.
In the current data (`src/data/sensor_data.py`), five cargo categories are
tracked — vaccines (2–8 °C), frozen seafood (−25 to −15 °C), fresh produce
(2–6 °C), industrial chemicals (15–25 °C), and blood samples (2–6 °C) — each
with its own safe range and its own escalation threshold.

---

## Why Manual Spreadsheets Cannot Keep Up

A spreadsheet can record current shipment status. It cannot **recompute
dependencies** as new information arrives. Consider what happens when the
disruption location is changed from Suez Canal to Strait of Malacca:

- The set of affected shipments changes entirely (different route corridors are
  matched against each shipment's `route` field).
- The alternative routes change — Lombok Strait and Sunda Strait replace Cape of
  Good Hope; Singapore Changi replaces Dubai Hub for perishable cargo.
- The fleet compatibility matrix changes — idle assets at Singapore Anchorage
  (VSL-001) become relevant where they were not before.
- The cargo priority ranking changes — which shipment has the most urgent need
  for an air-freight option now depends on which shipments are actually on the
  newly disrupted corridor.
- Cold-chain alerts remain independent but need to be visible alongside the
  rerouting decision, not in a separate tab.

In a spreadsheet, each of these recomputations is a manual update. The Operations
Director must open a route spreadsheet, update it, copy results into a fleet
availability sheet, then check a separate cold-chain alert log, and finally
synthesise a recommendation — all before the situation changes again.

The problem is not that operators are slow or unskilled. The problem is that the
dependencies between these four data domains (shipment state, route alternatives,
fleet availability, cold-chain readings) are **programmatic, not human-scale**.
They need to be computed continuously, automatically, and presented as a single
connected view that updates the moment the disruption input changes.

---

## Specific Gaps This Project Addresses

| Gap | Evidence in `src/` |
|---|---|
| No cargo-type-aware route filtering | `src/data/shipments.py` — every shipment has a `cargo_type` field; `ALTERNATIVE_ROUTES` has separate keys for `perishable`, `hazardous`, and `all` |
| No idle/affected shipment cross-reference | `src/modules/fleet_optimizer.py` — `match_assets_to_shipments()` filters idle assets by `suitable_for` ∩ `cargo_type` |
| No severity grading for temperature breaches | `src/modules/cold_chain_monitor.py` — explicit three-tier classification with a 3 °C `WARNING_MARGIN` separating WARNING from CRITICAL |
| No single view connecting all four domains | `src/dashboard.html` — Operations Dashboard screen renders affected shipments, idle fleet count, cold-chain alert count, and priority next actions in one page; any change to the disruption selector re-renders all four simultaneously |
