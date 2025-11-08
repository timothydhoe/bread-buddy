"""
filename: recipes.py
--------------------

This file holds all classes to recipe tables.

In breadbaking, there are two main tables/charts to show both the essential features of the recipe; a table called Vitals, an a table called TotalFormula which shows the ingredients and their baker's percentages.

Within the recipe, smaller ingredient tables are presented: Levain and Dough. These tables show the ingredients that need to be added or combined at a specific step.

"""

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
    def __init__(self, flour_1, water_1, water_2, salt, ripe_starter):
        self.flour_1 = flour_1
        self.water_1 = water_1
        self.water_2 = water_2
        self.salt = salt
        self.ripe_starter = ripe_starter


class Levain:
    def __init__(self, flour_1, water_1, ripe_starter):
        self.flour_1 = flour_1
        self.water_1 = water_1
        self.ripe_starter = ripe_starter


class Dough:
    def __init__(self, flour_1, water_1, water_2, salt, levain):
        self.flour_1 = flour_1
        self.water_1 = water_1
        self.water_2 = water_2
        self.salt = salt
        self.levain = levain
