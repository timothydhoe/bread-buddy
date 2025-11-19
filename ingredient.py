"""
filename: ingredient.py
-------------------------------

This file contains the class Ingredient.

"""

class Ingredient():
    """ The Ingredient class summary line.

    The Ingredient class bigger summary here.

    Args:
        name : str
            Each ingredient has an obligatory name.
        weight : float
            The weight expressed in grams. default = 1
        ratio : float
            The ratio of the ingredient in the recipe. default = 0

    Attributes:


    Methods:


    Returns:
        Ingredient Object

    Raises:
        ValueError
    """

    def __init__(self, name: str, weight: float=1.0, ratio: float=None):
        # Validate name
        if not name or not isinstance(name, str):
            raise ValueError("Ingredient name must be a non-empty string.")

        # Validate weight
        if weight < 0 or not isinstance(weight, float):
            raise ValueError(f"Weight must be higher than zero. (got {weight})")

        # Validate ratio (if provided)
        if ratio is not None and (ratio < 0 or ratio > 2.0):
            raise ValueError(f"Ratio should be between 0 and 2.0. (got {ratio})")

        # TODO: Need to add a type name? eg. flour, ...   ?
        self.name = name
        self.weight = float(weight)
        self.ratio = ratio


    def __str__(self):
        return f"Ingredient: {self.name}\n\tweight:{self.weight}\n\tratio: {self.ratio}"

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}=(name={self.name!r}, weight={self.weight!r}, ratio={self.ratio!r})"

    # TODO: only with type name? eg. flour, ...   ?
    def __add__(self, other):
        """ Combine two ingredients of the same type
        
        Usage:
            flour1 = Ingredient("flour", 500, 1.0)
            flour2 = Ingredient("flour", 300, 1.0)
            total_flour = flour1 + flour2
        """
        if self.name != other.name:
            raise ValueError(f"Cannot add {self.name} and {other.name}.")

        new_weight = self.weight + other.weight
        
        new_ratio = None
        if self.ratio is not None and other.ratio is not None:
            new_ratio = (self.ratio + other.ratio) / 2

        return Ingredient(self.name. new_weight, new_ratio)

    @classmethod
    def from_ratio(cls, name: str, flour_weight: float, ratio: float):
        """ Create ingredient from baker's percentage.
        
        Usage:
            Creates water with weight=700g
            water = Ingredient.from_ratio("water", flour_weight=1000, ratio=0.70)
        """
        weight = flour_weight * ratio
        return cls(name, weight, ratio)


    @property
    def weight(self):
        """ Get ingredient weight"""
        return self.new_weight

    @weight.setter
    def weight(self.value):
        """Set weight with validation"""
        if value < 0:
            raise ValueError(f"Weight cannot be negative. (got {weight})")
        self._weight = float(value)

    def scale(self, factor: float):
        """ Scale ingredient by factor. """
        return Ingredient(
            self.name,
            self.weight * factor,
            self.ratio
        )


flour = Ingredient('water')
print(flour.__repr__)
print(flour.name)

# Print docstring
# print(Ingredient.__doc__)
# print(str.__doc__)
# print(dir(Ingredient))