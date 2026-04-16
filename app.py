"""
filename: app.py
----------------

Flask application for Bread Buddy.
All bread calculation logic lives in models/. This file handles only
routing, form parsing, and rendering. No session state — the client
(localStorage) owns all recipe state.
"""

import json
from datetime import datetime

from flask import Flask, render_template, request

from models.dough import Dough
from models.ingredient import Ingredient
from models.levain import Levain
from models.recipe import Recipe
from models.timeline import BakeTimeline


app = Flask(__name__)
app.secret_key = 'bread-buddy-secret-key-change-in-production'

# Default recipe values per bread type, based on The Sourdough Framework
BREAD_TYPE_DEFAULTS = {
    "flatbread":    {"hydration": 80, "starter_pct": 10, "salt_pct": 2},
    "loaf_pan":     {"hydration": 75, "starter_pct": 10, "salt_pct": 2},
    "freestanding": {"hydration": 70, "starter_pct": 10, "salt_pct": 2},
}

_EMPTY_DOUGH = Dough(Recipe("_"))   # stateless helper — never reads self.recipe


# ── Main page ─────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    """Render the main page with hardcoded defaults.
    Client-side JS will restore any saved state from localStorage immediately.
    """
    flour_weight = 500.0
    hydration    = 70.0
    starter_pct  = 10.0
    salt_pct     = 2.0
    bread_type   = 'freestanding'

    recipe = Recipe.from_bakers_percentage('My Sourdough', flour_weight, {
        'water': hydration / 100, 'starter': starter_pct / 100, 'salt': salt_pct / 100,
    })
    hints = recipe.hints(bread_type)

    return render_template('index.html',
        recipe=recipe,
        bread_type=bread_type,
        hints=hints,
        flour_weight=flour_weight,
        hydration=hydration,
        starter_pct=starter_pct,
        salt_pct=salt_pct,
    )


# ── HTMX partial routes ───────────────────────────────────────────────────────

@app.route('/calculate/recipe', methods=['POST'])
def calculate_recipe():
    """Recalculate recipe from baker's percentages. Returns sidebar partial."""
    try:
        hydration   = float(request.form.get('hydration', 70)) / 100
        starter_pct = float(request.form.get('starter_pct', 10)) / 100
        salt_pct    = float(request.form.get('salt_pct', 2)) / 100
        bread_type  = request.form.get('bread_type', 'freestanding')
        loaf_count  = int(request.form.get('loaf_count', 1) or 1)

        # Check for multi-flour blend (flour_0_name / flour_0_weight, …)
        flour_rows, i = [], 0
        while request.form.get(f'flour_{i}_name'):
            w = float(request.form.get(f'flour_{i}_weight') or 0)
            if w > 0:
                flour_rows.append({'name': request.form[f'flour_{i}_name'], 'weight': w * loaf_count})
            i += 1

        if flour_rows:
            recipe = Recipe('My Sourdough')
            for f in flour_rows:
                recipe.add_ingredient(Ingredient(f['name'], f['weight'], 'flour'))
            flour_weight = recipe.total_flour_weight
            recipe.add_ingredient(Ingredient('water',   flour_weight * hydration,   'water'))
            recipe.add_ingredient(Ingredient('starter', flour_weight * starter_pct, 'starter'))
            recipe.add_ingredient(Ingredient('salt',    flour_weight * salt_pct,    'salt'))
        else:
            flour_weight = float(request.form.get('flour_weight', 500)) * loaf_count
            recipe = Recipe.from_bakers_percentage('My Sourdough', flour_weight, {
                'water': hydration, 'starter': starter_pct, 'salt': salt_pct,
            })

        # Parse custom "other" ingredients (other_0_name / other_0_weight, …)
        j = 0
        while request.form.get(f'other_{j}_name'):
            name = request.form[f'other_{j}_name'].strip()
            w = float(request.form.get(f'other_{j}_weight') or 0)
            if name and w > 0:
                recipe.add_ingredient(Ingredient(name, w * loaf_count, 'other'))
            j += 1

        hints = recipe.hints(bread_type)
        input_hydration = round(float(request.form.get('hydration', 70)), 1)
        return render_template('_recipe_summary.html', recipe=recipe, error=None,
                               hints=hints, bread_type=bread_type,
                               input_hydration=input_hydration)
    except (ValueError, TypeError) as e:
        return render_template('_recipe_summary.html', recipe=None, error=str(e),
                               hints=[], bread_type='freestanding')


