## Prerequisites

| Requirement | Dashboard (browser) | Python CLI |
|---|---|---|
| Modern browser (Chrome, Firefox, Edge, Safari) | âœ… Required | â€” |
| Internet connection | âœ… Required (CDN assets) | âŒ Not needed |
| Python 3.8 or later | â€” | âœ… Required |
| `pip install` / third-party packages | âŒ None needed | âŒ None needed |
| Node.js / npm / build tool | âŒ Not needed | âŒ Not needed |
| Web server / localhost | âŒ Not needed | âŒ Not needed |
| API key of any kind | âŒ None required | âŒ None required |

The dashboard opens directly as a local file â€” there is no build step, no server
to start, and no environment variables to set. The Python CLI uses only the
Python standard library.

---

## Option A â€” Run the Dashboard in a Browser

This is the primary way to use R.E.A.C.T.

**Step 1.** Locate the file:

```
src/dashboard.html
```

**Step 2.** Open it in any modern browser using one of these methods:

- **Double-click** `dashboard.html` in Windows Explorer / Finder.
- **Drag and drop** the file onto an open browser window.
- **Paste the full path** into the browser address bar:
  ```
  C:\Users\darji\Downloads\supplychain_guardian\src\dashboard.html
  ```
  (adjust the path to wherever you cloned the repo)
- From a terminal, on Windows:
  ```powershell
  Start-Process "src\dashboard.html"
  ```
  On macOS/Linux:
  ```bash
  open src/dashboard.html
  # or
  xdg-open src/dashboard.html
  ```

**Step 3.** The login screen appears. Use any of the three demo accounts:

| Username | Access code | Role |
|---|---|---|
| `captain.india` | `guardian2024` | Fleet Commander |
| `route.analyst` | `route123` | Route Analyst |
| `ops.director` | `ops2024` | Operations Director |

Click **âš“ Board the Bridge** (or click one of the "Use" quick-access buttons)
to enter the Operations Dashboard.

> **That's it.** No install, no server, no keys.

---

## Option B â€” Run the Python CLI

The Python CLI provides the same four analytical modules as a terminal menu.

**Step 1.** Confirm Python 3.8+ is installed:

```bash
python --version
# or, on some systems:
python3 --version
```

**Step 2.** Navigate to `src/` and run `main.py`:

```bash
cd src
python main.py
```

> **Important:** run from inside `src/`, not from the repo root. The module
> imports (`from modules.disruption_monitor import ...`, `from data.fleet_data
> import ...`) use relative package paths that resolve correctly only when
> `main.py` is run with `src/` as the working directory. Running
> `python src/main.py` from the repo root will raise a `ModuleNotFoundError`.

**Step 3.** The interactive menu appears:

```
=================================================================
   SupplyChain Guardian
   Supply Chain Disruption & Fleet Intelligence Platform
=================================================================
   Active Disruption : Suez Canal
   Reason            : Geopolitical conflict causing route blockage
=================================================================

  Select a module to run:

    [1]  Disruption Monitor      â€” Detect affected shipments
    [2]  Route Optimizer         â€” Alternative route recommendations
    [3]  Fleet Optimizer         â€” Idle asset detection
    [4]  Cold Chain Monitor      â€” Temperature excursion alerts
    [5]  Operations Dashboard    â€” Compact summary (all modules)
    [0]  Exit
```

Enter a number and press Enter.

**To simulate a different disruption**, edit the two constants near the top of
`src/main.py` before running:

```python
DISRUPTION_LOCATION = "Strait of Malacca"   # change this
DISRUPTION_REASON   = "Port workers' strike causing vessel backlog"  # and this
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| **Map is blank / grey** | No internet connection â€” Leaflet tiles are loaded from OpenStreetMap CDN at runtime | Connect to the internet and reload the page. There is no offline tile cache. |
| **Map loads but fonts look wrong** | No internet connection â€” Inter and Nunito are loaded from Google Fonts CDN | Connect to the internet. The UI is fully functional with system fallback fonts; only the visual appearance differs. |
| **Login screen appears but "Board the Bridge" does nothing** | JavaScript is disabled in the browser | Enable JavaScript. The entire app is a JS application; it cannot run without it. |
| **`ModuleNotFoundError: No module named 'modules'`** | Python CLI run from the repo root instead of `src/` | `cd src` first, then `python main.py`. |
| **`ModuleNotFoundError: No module named 'data'`** | Same cause as above | `cd src` first, then `python main.py`. |
| **`SyntaxError` or `IndentationError` on Python import** | Python version older than 3.8 (f-strings require 3.6+; some walrus-operator style patterns require 3.8+) | Upgrade to Python 3.8 or later. |
| **Disruption selector change has no effect** | Browser has cached an older version of `dashboard.html` | Hard-reload: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (macOS). |
| **Cold-chain alert badge shows wrong count** | Not a bug â€” badge reflects the number of shipments with at least one non-NORMAL reading, not the total number of readings | Expected behaviour. See `src/modules/cold_chain_monitor.py` for classification logic. |

---

## File Layout Reference

```
src/
â”œâ”€â”€ dashboard.html          â† open this in a browser to run the full UI
â”œâ”€â”€ main.py                 â† run this with Python for the CLI
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ fleet_data.py       â† fleet asset records
â”‚   â”œâ”€â”€ sensor_data.py      â† cold-chain sensor readings
â”‚   â””â”€â”€ shipments.py        â† shipment records + route alternatives table
â””â”€â”€ modules/
    â”œâ”€â”€ disruption_monitor.py
    â”œâ”€â”€ route_optimizer.py
    â”œâ”€â”€ fleet_optimizer.py
    â””â”€â”€ cold_chain_monitor.py
```

---

## What Requires an Internet Connection?

Only two things, both in the browser path:

| Asset | Source | Effect if offline |
|---|---|---|
| Leaflet.js 1.9.4 + CSS | `unpkg.com` | Map panel is blank; all other screens work normally |
| Inter + Nunito fonts | Google Fonts | UI falls back to system-ui sans-serif; layout is unaffected |

The Python CLI has **no network dependency whatsoever**.
