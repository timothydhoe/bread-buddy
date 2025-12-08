"""
filename: levain.py
-------------------------------

This file contains the Levain class. This is basically a Recipe so the Levain Class is a Subclass from Recipe. 

params:
    ingredients: [Ingredient] -- default=None

"""

from recipe import Recipe

class Levain(Recipe):
    def __init__(self, name: str="Levy"):   # TODO: randomly generate names
        self.ingredients = []

    @classmethod
    def add_ingredient(self, ingredient):
        if ingredient not in self.ingredients:
            self.ingredients.append()
        