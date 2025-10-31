"""
filename: bakers_calculator.py
-------------------------------

This file contains all basic calculations for the "Bread Buddy" programme.

"""

from datetime import datetime, timedelta
import utils

# Calculation constants
FERMENTATION_ADJUSTMENT_FACTOR = 1.12   # ~12% change per °C
WATER_TEMP_MULTIPLIER = 4

# Hydration thresholds (in %)
HYDRATION_LOW = 60
HYDRATION_MEDIUM = 70
HYDRATION_HIGH = 80

# Temperature constants
DEFAULT_DDT = 25
DEFAULT_FLOUR_TEMP = 22
DEFAULT_LEVAIN_TEMP = 22
DEFAULT_AMBIENT_TEMP = 22
DEFAULT_REFERENCE_TEMP = 21



def bakers_percentage(flour_weight: float, formula: dict) -> dict:
    """Calculates ingredient weights from baker's percentages.
    
    Args:
        flour_weight: Flour weight in grams.
        formula: Dict of ingredients and their ratios as decimals, 
                 e.g. {"water_weight": 0.70, "salt_weight": 0.02}.
    
    Returns:
        dict: All ingredient weights plus total_weight.
    """
    if not isinstance(flour_weight, (int, float)):
        raise TypeError("Flour must be a number. Surely, you know that.\n")
    if flour_weight <= 0:
        raise ValueError("Flour weight can't be negative unless you're baking in a parallel universe!\n")
    if not isinstance(formula, dict):
        raise TypeError("Empty recipe? Even a minimalist needs flour!\n")

    recipe = {"flour_weight": flour_weight}
    total_weight = flour_weight

    for ingredient, ratio in formula.items():
        recipe[ingredient] = round(flour_weight * ratio, 1)
        total_weight += recipe[ingredient]
        
    recipe["total_weight"] = round(total_weight, 1)

    return recipe


def calculate_hydration(flour_weight: float, water_weight: float) -> dict:
    """Calculates dough hydration and consistency level.
    
    Args:
        flour_weight: Flour weight in grams.
        water_weight: Water weight in grams.
    
    Returns:
        dict: Hydration percentage and dough description.
    """
    if flour_weight <= 0:
        raise ValueError("Can't calculate hydration without flour. That's just... water!\n")
    if water_weight <= 0:
        raise ValueError("Zero water? That's not dough, that's flour dust!\n")

    hydration_percentage = round((water_weight / flour_weight) * 100, 1)

    if hydration_percentage < HYDRATION_LOW:
        description = "stiff dough. Good for bagels and pretzels. Or beginner bakers."
    elif hydration_percentage < HYDRATION_MEDIUM:
        description = "standard hydration dough."
    elif hydration_percentage < HYDRATION_HIGH:
        description = "high hydration dough. Good for Focaccia."
    else:
        description = "Very wet... consider getting your swimwear and diving right in."

    return {
        "hydration": hydration_percentage,
        "description": description
    }


def recipe_scaler(scale_factor: float, recipe: dict) -> dict:
    """Scales a recipe up or down.
    
    Args:
        scale_factor: Multiplier (2 = double, 0.5 = half).
        recipe: Dict of ingredients and weights in grams.
    
    Returns:
        dict: Scaled recipe.
    """
    if scale_factor < 0:
        raise ValueError("Negative scaling? Are we un-baking the bread?\n")
    if scale_factor == 0:
        raise ValueError("Scale factor of 0? That's not scaling, that's disappearing!\n")
    if not isinstance(recipe, dict):
        raise TypeError("Empty recipe? Even a minimalist needs flour!\n")

    scaled_recipe = {}
    for ingredient, weight in recipe.items():
        scaled_recipe[ingredient] = round(weight * scale_factor, 1)
    return scaled_recipe


def desired_dough_weight(desired_weight: float, formula: dict) -> dict:
    """Calculates ingredient weights from target dough weight.
    
    Args:
        target_weight: Desired total dough weight in grams.
        formula: Dict of ingredients and their ratios as decimals.
    
    Returns:
        dict: All ingredient weights in grams.
    """
    if desired_weight <= 0:
        raise ValueError(f"We all have desires. Why don't you tell me yours?\n")

    total_ratio = sum(ratio for ingredient, ratio in formula.items() if ingredient != "flour_weight")

    flour_weight = round(desired_weight / (1 + total_ratio), 1)

    recipe = {"flour_weight": flour_weight}
    for ingredient, ratio in formula.items():
        recipe[ingredient] = round(flour_weight * ratio, 1)

    return recipe
    

