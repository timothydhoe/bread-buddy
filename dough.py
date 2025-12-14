"""
filename: dough.py
-------------------------------

This file contains the Dough class for bread recipes.

"""

import utils

FERMENTATION_ADJUSTMENT_FACTOR = 1.12
WATER_TEMP_MULTIPLIER = 4
HYDRATION_LOW = 60
HYDRATION_MEDIUM = 70
HYDRATION_HIGH = 80
DEFAULT_DDT = 25
DEFAULT_FLOUR_TEMP = 22
DEFAULT_LEVAIN_TEMP = 22
DEFAULT_AMBIENT_TEMP = 22
DEFAULT_REFERENCE_TEMP = 21

from recipe import Recipe

class Dough:
    def __init__(self, recipe):
        self.recipe = recipe

    def __str__(self):
        pass

    def __repr__(self):
        pass

    @property
    def hydration(self):
        """ Returns the hydration percentage of the recipe. """
        return self.recipe.hydration_percentage()

    @property
    def hydration_description(self):
        """ Calculates hydration % and returns feedback """
        pass

    def calculate_water_temperature(self):
        pass

    def calculate_fermentation_time(self):
        pass

    def schedule_autolyse(self):
        pass


