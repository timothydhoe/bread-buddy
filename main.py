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
    Everything below is for testing purposes.
    """

    # Calling and printing bakers percentage.
    ratio_results, total_weight = bc.bakers_percentage(flour_weight, formula)

    for ingredient, percentage in ratio_results.items():
        print(f"Ingredient: {ingredient} -- {percentage} -- {round(formula[ingredient]*100)}%")
    print(f"Total dough weight: {total_weight} grams\n")

    # Calling and printing Hydration function.
    hydration = bc.calculate_hydration(flour_weight, ratio_results["water_weight"])
    print(f"Hydration level: {hydration}\n")

    # Calling and printing Scaling function.
    scaled_result = bc.recipe_scaler(scale, ratio_results)
    for ingredient, value in scaled_result.items():
        print(f"{ingredient}: {value}")
    print()

    # Calling and printing desired_dough_weight()
    dough_weight = 1_900
    desired_weight = bc.desired_dough_weight(dough_weight, formula)
    print(f"\nDesidered Total Dough Weight: {dough_weight}")
    for ingredient, value in desired_weight.items():
        print(f"• {ingredient}: {value} grams")

    # Calling and printing desired_water_temperature()
    my_water = bc.mixing_water_temperature()
    print(f"My water: {my_water} in Celsius")

    my_water = bc.mixing_water_temperature(celsius=False)
    print(f"My water: {my_water} in Fahrenheit")

# Run the programme.
if __name__ == "__main__":
    main()



# class Recipe:
#     # Store ingredients, scale up/down

# class BakersPercentage:
#     # Convert between weights and percentages

# class DoughCalculator:
#     # Hydration, water temp, ...
