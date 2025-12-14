"""
filename: recipe.py
-------------------------------

This file contains the Recipe class for bread recipes.
A Recipe is a container Class for Ingredients.

"""

from ingredient import Ingredient

class Recipe:
    """ An Ingredient in a bread recipe.

    Represents a single ingredient with its weight and optional baker's
    percentage ratio. Supports scaling and validation.

    Params:
        name: str   -- default="My Recipe"
        ingredients: list[Ingredient]


    """
    def __init__(self, name: str="My Recipe"):
        self._name = name
        self.ingredients = []  # List of ingredient objects .. OR DICT???


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self):
        pass

    def __str__(self):
        return f"Recipe: {self.name}\n  {self.ingredients}"

    def __repr__(self):
        return f"Recipe: name={self.name}, ingredients={self.ingredients}"

    def add_ingredient(self, ingredient):
        """ Add an ingredient to the recipe."""
        if ingredient not in self.ingredients:
            self.ingredients.append(ingredient)

    def remove_ingredient(self, ingredient):
        """ Remove an ingredient from the recipe."""
        if ingredient in self.ingredients:
            self.ingredients.remove(ingredient)

    @property
    def total_flour_weight(self):
        """ Sum of all flours ingredients"""
        return sum(ingredient.weight for ingredient in self.ingredients if ingredient.category == 'flour')

    @property
    def total_liquid_weight(self):
        """ Sum of all water and starter ingredients"""
        return sum(ingredient.weight for ingredient in self.ingredients if ingredient.category in ('water', 'starter'))

    @property
    def total_weight(self):
        """ Sum of all ingredients."""
        return sum(ingredient.weight for ingredient in self.ingredients)

    @property
    def hydration_percentage(self):
        """ Calculate the hydration of the dough. 

            Formula: (liquids / flour) * 100
        """
        flour = self.total_flour_weight
        if flour == 0:
            return 0
        return round((self.total_liquid_weight / flour) * 100, 1)

    def divide_water():
        # Idea to divide water, never pour total water at once,
        # keep about 10% on the side to add after if needed.
        pass

    def validate(self):
        """ Check dough viability.

        At least one flour. All ingredients have weights. warning if hydration is too low. Suggest if ingredient forgotten. eg. yeast
        """
        pass

    def scale(self, factor: float):
        """ Return a new scaled recipe"""
        scaled = Recipe(f"{self.name} (scaled {factor}x)")
        scaled.ingredients = [ingredient.scale(factor) for ingredient in self.ingredients]
        return scaled

    @classmethod
    def from_bakers_percentage(cls, name, flour_weight, formula):
        """ Create Recipe from flour weight + ratios.
        Args:
            name: Recipe name
            flour_weight: Total flour weight in grams
            formula: Dict like {"water": 0.70, "salt": 0.02, "starter": 0.20}
        
        Returns:
            Recipe with ingredients created from ratios
        """

        recipe = cls(name)

        flour = Ingredient("flour", flour_weight, "flour", ratio=1.0)
        recipe.add_ingredient(flour)

        category_map = {
            "water": "water",
            "salt": "salt", 
            "starter": "starter",
            "levain": "starter"
        }

        for ingredient_name, ratio in formula.items():
            # Strip "_weight" suffix if present (for backward compatibility)
            clean_name = ingredient_name.replace("_weight", "")
            
            # Determine category
            category = category_map.get(clean_name, "other")
            
            # Create ingredient using from_ratio
            ing = Ingredient.from_ratio(
                name=clean_name,
                flour_weight=flour_weight,
                ratio=ratio,
                category=category
            )
            recipe.add_ingredient(ing)
        
        return recipe

    def to_dict(self):
        """ For saving purposes in JSON """
        return {
            "name": self.name,
            "ingredients": [ingredient.to_dict() for ingredient in self.ingredients]
        }

    @classmethod
    def from_dict(cls, data: dict):
        """ Reload from dict."""
        from ingredient import Ingredient
        recipe = cls(data["name"])
        recipe.ingredients = [Ingredient.from_dict(ingredient) for ingredient in data["ingredients"]]
        return recipe


# rye = Ingredient('rye', 500, 'flour')
# water = Ingredient('WAter', 300, 'water')
# salt = Ingredient('salt', 10, 'salt')
# # starter = Levain()

# the_one = Recipe("My First Loaf")
# print(the_one)

# the_one.add_ingredient(rye)
# the_one.add_ingredient(water)
# the_one.add_ingredient(salt)

# print(the_one)

recipe = Recipe.from_bakers_percentage(
    "My Sourdough",
    1000,
    {"water": 0.70, "salt": 0.02, "starter": 0.20}
)

print(recipe)
print(f"Total weight: {recipe.total_weight}g")
print(f"Hydration: {recipe.hydration_percentage}%")
"""

Should output:
```
Recipe: My Sourdough
  [flour, water, salt, starter ingredients]
Total weight: 1920.0g
Hydration: 90.0%
"""