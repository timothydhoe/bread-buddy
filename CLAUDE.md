# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Package manager

This project uses [uv](https://docs.astral.sh/uv/). Dependencies are declared in `pyproject.toml`; the lock file is `uv.lock`.

```bash
uv sync                  # install/sync dependencies
uv run python app.py     # run without activating venv manually
```

## Running the app

```bash
# Activate the virtual environment first
source .venv/bin/activate

# Run the Flask development server
python app.py
```

The app runs at `http://127.0.0.1:5000` in debug mode.

If port 5000 is already in use (e.g. from a previous session):
```bash
lsof -ti :5000 | xargs kill -9
```

## Running tests

```bash
pytest                        # all tests
pytest tests/test_foo.py      # single file
pytest tests/test_foo.py::test_bar  # single test
```

Tests don't exist yet — they're a planned TODO.

## Architecture

Single-page Flask app (`app.py`) with **no server-side session state**. The server is stateless — every request is self-contained. All recipe state lives in the client (`localStorage`). Bread calculation logic lives in `models/`; `app.py` handles only form parsing and rendering.

### State ownership

**The client owns all state.** There is no `session['recipe']` or any Flask session usage.

- `localStorage['bb_last_state']` — current recipe form state, saved after every sidebar HTMX swap, restored on page load
- `localStorage['bb_recipe_<name>']` — named saved recipes (form-state format, not Recipe model dicts)
- `localStorage['bb_bake_<iso>']` — bake log entries
- `localStorage['bb_reminders']` — scheduled step notification timestamps
- `sessionStorage['bb_step_N']` — timeline step checkbox state

### HTMX flow

Every form posts to a `/calculate/*` endpoint via HTMX and receives an HTML partial in return. Endpoints read all inputs from the POST body — nothing from session.

The timeline form uses `hx-include="#bread-type-input, #starter-pct"` to pull recipe fields into the POST so the server knows the bread type and starter percentage without session.

After every sidebar swap (`htmx:afterSwap` on `#recipe-sidebar`), JS calls `saveLastState()` to persist the current form state to localStorage. On page load, `restoreFormState()` reads `bb_last_state` and triggers an HTMX recalculation.

### Model hierarchy

- `Ingredient` — base unit: name, weight (grams), category, baker's percentage ratio, starter hydration
- `Recipe` — container of `Ingredient` objects; computes `total_flour_weight`, `total_liquid_weight`, `hydration_percentage`
- `Levain(Recipe)` — subclass for sourdough starters; adds feeding ratio tuple `(flour, water, starter)` and `calculate_feeding(target_amount)`
- `Dough(Recipe)` — wraps a recipe; adds `calculate_water_temperature()` and `calculate_fermentation_time()`. Note: neither method reads `self.recipe` — they operate only on their passed parameters. `app.py` uses `_EMPTY_DOUGH = Dough(Recipe("_"))` as a stateless singleton.
- `BakeTimeline` — generates a list of `BakeStep` objects, working backwards from a target datetime

`utils.py` — temperature conversions, time formatting, percentage helpers.

### Key domain conventions

- **All ratios are decimal fractions**: `0.70` = 70%, `0.02` = 2%. Never use raw percentages in model code.
- **All weights are in grams**, including liquids.
- **Baker's percentage**: flour is always 100%; all other ingredients are expressed relative to total flour weight.
- **Hydration calculation for starters**: `liquid_part = starter_weight × (hydration / (1 + hydration))` — extracts the water fraction from a starter of known hydration.
- **Temperatures**: all internal calculations use Celsius. `utils.celsius_to_fahrenheit()` is available for display.
- **Ingredient categories**: `{"flour", "water", "salt", "starter", "fat", "sweetener", "other"}` — validated on construction.

### PWA

- `static/manifest.json` — app name, icons, theme colour, `display: standalone`
- `static/sw.js` — service worker: cache-first for `/static/*`, network-first for `/calculate/*`, offline fallback for navigation
- `static/icons/` — 192px and 512px PNGs plus 180px Apple touch icon, generated from `icon.svg`
- Registered in `base.html` via an inline `<script>` in `<head>`

### Notifications (Phase 3)

Timeline step elements carry `data-step-time`, `data-step-date`, `data-step-label`, `data-step-cue` attributes. After timeline generation, `initReminders()` is called from `htmx:afterSwap`. The "Set step reminders" button calls `scheduleReminders()` which reads those data attributes, requests `Notification` permission, schedules `setTimeout` callbacks, and optionally uses `registration.showNotification()` via the service worker for background delivery.

### Saved recipe format (localStorage)

Named recipes are stored as **form-state objects**, not Recipe model dicts:

```js
{
  flour_weight: 500,
  hydration: 72,
  starter_pct: 10,
  salt_pct: 2,
  bread_type: "freestanding",
  loaf_count: 1,
  recipe_name: "My Sourdough",
  notes: "",
  flour_blend: [{ name: "Bread flour", weight: 400 }, ...],  // optional
}
```

`normaliseStoredState()` in `main.js` handles legacy recipes stored in the old Recipe model dict format (with an `ingredients` array) and converts them to form-state format on load.

### Progressive disclosure

Sections `#section-starter`, `#section-params`, and `#section-timeline` start with the CSS class `section-locked` (dim + hint badge). The class is removed by `unlockSections()` which is called in the `htmx:afterSwap` handler for `#recipe-sidebar`. This is visual guidance only — not a hard gate.

### Mobile sidebar

On screens ≤ 900px, the sidebar becomes a fixed bottom sheet (CSS: `position: fixed; bottom: 0; max-height: 0` → `max-height: 75vh` when `.is-open`). A floating "Your Recipe" FAB button (`.recipe-fab`) toggles it. `toggleSidebarSheet()` and `closeSidebarSheet()` in `main.js` manage state.
