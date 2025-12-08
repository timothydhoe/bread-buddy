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
    def __init__(self, name: str = "My Recipe"):
        self._name = name
        self.ingredients = []  # List of ingredient objects .. OR DICT???


    @property
    def name(self):
        return self._name

    @name.setter(self):
        pass

    def __str__(self):
        return f"Recipe: {self.name}/n  {self.ingredients}"

    def __repr__(self):
        return f"Recipe: name={self.name}, ingredients={self.ingredients}"

    add_ingredient(self, ingredient: Ingredient):
        """ Add an ingredient to the recipe."""
        pass

    remove_ingredient(self, ingredient: Ingredient):
        """ Remove an ingredient from the recipe."""
        pass

    @property
    total_flour_weight(self):
        """ Sum of all flours."""
        pass

    @property
    total_liquid_weight(self):
        """ Sum of all liquids."""
        pass

    @property
    total_weight(self):
        """ Sum of all liquids."""
        pass

    @property
    hydration_percentage(self):
        """ Calculate the hydration of the dough. """
        pass

    def validate(self):
        """ Check dough viability.

        At least one flour. All ingredients have weights. warning if hydration is too low. Suggest if ingredient forgotten. eg. yeast
        """
        pass

    def scale(self, factor: float):
        """ Return a new recipe with all ingredients scaled."""
        pass

    def to_dict(self):
        """ For saving purposes. """
        pass

    def from_dict(data: dict):
        """ For loading purposes."""
        pass



recipe_test = Recipe("My First Bread")
print(recipe_test)