def mixing_water_temperature(
    ddt: float=DEFAULT_DDT,
    flour_temp: float=DEFAULT_FLOUR_TEMP,
    levain_temp: float=DEFAULT_LEVAIN_TEMP,
    ambient_temp: float=DEFAULT_AMBIENT_TEMP,
    friction_fact: float=0,
    celsius: bool=True
) -> dict:
    """Calculates water temperature for target dough temperature.
    
    Args:
        ddt: Desired dough temperature. Default 25°C.
        flour_temp: Flour temperature. Default 22°C.
        levain_temp: Levain/starter temperature. Default 25°C.
        ambient_temp: Room temperature. Default 22°C.
        friction_factor: Heat from mixing (0 for hand, 10-30°F for machine). Default 0.
        celsius: Use Celsius if True, Fahrenheit if False. Default True.
    
    Returns:
        dict: Water temperature and unit.
    """
    if not celsius:
        ddt = utils.celsius_to_fahrenheit(ddt)
        flour_temp = utils.celsius_to_fahrenheit(flour_temp)
        levain_temp = utils.celsius_to_fahrenheit(levain_temp)
        ambient_temp = utils.celsius_to_fahrenheit(ambient_temp)
        # friction_fact = utils.celsius_to_fahrenheit(friction_fact) -- has to stay 0 when no friction is applied.

    water_temp = round((ddt * WATER_TEMP_MULTIPLIER) - (flour_temp + levain_temp + ambient_temp + friction_fact), 1)

    if 15 < water_temp > 48:
        raise ValueError("That temperature would either freeze or boil your dough. Let's keep it real!\n")

    return {
        "water_temp": water_temp,
        "unit": "°F" if not celsius else "°C"
    }


def autolyse_schedule(duration_minutes: int=30) -> dict:
    """Calculates autolyse rest period start and end times.
    
    Args:
        duration_minutes: Rest duration in minutes. Default 30.
    
    Returns:
        dict: Start time, end time, and duration.
    """
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration_minutes)

    return {
        "start": start_time.strftime("%H:%M"),
        "end": end_time.strftime("%H:%M"),
        "duration": duration_minutes
    }


def bulk_fermentation_adjuster(
    base_time_hours: int,
    reference_temp: float=DEFAULT_REFERENCE_TEMP,
    ambient_temp: float=DEFAULT_AMBIENT_TEMP
) -> dict:
    """Adjusts fermentation time based on room temperature.
    
    Args:
        base_time_hours: Fermentation time at reference temp, in hours.
        reference_temp: Recipe's designed temperature in Celsius. Default 21°C.
        ambient_temp: Actual room temperature in Celsius. Default 22°C.
    
    Returns:
        dict: Original and adjusted times, temperatures.
    """
    if base_time_hours <= 0:
        raise ValueError("Negative fermentation time? We can't go back in time... yet!\n")

    temp_difference = reference_temp - ambient_temp
    # For every 1°C change, fermentation time changes by ~10-15%
    adjustment_factor = FERMENTATION_ADJUSTMENT_FACTOR ** temp_difference
    # TODO: adjustment_factor for °F.
    adjusted_time_hours = base_time_hours * adjustment_factor

    return {
        "base_time": utils.decimal_hours_to_time(base_time_hours),
        "adjusted_time": utils.decimal_hours_to_time(adjusted_time_hours),
        "reference_temp": reference_temp,
        "ambient_temp": ambient_temp
    }

def feeding_calculator (
    target_amount: int=220,
    feeding_ratio: tuple=(1,1,0.2)
) -> dict:
    """Calculates sourdough starter feeding amounts.
    
    Args:
        target_amount: Desired total weight of fed starter in grams. Default 220.
        feeding_ratio: Ratio of (flour, water, starter). Default (1, 1, 0.2).
    
    Returns:
        dict: Flour, water, and starter weights in grams.
    """
    flour_ratio, water_ratio, starter_ratio = feeding_ratio

    if flour_ratio <= 0 or water_ratio <= 0:
        raise ValueError("Can't feed nothing! Even starters need to eat!")
    if starter_ratio <= 0:
        raise ValueError("You'll need some starter. I hope you didn't discard it...")
    
    total_ratio = sum(feeding_ratio)
    part_weight = target_amount / total_ratio

    return {
        "flour_weight": round(flour_ratio * part_weight, 1),
        "water_weight": round(water_ratio * part_weight, 1),
        "starter-weight": round(starter_ratio * part_weight, 1)
    }

