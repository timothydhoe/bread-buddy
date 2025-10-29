"""
filename: main.py
-------------------------------

Programme "Bread Buddy" that helps bakers, from novices to experts, calcuate all their bready needs.

"""
import bakers_calculators as bc


def main():
    """s
    Setting up variables.
    """
    flour_weight = 0
    scale = .5
    formula = {"water_weight": .691, "salt_weight": .018, "levain_weight": .220}
   

    # User input Control Flow.
    while True:
        try:
            flour_weight = int(input("How much flour do you plan to use? "))
            if flour_weight <= 0:
                print("You will need more flour than that, mate...\n")
            else:
                formula["flour_weight"] = 1
                print()
                break
        except (ValueError, TypeError):
            print("Mate, you're baking bread... You'll need flour!\n")
    



    """
    🧪 Everything below is for testing purposes only.
    """

    # Calling and printing bakers percentage.
    ratio_results, total_weight = bc.bakers_percentage(flour_weight, formula)
    print("Ingredients, weight and ratio")
    print("-----------------------------")
    for ingredient, percentage in ratio_results.items():
        print(f"Ingredient: {ingredient} -- {percentage} -- {round(formula[ingredient]*100)}%")
    print(f"Total dough weight: {total_weight} grams\n")
    print("---\n")


    # Calling and printing Hydration function.
    print("Hydration level")
    print("---------------")
    hydration = bc.calculate_hydration(flour_weight, ratio_results["water_weight"])
    print(f"Hydration: {hydration}\n")
    print("---\n")


    # Calling and printing Scaling function.
    print("Scaling function")
    print("----------------")
    scaled_result = bc.recipe_scaler(scale, ratio_results)
    for ingredient, value in scaled_result.items():
        print(f"{ingredient}: {value}")
    print("---\n")


    # Calling and printing desired_dough_weight()
    print("Desired Dough Weight")
    print("--------------------")
    dough_weight = 1_900
    desired_weight = bc.desired_dough_weight(dough_weight, formula)
    print(f"\nDesidered Total Dough Weight: {dough_weight}")
    for ingredient, value in desired_weight.items():
        print(f"• {ingredient}: {value} grams")
    print("---\n")


    # Calling and printing mixing_water_temperature()
    print("Mixing Water Temperature")
    print("------------------------")
    my_water = bc.mixing_water_temperature()
    print(f"My water: {my_water} in Celsius")

    my_water = bc.mixing_water_temperature(celsius=False)
    print(f"My water: {my_water} in Fahrenheit\n")
    print("---\n")

    # Calling and printing autolyse_timer()
    print("Autolyse timer")
    print("--------------")
    timer = bc.autolyse_timer()
    for key, value in timer.items():
        if key == 'duration':
            print(f"{key}: {value}'")
        else:
            print(f"{key}: {value}")
    print("---\n")


    # Calling and printing bulk_fermentation_adjuster()
    print("Bulk Fermentation Calculator")
    print("----------------------------")
    bulk_time = bc.bulk_fermentation_adjuster(base_time_hours=4)
    for value, key in bulk_time.items():
        print(f"{value}: {key}")
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
