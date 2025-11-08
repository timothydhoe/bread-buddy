"""
filename: recipes.py
--------------------

This file holds all classes to recipe tables.

In breadbaking, there are two main tables/charts to show both the essential features of the recipe; a table called Vitals, an a table called TotalFormula which shows the ingredients and their baker's percentages.

Within the recipe, smaller ingredient tables are presented: Levain and Dough. These tables show the ingredients that need to be added or combined at a specific step.

"""

import utils

class Vitals:
    """
    """
    def __init__(self, total_dough_weight, prefermented_flour,
                       levain, hydration, _yield):
        self.total_dough_weight = total_dough_weight
        self.prefermented_flour = prefermented_flour
        self.levain = levain
        self.hydration = hydration
        self._yield = _yield

    def hydration_percentage():
        pass


class TotalFormula:
    """
    """
    def __init__(self):
        self.flours = {}
        self.water = water
        self.ripe_starter = ripe_starter
        self.salt = salt
        self.ingredients = {}

        def add_flour(self, name, grams):
            """ Add a flour type and its weight."""
            self.flours[name] = grams

        def add_ingredient(self, name, grams):
            """ Add an ingredient and its weight."""
            self.ingredients[name] = grams

        def remove_ingredient(self, name):
            if name in flours:
                flours.pop(name)
            elif name in ingredients:
                ingredients.pop(name)

            return f"{name} removed."

        def divide_water():
            # Idea to divide water, never pour total water at once,
            # keep about 10% on the side to add after if needed.
            pass

        @property
        def flour_ratio(self):
            flours_ratio = {}
            """ Calculate ratio of all flours used"""
            whole = sum(flours.values()) # TODO: Return ratio of flours not sum.
            for flour in flours:
                flours_ratio[flour] = pct_ratio(flour, whole)

            return flours_ratio

class Levain:
    def __init__(self, flour_1, water, ripe_starter):
        self.flour_1 = flour_1
        self.water = water
        self.ripe_starter = ripe_starter


class Dough:
    def __init__(self, flour_1, water_1, salt, levain):
        self.flour_1 = flour_1
        self.water_1 = water_1
        self.salt = salt
        self.levain = levain
