"""Bread Buddy - Baker's calculation assistant.

This module provides an interactive command-line interface for amateur and expert bakers to calculate ingredient ratios, hydration levels, fermentation times, and other essential baking metrics.

The program guides users through various calculations including baker's percentages, recipe scaling, water temperature, and sourdough starter feeding.
"""
import bakers_calculators as bc
import utils



def main():
    """Runs the main program loop for Bread Buddy.
    
    Prompts the user for flour weight and uses that as the base for various
    baking calculations. Sets up default formula with water, salt, and levain
    percentages based on baker's percentage conventions.
    
    The function handles user input validation and guides the user through
    the calculation workflow.
    
    Returns:
        None
    """
    flour_weight = 0
    scale = .5
    # TODO: make interactive/dynamic in GUI
    formula = {"water_weight": 0.691, "salt_weight": .018, "levain_weight": .220}
   

    # User input Control Flow.
    while True:
        try:
            flour_weight = utils.user_input()
            break
        except (TypeError, ValueError) as e:
            print(f"Error: {e}")

    formula["flour_weight"] = 1
    print()
  

    """
    🧪 Everything below is for testing purposes only.
    """

    # Calling and printing bakers percentage.
    print("Ingredients, weight and ratio")
    print("-----------------------------")
    try:
        recipe = bc.bakers_percentage(flour_weight, formula)
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
    # ratio = recipe["ingredients"]
    # total = recipe["total_weight"]
    else:
        for ingredient, weight in recipe.items():
            if ingredient != "total_weight":
                print(f"Ingredient: {ingredient} -- {weight} -- {round(formula[ingredient]*100)}%")
        print(f"Total dough weight: {recipe["total_weight"]} grams\n")
        print("---\n")


    # Calling and printing Hydration function.
    print("Hydration level")
    print("---------------")
    try:
        hydration_result = bc.calculate_hydration(flour_weight, recipe["water_weight"])
    except ValueError as e:
        print(f"Error: {e}")
    else:
        print(f"Hydration: {hydration_result["hydration"]} - {hydration_result["description"]}\n")
        print("---\n")


    # Calling and printing Scaling function.
    print("Scaling function")
    print("----------------")
    try:
        scaled_recipe = bc.recipe_scaler(scale, recipe)
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
    else:
        for ingredient, value in scaled_recipe.items():
            print(f"{ingredient}: {value}")
        print("---\n")


    # Calling and printing desired_dough_weight()
    print("Desired Dough Weight")
    print("--------------------")
    dough_weight = 1_900
    try:
        target_recipe = bc.desired_dough_weight(dough_weight, formula)
    except ValueError as e:
        print(f"Error: {e}")
    else:
        print(f"\nDesidered Total Dough Weight: {dough_weight}")
        for ingredient, value in target_recipe.items():
            print(f"• {ingredient}: {value} grams")
        print("---\n")


    # Calling and printing mixing_water_temperature()
    print("Mixing Water Temperature")
    print("------------------------")
    try:
        water_result = bc.mixing_water_temperature()
    except ValueError as e:
        print(f"Error: {e}")
    else:
        print(f"Water temp: {water_result["water_temp"]}{water_result["unit"]}\n")

    try:
        water_result = bc.mixing_water_temperature(celsius=False)
    except ValueError as e:
        print(f"Error: {e}")
    else:
        print(f"Water temp: {water_result["water_temp"]}{water_result["unit"]}")
        print("---\n")

    # Calling and printing autolyse_timer()
    print("Autolyse timer")
    print("--------------")
    autolyse_schedule = bc.autolyse_schedule()
    for key, value in autolyse_schedule.items():
        if key == 'duration':
            print(f"{key}: {value}'")
        else:
            print(f"{key}: {value}")
    print("---\n")


    # Calling and printing bulk_fermentation_adjuster()
    print("Bulk Fermentation Calculator")
    print("----------------------------")
    try:
        fermentation_schedule = bc.bulk_fermentation_adjuster(base_time_hours=4)
    except ValueError as e:
        print(f"Error: {e}")
    else:
        for value, key in fermentation_schedule.items():
            print(f"{value}: {key}")
        print("---\n")


    # Calling and printing feeding_calculator()
    print("Feeding Calculator")
    print("------------------")
    try:
        starter_feed = bc.feeding_calculator()
    except ValueError as e:
        print(f"Error: {e}")
    else:
        for ingredient, weight in starter_feed.items():
            print(f"{ingredient}: {weight}")
        print("---\n")


# Run the programme.
if __name__ == "__main__":
    main()





# class Recipe:
#     # Store ingredients, scale up/down

# class BakersPercentage:
#     # Convert between weights and percentages

# class DoughCalculator:
#     # Hydration, water temp, ...
