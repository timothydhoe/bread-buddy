"""
filename: recipe.py
-------------------------------

This file contains the Recipe class for bread recipes.
A Recipe is a container Class for Ingredients.

"""

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
        return f"Recipe: {self.name}/n  {self.ingredients}"

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
        """ Sum of all flours."""
        pass

    @property
    def total_liquid_weight(self):
        """ Sum of all liquids."""
        pass

    @property
    def total_weight(self):
        """ Sum of all ingredients' weight."""
        pass

    @property
    def hydration_percentage(self):
        """ Calculate the hydration of the dough. """
        pass

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
