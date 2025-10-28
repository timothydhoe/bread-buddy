"""
filename: bakers_calculator.py
-------------------------------

This file contains all basic calculations for the "Bread Buddy" programme.

"""

def bakers_percentage(flour_weight, percentages):
    """
    flour: grams
    percentages: dict like {"water": .70, "salt": .02, "levain": .01}

    Output: ratio_results and total_weight.
    """
    ratio_results = {"flour_weight": flour_weight}
    ingredient_weight = {}
    total_weight = flour_weight

    for ingredient, percent in percentages.items():
        ratio_results[ingredient] = round(flour_weight * percent, 1)
        total_weight += ratio_results[ingredient]
        
    return ratio_results, total_weight

def calculate_hydration(flour_weight, water_weight):
    """
    Returns hydration percentage and dough consistency description
    """
    hydration = round((water_weight / flour_weight) * 100, 1)

    if hydration < 60:
        consistency = f"{hydration}: stiff dough. Good for bagels and pretzels. Or beginner bakers."
    elif hydration < 70:
        consistency = f"{hydration}: standard hydration dough."
    elif hydration < 80:
        consistency = f"{hydration}: high hydration dough. Good for Focaccia"
    else:
        consistency = f"{hydration}: Very wet... consider getting your swimwear and diving right in"

    return consistency

def recipe_scaler(multiplier, ingredients):
    for ingredient, value in ingredients.items():
        ingredients[ingredient] = value * multiplier
    return ingredients
    

# TODO: def desired_water_temperature()