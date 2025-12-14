"""
filename: levain.py
-------------------------------

This file contains the Levain class. This is basically a Recipe so the Levain Class is a Subclass from Recipe. 

params:
    ingredients: [Ingredient] -- default=None

"""

#TODO: method to add ingredients like sugar!!

from ingredient import Ingredient
from recipe import Recipe

class Levain(Recipe):
    """ A Levain/Starter class, based on the Recipe class.

    Levain is a recipe with special feeding calculations.
    
    Args:
        name: str
        feeding_ratio: Tuple (in order: flour, water, levain)

    """
    def __init__(self, name: str="Levy", feeding_ratio=(1,1,.2)):
        super().__init__(name)
        self.feeding_ratio = feeding_ratio
        # self.ingredients = []

    def __str__(self):
        f, w, s = self.feeding_ratio
        return f"Levain: {self.name} (ratio {f}:{w}:{s})"

    def __repr__(self):
        return f"Levain(name={self.name!r}, feeding_ratio={self.feeding_ratio})"

    
    def calculate_feeding(self, target_amount: int=220):
        """Calculates sourdough starter feeding amounts.
        
        Args:
            target_amount: Desired total weight of fed starter in grams. Default 220.
        
        Returns:
            dict: Flour, water, and starter weights in grams.
        """
        flour_ratio, water_ratio, starter_ratio = self.feeding_ratio

        if flour_ratio <= 0 or water_ratio <= 0:
            raise ValueError("Can't feed nothing! Even starters need to eat!")
        if starter_ratio <= 0:
            raise ValueError("You'll need some starter. I hope you didn't discard it...")
        
        total_ratio = sum(self.feeding_ratio)
        part_weight = target_amount / total_ratio

        return {
            "flour_weight": round(flour_ratio * part_weight, 1),
            "water_weight": round(water_ratio * part_weight, 1),
            "starter_weight": round(starter_ratio * part_weight, 1)
        }

    def set_feeding_ratio(self, flour, water, starter):
        """ Update feeding ratio """
        if flour <= 0 or water <= 0 or starter <= 0:
            raise ValueError("We need ingredients!")
        self.feeding_ratio = (flour, water, starter)
        return self

#TODO: method to add ingredients like sugar!!
    def create_feeding_recipe(self, target_amount=220):
        """ Create a feeding recipe """
        amount = self.calculate_feeding(target_amount)

        feeding_recipe = Recipe(f"{self.name} Feeding")
        feeding_recipe.add_ingredient(
            Ingredient("flour", amount["flour_weight"], "flour")
        )
        feeding_recipe.add_ingredient(
            Ingredient("water", amount["water_weight"], "water")
        )
        feeding_recipe.add_ingredient(
            Ingredient("starter", amount["starter_weight"], "starter")
        )
        
        return feeding_recipe
        

# starter = Levain("My Starter")
# print(starter.calculate_feeding(220))
# feeding_recipe = starter.create_feeding_recipe(220)
# print(feeding_recipe)