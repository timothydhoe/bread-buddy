# bread buddy

A sourdough calculator and bake planner for home bakers. Runs in the browser, installs as a PWA on iPhone and iPad, works offline.

## What it does

- **Recipe builder** — flour weight + baker's percentages for water, starter, and salt. Supports flour blends. Live ingredient breakdown in the sidebar.
- **Bake timeline** — enter when you want fresh bread; get a backwards-planned schedule from starter feeding to first slice, with "what to look for" cues at each step.
- **Step reminders** — browser notifications, 2 minutes before each timeline step. Works in the background when installed as a PWA.
- **Water temperature calculator** — DDT formula accounts for room temp, flour temp, starter temp, and friction factor.
- **Bulk fermentation adjuster** — adjusts time for your actual room temperature vs. the recipe's reference temp.
- **Starter feeding calculator** — target amount + feeding ratio → old starter, flour, water weights.
- **Bake log** — tap your outcome (Great / Good / OK / Disappointing), add an optional note. Stored locally.
- **The Science** and **Troubleshooting** reference pages.

## Running the app

```bash
# Activate the virtual environment first
source .venv/bin/activate

# Run the Flask development server
python app.py
```

The app runs at `http://127.0.0.1:5000` in debug mode.

If you get "Address already in use":
```bash
lsof -ti :5000 | xargs kill -9
```

## Running tests

```bash
pytest                              # all tests
pytest tests/test_foo.py            # single file
pytest tests/test_foo.py::test_bar  # single test
```

Tests are a planned TODO — none exist yet.

## Architecture

Single-page Flask app (`app.py`) with **no server-side state**. The Flask server is stateless — every request carries all the data it needs. Recipe state lives entirely in the client (`localStorage`). All bread calculation logic lives in the `models/` package; `app.py` handles only form parsing and rendering.

### State management

- **`localStorage['bb_last_state']`** — the current recipe form state, auto-saved after every sidebar recalculation. Restored on page load, so refresh never wipes your work.
- **`localStorage['bb_recipe_<name>']`** — named saved recipes (form-state format).
- **`localStorage['bb_bake_<iso-date>']`** — bake log entries.
- **`localStorage['bb_reminders']`** — scheduled step notification times.
- **`sessionStorage['bb_step_N']`** — timeline step checkbox state (checked/unchecked).

### Model hierarchy

- `Ingredient` — base unit: name, weight (grams), category, baker's percentage ratio, starter hydration
- `Recipe` — container of `Ingredient` objects; computes `total_flour_weight`, `total_liquid_weight`, `hydration_percentage`
- `Levain(Recipe)` — subclass for sourdough starters; adds feeding ratio tuple `(flour, water, starter)` and `calculate_feeding(target_amount)`
- `Dough(Recipe)` — wraps a recipe; adds `calculate_water_temperature()` and `calculate_fermentation_time()` (both stateless — don't read `self.recipe`)
- `BakeTimeline` — generates a list of `BakeStep` objects working backwards from a target datetime

`utils.py` — temperature conversions, time formatting, percentage helpers.

### Key domain conventions

- **All ratios are decimal fractions**: `0.70` = 70%, `0.02` = 2%.
- **All weights are in grams**, including liquids.
- **Baker's percentage**: flour is always 100%; all other ingredients are expressed relative to total flour weight.
- **Hydration calculation for starters**: `liquid_part = starter_weight × (hydration / (1 + hydration))`
- **Temperatures**: all internal calculations use Celsius. `utils.celsius_to_fahrenheit()` is available for display.
- **Ingredient categories**: `{"flour", "water", "salt", "starter", "fat", "sweetener", "other"}` — validated on construction.

### HTMX flow

Every form posts to a `/calculate/*` endpoint via HTMX and gets back an HTML partial. The endpoints are fully stateless — they read all inputs from the POST body and return rendered HTML. No Flask session is used.

The timeline form uses `hx-include="#bread-type-input, #starter-pct"` to pull those fields from the recipe form into the timeline POST.

### PWA

- `static/manifest.json` — app name, icons, theme colour, `display: standalone`
- `static/sw.js` — service worker: cache-first for static assets, network-first for `/calculate/*` endpoints, offline fallback for navigation
- `static/icons/` — 192px, 512px, and 180px (Apple touch) PNG icons

Install via Safari → Share → Add to Home Screen. Opens full-screen, works offline.

## Tech stack

| Layer | Choice |
|---|---|
| Backend | Flask (Python) |
| Templating | Jinja2 |
| Reactivity | HTMX 1.9 |
| Styling | Vanilla CSS (design tokens, ~2800 lines) |
| JS | Vanilla JS (~1200 lines, no framework) |
| State | localStorage + sessionStorage |
| Offline | Service Worker (Cache API) |

## Project structure

```
app.py                    Flask routes (stateless)
models/
  ingredient.py           Ingredient model
  recipe.py               Recipe model
  levain.py               Levain (starter) model
  dough.py                Dough model (DDT, fermentation calculations)
  timeline.py             BakeTimeline + BakeStep
  utils.py                Temperature conversions, time formatting
static/
  main.js                 All client-side logic
  style.css               Design system + component styles
  manifest.json           PWA manifest
  sw.js                   Service worker
  icons/                  App icons (192, 512, 180px PNG + source SVG)
templates/
  base.html               Layout shell, header, sidebar, PWA meta
  index.html              Main calculator page
  science.html            Fermentation science reference
  troubleshoot.html       Problem-solving guide
  bakes.html              Bake log page
  _recipe_summary.html    Sidebar partial (injected by HTMX)
  _bake_timeline.html     Timeline partial (injected by HTMX)
  _starter_result.html    Starter feeding result partial
  _water_temp_result.html Water temperature result partial
  _fermentation_result.html Fermentation time result partial
```

## Resources

> Leo M. (2022), *The Perfect Loaf: The Craft and Science of Sourdough Breads, Sweets, and More*. Clarkson Potter.
