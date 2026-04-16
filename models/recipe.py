"""
filename: recipe.py
-------------------

This file contains the Recipe class for bread recipes.
A Recipe is a container Class for Ingredients.

"""

from .ingredient import Ingredient

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
    def name(self, value):
        if value and isinstance(value, str):
            self._name = value

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
        """ Sum of all water and the water in starters"""
        liquid = 0
        
        for ingredient in self.ingredients:
            if ingredient.category == 'water':
                liquid += ingredient.weight
            elif ingredient.category == 'starter':
                # formula: starter_weight * (hydration/ (100+hydration))
                hydration = ingredient.starter_hydration / 100
                liquid_part = ingredient.weight * (hydration / (1 + hydration))
                liquid += liquid_part
                
        return liquid

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
        from .ingredient import Ingredient
        recipe = cls(data["name"])
        recipe.ingredients = [Ingredient.from_dict(ingredient) for ingredient in data["ingredients"]]
        return recipe

    @property
    def chart_data(self) -> list:
        """Return ingredient data list for donut chart rendering."""
        return [ing.to_chart_dict() for ing in self.ingredients]

    def hints(self, bread_type: str = 'freestanding') -> list:
        """Return a list of smart hint dicts for the current recipe.

        Each dict has keys: 'level' ('warn' or 'info'), 'text' (str).
        """
        result = []
        flour = self.total_flour_weight
        if flour == 0:
            return result

        hyd = self.hydration_percentage
        starter_w = sum(i.weight for i in self.ingredients if i.category == 'starter')
        salt_w    = sum(i.weight for i in self.ingredients if i.category == 'salt')
        starter_pct = (starter_w / flour) * 100 if flour else 0
        salt_pct    = (salt_w    / flour) * 100 if flour else 0

        flour_ings = [i for i in self.ingredients if i.category == 'flour']
        rye_w = sum(i.weight for i in flour_ings if 'rye' in i.name.lower())
        rye_pct = (rye_w / flour) * 100 if flour else 0

        if hyd >= 90:
            result.append({
                'level': 'warn',
                'text': f"Put your wetsuit on. At {hyd:.0f}% this is not a dough, it is a very committed puddle. You will need the strongest high-protein flour you can find, a bench scraper for every single move, and absolutely no shame about relying on a well-oiled banneton liner. Achievable, but do not say you were not warned.",
            })
        elif hyd > 78 and bread_type == 'freestanding':
            result.append({
                'level': 'warn',
                'text': f'At {hyd}%, this is a wet dough for a free-form loaf. Shaping will require confident hands and a well-floured bench. 70-76% is more forgiving if you are still building technique.',
            })
        if salt_pct < 1.5 and salt_w > 0:
            result.append({
                'level': 'warn',
                'text': f'Salt is low at {salt_pct:.1f}%. It does considerably more than season: it tightens gluten, slows fermentation, and suppresses unwanted bacteria. Aim for 1.8-2.2%.',
            })
        if salt_pct > 2.8:
            result.append({
                'level': 'info',
                'text': f'Salt is at {salt_pct:.1f}%, which is on the assertive side. Most recipes sit comfortably at 2-2.2%. Perfectly fine if you like your bread well-seasoned, but fermentation may drag slightly.',
            })
        if starter_pct > 20:
            result.append({
                'level': 'info',
                'text': f'You are using a generous {starter_pct:.0f}% starter. Expect a fast rise and a mild, approachable flavour. Drop to 8-12% and give it more time if you want more sour character.',
            })
        if starter_pct < 5 and starter_w > 0:
            result.append({
                'level': 'info',
                'text': f'At only {starter_pct:.1f}% starter, fermentation will be slow and deliberate. Budget 12-18 hours for bulk at room temperature. The trade-off is a more complex, tangy flavour.',
            })
        if rye_pct > 50:
            result.append({
                'level': 'info',
                'text': 'More than half rye: expect a denser, moister crumb and noticeably faster fermentation. Rye enzymes are extremely active. Watch your bulk carefully.',
            })

        # Whole wheat / wholemeal
        ww_w = sum(i.weight for i in flour_ings
                   if any(w in i.name.lower() for w in ('whole wheat', 'wholemeal', 'whole grain')))
        ww_pct = (ww_w / flour) * 100 if flour else 0
        if ww_pct > 0:
            result.append({
                'level': 'info',
                'text': f'Whole wheat at {ww_pct:.0f}%: it absorbs considerably more water than white flour, so your dough may feel stiffer than you expect. Add a small splash more water if needed. Expect a nuttier depth of flavour and slightly faster fermentation.',
            })

        # Spelt
        spelt_w = sum(i.weight for i in flour_ings if 'spelt' in i.name.lower())
        spelt_pct = (spelt_w / flour) * 100 if flour else 0
        if spelt_pct > 20:
            result.append({
                'level': 'warn',
                'text': f'Spelt at {spelt_pct:.0f}%: wonderful flavour, genuinely fragile gluten. Keep your autolyse short, handle it gently during shaping, and resist any urge to overwork it. You will not enjoy the consequences if you do.',
            })

        # Einkorn
        einkorn_w = sum(i.weight for i in flour_ings if 'einkorn' in i.name.lower())
        einkorn_pct = (einkorn_w / flour) * 100 if flour else 0
        if einkorn_pct > 0:
            result.append({
                'level': 'info',
                'text': f'Einkorn at {einkorn_pct:.0f}%: an ancient grain with very weak gluten by modern standards. Expect a denser crumb, faster fermentation, and a distinctly nutty, almost sweet flavour. Worth every bit of the extra care it demands.',
            })

        return result

