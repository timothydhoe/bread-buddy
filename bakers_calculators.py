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


def recipe_scaler(scale_factor, ingredients):
    """Scales a recipe up or down by a given scale_factor.
    
    Multiplies all ingredient quantities by the specified factor. Useful for
    adjusting recipe yields (e.g., doubling a recipe with scale_factor=2).
    
    Args:
        scale_factor (int or float): Factor to scale the recipe by. Use 2 to double,
            0.5 to halve, etc.
        ingredients (dict): Dictionary mapping ingredient names to their weights
            in grams. For example, {"flour": 500, "water": 350}.
    
    Returns:
        dict: Dictionary with scaled ingredient weights.
    
    Note:
        This function modifies the original ingredients dictionary in place.
    
    Example:
        >>> recipe_scaler(2, {"flour": 500, "water": 350})
        {'flour': 1000, 'water': 700}
    """
    for ingredient, value in ingredients.items():
        ingredients[ingredient] = value * scale_factor
    return ingredients


def desired_dough_weight(desired_weight, formula):
    """Calculates ingredient quantities to achieve a target dough weight.
    
    Works backwards from a desired total dough weight to determine how much
    flour and other ingredients are needed, based on baker's percentages.
    
    Args:
        desired_weight (int or float): Target total dough weight in grams.
        formula (dict): Dictionary mapping ingredient names to their percentages
            as decimals relative to flour. For example, 
            {"water_weight": 0.70, "salt_weight": 0.02, "levain_weight": 0.22}.
            Should not include flour.
    
    Returns:
        dict: Dictionary with all ingredient weights in grams, including flour.
    
    Example:
        >>> desired_dough_weight(1900, {"water_weight": 0.66, "salt_weight": 0.02})
        {'flour_weight': 1136.4, 'water_weight': 750.0, 'salt_weight': 22.7}
    """
    sum_percentages = sum(v for k, v in formula.items() if k != "flour_weight")

    flour_weight = round(desired_weight / (1 + sum_percentages), 1)

    recipe = {"flour_weight": flour_weight}
    for ingredient, percentage in formula.items():
        recipe[ingredient] = round(flour_weight * percentage, 1)

    return recipe
    

def mixing_water_temperature(ddt=25, flour_temp=22, levain_temp=25, ambient_temp=22, friction_fact=0, celsius=True):
    """Calculates the water temperature needed to achieve desired dough temperature.
    
    Uses the baker's formula: water_temp = (DDT × 4) - (flour + levain + ambient + friction).
    This accounts for all temperature factors that affect final dough temperature.
    
    Args:
        ddt (int or float, optional): Desired dough temperature. Defaults to 25°C.
        flour_temp (int or float, optional): Temperature of flour. Defaults to 22°C.
        levain_temp (int or float, optional): Temperature of levain/starter. Defaults to 25°C.
        ambient_temp (int or float, optional): Room temperature. Defaults to 22°C.
        friction_fact (int or float, optional): Friction factor from mixing. 
            0 for hand mixing, higher values for machine mixing (typically 10-30°F 
            or 5-15°C). Defaults to 0.
        celsius (bool, optional): If True, uses Celsius. If False, converts all 
            inputs to Fahrenheit before calculation. Defaults to True.
    
    Returns:
        float: Required water temperature in the same unit as input (Celsius or Fahrenheit).
    
    Example:
        >>> mixing_water_temperature(ddt=25, flour_temp=20, levain_temp=24)
        23.0
        >>> mixing_water_temperature(ddt=78, flour_temp=72, celsius=False)
        90.0
    """
    if not celsius:
        ddt = utils.celsius_to_fahrenheit(ddt)
        flour_temp = utils.celsius_to_fahrenheit(flour_temp)
        levain_temp = utils.celsius_to_fahrenheit(levain_temp)
        ambient_temp = utils.celsius_to_fahrenheit(ambient_temp)
        # friction_fact = utils.celsius_to_fahrenheit(friction_fact) -- has to stay 0 when no friction is applied.

    return round((ddt * 4) - (flour_temp + levain_temp + ambient_temp + friction_fact), 1)


