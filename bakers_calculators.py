"""
filename: bakers_calculator.py
-------------------------------

This file contains all basic calculations for the "Bread Buddy" programme.

"""

from datetime import datetime, timedelta
import utils


def bakers_percentage(flour_weight, formula):
    """Calculates ingredient weights from baker's percentages.
    
    Args:
        flour_weight: Flour weight in grams.
        formula: Dict of ingredients and their ratios as decimals, 
                 e.g. {"water_weight": 0.70, "salt_weight": 0.02}.
    
    Returns:
        dict: All ingredient weights plus total_weight.
    """
    recipe = {"flour_weight": flour_weight}
    total_weight = flour_weight

    for ingredient, ratio in formula.items():
        recipe[ingredient] = round(flour_weight * ratio, 1)
        total_weight += recipe[ingredient]
        
    recipe["total_weight"] = total_weight

    return recipe


def calculate_hydration(flour_weight, water_weight):
    """Calculates dough hydration and consistency level.
    
    Args:
        flour_weight: Flour weight in grams.
        water_weight: Water weight in grams.
    
    Returns:
        dict: Hydration percentage and dough description.
    """
    hydration_percentage = round((water_weight / flour_weight) * 100, 1)

    if hydration_percentage < 60:
        description = "stiff dough. Good for bagels and pretzels. Or beginner bakers."
    elif hydration_percentage < 70:
        description = "standard hydration dough."
    elif hydration_percentage < 80:
        description = "high hydration dough. Good for Focaccia."
    else:
        description = "Very wet... consider getting your swimwear and diving right in."

    return {
        "hydration": hydration_percentage,
        "description": description
    }


def recipe_scaler(scale_factor, recipe):
    """Scales a recipe up or down.
    
    Args:
        scale_factor: Multiplier (2 = double, 0.5 = half).
        recipe: Dict of ingredients and weights in grams.
    
    Returns:
        dict: Scaled recipe.
    """
    scaled_recipe = {}
    for ingredient, weight in recipe.items():
        scaled_recipe[ingredient] = round(weight * scale_factor, 1)
    return scaled_recipe


def desired_dough_weight(desired_weight, formula):
    """Calculates ingredient weights from target dough weight.
    
    Args:
        target_weight: Desired total dough weight in grams.
        formula: Dict of ingredients and their ratios as decimals.
    
    Returns:
        dict: All ingredient weights in grams.
    """
    total_ratio = sum(ratio for ingredient, ratio in formula.items() if ingredient != "flour_weight")

    flour_weight = round(desired_weight / (1 + total_ratio), 1)

    recipe = {"flour_weight": flour_weight}
    for ingredient, ratio in formula.items():
        recipe[ingredient] = round(flour_weight * ratio, 1)

    return recipe
    

def mixing_water_temperature(ddt=25, flour_temp=22, levain_temp=25, ambient_temp=22, friction_fact=0, celsius=True):
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

    water_temp = round((ddt * 4) - (flour_temp + levain_temp + ambient_temp + friction_fact), 1)

    return {
        "water_temp": water_temp,
        "unit": "°F" if not celsius else "°C"
    }


def autolyse_schedule(duration_minutes=30):
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


def bulk_fermentation_adjuster(base_time_hours, reference_temp=21, ambient_temp=22):
    """Adjusts fermentation time based on room temperature.
    
    Args:
        base_time_hours: Fermentation time at reference temp, in hours.
        reference_temp: Recipe's designed temperature in Celsius. Default 21°C.
        ambient_temp: Actual room temperature in Celsius. Default 22°C.
    
    Returns:
        dict: Original and adjusted times, temperatures.
    """
    temp_difference = reference_temp - ambient_temp
    # For every 1°C change, fermentation time changes by ~10-15%
    adjustment_factor = 1.12 ** temp_difference     # ~12% per °C
    # TODO: adjustment_factor for °F.
    adjusted_time_hours = base_time_hours * adjustment_factor

    return {
        "base_time": utils.decimal_hours_to_time(base_time_hours),
        "adjusted_time": utils.decimal_hours_to_time(adjusted_time_hours),
        "reference_temp": reference_temp,
        "ambient_temp": ambient_temp
    }

def feeding_calculator (target_amount=220, feeding_ratio=(1,1,.2)):
    """Calculates sourdough starter feeding amounts.
    
    Args:
        target_amount: Desired total weight of fed starter in grams. Default 220.
        feeding_ratio: Ratio of (flour, water, starter). Default (1, 1, 0.2).
    
    Returns:
        dict: Flour, water, and starter weights in grams.
    """
    if target_amount <= 0:
        return {
            "error": "You'll need more than that!"
        }

    flour_ratio, water_ratio, starter_ratio = feeding_ratio
    
    total_ratio = sum(feeding_ratio)
    part_weight = target_amount / total_ratio

    return {
        "flour_weight": round(flour_ratio * part_weight, 1),
        "water_weight": round(water_ratio * part_weight, 1),
        "starter-weight": round(starter_ratio * part_weight, 1)
    }