@app.route('/calculate/water-temp', methods=['POST'])
def calculate_water_temp():
    """Calculate DDT water temperature. Returns inline result partial."""
    try:
        temp_unit = request.form.get('temp_unit', 'C')
        def _to_c(v): return (v - 32) * 5 / 9 if temp_unit == 'F' else v
        def _to_display(c): return round(c * 9 / 5 + 32, 1) if temp_unit == 'F' else round(c, 1)

        target_temp     = _to_c(float(request.form.get('target_dough_temp', 25)))
        ambient_temp    = _to_c(float(request.form.get('ambient_temp', 20)))
        flour_temp      = _to_c(float(request.form.get('flour_temp', 20)))
        levain_temp     = _to_c(float(request.form.get('levain_temp', 20)))
        friction_factor = float(request.form.get('friction_factor', 0))

        result_c = _EMPTY_DOUGH.calculate_water_temperature(
            target_temp=target_temp,
            flour_temp=flour_temp,
            levain_temp=levain_temp,
            ambient_temp=ambient_temp,
            friction_factor=friction_factor,
        )
        result = {
            'water_temp':   _to_display(result_c['water_temp']),
            'water_temp_c': result_c['water_temp'],
            'unit':         '°F' if temp_unit == 'F' else '°C',
        }
        return render_template('_water_temp_result.html', result=result, error=None,
                               temp_unit=temp_unit)
    except (ValueError, TypeError) as e:
        return render_template('_water_temp_result.html', result=None, error=str(e),
                               temp_unit='C')


@app.route('/calculate/fermentation', methods=['POST'])
def calculate_fermentation():
    """Adjust bulk fermentation time for room temperature. Returns inline result partial."""
    try:
        temp_unit = request.form.get('temp_unit', 'C')
        def _to_c(v): return (v - 32) * 5 / 9 if temp_unit == 'F' else v

        base_hours     = float(request.form.get('base_fermentation', 5))
        reference_temp = _to_c(float(request.form.get('reference_temp', 21)))
        ambient_temp   = _to_c(float(request.form.get('ambient_temp', 20)))

        result = _EMPTY_DOUGH.calculate_fermentation_time(
            base_hours=base_hours,
            reference_temp=reference_temp,
            ambient_temp=ambient_temp,
        )
        result['base_hours'] = base_hours
        return render_template('_fermentation_result.html', result=result, error=None)
    except (ValueError, TypeError) as e:
        return render_template('_fermentation_result.html', result=None, error=str(e))


@app.route('/calculate/starter', methods=['POST'])
def calculate_starter():
    """Calculate starter feeding amounts. Returns inline result partial."""
    try:
        target_amount  = float(request.form.get('target_amount', 110))
        ratio_flour    = float(request.form.get('ratio_flour', 5))
        ratio_water    = float(request.form.get('ratio_water', 5))
        ratio_starter  = float(request.form.get('ratio_starter', 1))

        levain = Levain("starter", (ratio_flour, ratio_water, ratio_starter))
        result = levain.calculate_feeding(target_amount)
        return render_template('_starter_result.html', result=result, error=None)
    except (ValueError, TypeError) as e:
        return render_template('_starter_result.html', result=None, error=str(e))


@app.route('/calculate/timeline', methods=['POST'])
def calculate_timeline():
    """Generate full bake timeline. Returns timeline partial.
    Reads bread_type and starter_pct from form (included via hx-include).
    """
    bread_type = 'freestanding'
    try:
        target_date      = request.form.get('target_date', '')
        target_time      = request.form.get('target_time', '08:00')
        room_temp        = float(request.form.get('room_temp', 20))
        proofing_method  = request.form.get('proofing_method', 'cold')
        autolyse_mins    = int(request.form.get('autolyse_mins', 30))
        include_autolyse = request.form.get('include_autolyse') == 'on'
        bread_type       = request.form.get('bread_type', 'freestanding')
        starter_pct      = float(request.form.get('starter_pct', 10)) / 100

        if not target_date:
            return render_template('_bake_timeline.html', steps=None,
                                   error="Please select the date you want your bread ready.",
                                   now=datetime.now(), bread_type=bread_type)

        target_dt = datetime.strptime(f"{target_date} {target_time}", "%Y-%m-%d %H:%M")

        steps = BakeTimeline.generate(
            target_datetime=target_dt,
            room_temp=room_temp,
            starter_pct=starter_pct,
            proofing_method=proofing_method,
            autolyse_mins=autolyse_mins if include_autolyse else 0,
            bread_type=bread_type,
        )

        return render_template('_bake_timeline.html', steps=steps, error=None,
                               now=datetime.now(), bread_type=bread_type)
    except (ValueError, TypeError) as e:
        return render_template('_bake_timeline.html', steps=None, error=str(e),
                               now=datetime.now(), bread_type=bread_type)


# ── Static pages ───────────────────────────────────────────────────────────────

@app.route('/science')
def science():
    return render_template('science.html', hide_sidebar=True)


@app.route('/troubleshoot')
def troubleshoot():
    return render_template('troubleshoot.html', hide_sidebar=True)


@app.route('/bakes')
def bakes():
    return render_template('bakes.html', hide_sidebar=True)


if __name__ == '__main__':
    # use_reloader=False prevents semaphore leaks on Python 3.14 / macOS
    app.run(debug=True, use_reloader=False)