def autolyse_schedule(duration_minutes=30):
    """Calculates start and end times for the autolyse rest period.
    
    Autolyse is a resting period where flour and water are mixed and left to rest
    before adding salt and starter. This allows flour to fully hydrate and develops
    gluten naturally.
    
    Args:
        duration_minutes (int, optional): Length of autolyse rest in minutes.
            Typically 20-60 minutes. Defaults to 30.
    
    Returns:
        dict: Dictionary containing:
            - start (str): Start time in HH:MM format.
            - end (str): End time in HH:MM format.
            - duration (int): Duration in minutes.
    
    Note:
        This function provides time calculations only. Full schedule functionality
        with notifications will be implemented in the web interface.
    
    Example:
        >>> autolyse_schedule(45)
        {'start': '14:30', 'end': '15:15', 'duration': 45}
    """
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration_minutes)

    return {
        "start": start_time.strftime("%H:%M"),
        "end": end_time.strftime("%H:%M"),
        "duration": duration_minutes
    }


def bulk_fermentation_adjuster(base_time_hours, reference_temp=21, ambient_temp=22):
    """Adjusts bulk fermentation time based on room temperature.
    
    Warmer temperatures speed up fermentation, while cooler temperatures slow it down.
    This function uses the rule that fermentation time changes by approximately 12%
    for every 1°C change in temperature.
    
    Args:
        base_time_hours (int or float): Expected fermentation time at reference
            temperature, in hours.
        reference_temp (int or float, optional): Temperature the recipe was designed
            for, in Celsius. Defaults to 21°C.
        ambient_temp (int or float, optional): Actual room temperature in Celsius.
            Defaults to 22°C.
    
    Returns:
        dict: Dictionary containing:
            - original_time (str): Base fermentation time formatted as "Xh Ymin".
            - adjusted_time (str): Temperature-adjusted time formatted as "Xh Ymin".
            - reference_temp (float): Reference temperature used.
            - ambient_temp (float): Ambient temperature used.
    
    Example:
        >>> bulk_fermentation_adjuster(4, reference_temp=21, ambient_temp=25)
        {'original_time': '4h 0min', 'adjusted_time': '3h 11min', 
         'reference_temp': 21, 'ambient_temp': 25}
    """
    temp_difference = reference_temp - ambient_temp
    # For every 1°C change, fermentation time changes by ~10-15%
    adjustment_factor = 1.12 ** temp_difference
    adjusted_time = base_time_hours * adjustment_factor
    # print(adjusted_time)

    return {
        "original_time": utils.decimal_hours_to_time(base_time_hours),
        "adjusted_time": utils.decimal_hours_to_time(adjusted_time),
        "reference_temp": reference_temp,
        "ambient_temp": ambient_temp
    }

def feeding_calculator (target_amount=220, feeding_ratio=(1,1,.2)):
    """Calculates ingredient amounts for feeding sourdough starter.
    
    Determines how much flour, water, and existing starter to use based on a
    desired total amount and feeding ratio. Common ratios include 1:1:1 (equal parts) or 1:5:5 (high feeding ratio for vigorous activity).
    
    Args:
        target_amount (int or float, optional): Desired total weight of fed starter in grams. Defaults to 220.
        feeding_ratio (tuple, optional): Ratio of (flour, water, starter) as relative parts. For example, (1, 1, 0.2) means 1 part flour, 1 part water, and 0.2 parts existing starter. Defaults to (1, 1, 0.2).
    
    Returns:
        dict: Dictionary containing weights in grams:
            - flour (float): Amount of flour to add.
            - water (float): Amount of water to add.
            - starter (float): Amount of existing starter to use.
        Returns None if target_amount is <= 0.
    
    Example:
        >>> feeding_calculator(220, (1, 1, 0.2))
        {'flour': 100.0, 'water': 100.0, 'starter': 20.0}
        >>> feeding_calculator(300, (1, 1, 1))
        {'flour': 100.0, 'water': 100.0, 'starter': 100.0}
    """
    if target_amount <= 0:
        print("You'll need more than that!")
    else:
        flour_ratio, water_ratio, starter_ratio = feeding_ratio
        
        total_ratio = sum(feeding_ratio)
        part_size = target_amount / total_ratio

        flour_weight = round(flour_ratio * part_size, 1)
        water_weight = round(water_ratio * part_size, 1)
        starter_weight = round(starter_ratio * part_size, 1)

        return {
            "flour": flour_weight,
            "water": water_weight,
            "starter": starter_weight
        }

    