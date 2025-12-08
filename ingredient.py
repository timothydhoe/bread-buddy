"""
filename: ingredient.py
-------------------------------

This file contains the Ingredient class for bread recipes.

"""


class Ingredient:
    """ An Ingredient in a bread recipe.

    Represents a single ingredient with its weight and optional baker's
    percentage ratio. Supports scaling and validation.

    Params:
        name: str
        weight: float   -- default=1.0  (100%)
        category: str   -- default="other"
        ratio: float    -- default=None

    Raises:
        ValueError: if name is empty, weight is negative or ratio is invalid.

    Returns:
        Ingredient Object

    Examples:
        >>> flour = Ingredient("flour", 1000, 1.0)
        >>> water = Ingredient("water", 700, 0.70)
        >>> scaled = flour.scale(0.5)
        >>> print(scaled.weight)
        500.0
    """

    # TODO: extend when needed.
    CATEGORIES = {"flour", "water", "salt", "starter", "fat", "sweetener", "other"}

    def __init__(
        self,
        name: str,  # Name should be category when water?
        weight: float=1.0,
        category: str="other",
        ratio: float=None,
    ):
        # Validate ratio (if provided)
        if ratio is not None and (ratio < 0 or ratio > 2.0):
            raise ValueError(f"Ratio should be between 0 and 2.0. (got {ratio})")

        # TODO: Need to add a type name? eg. flour, ...   ?
        self.name = name
        self.category = category
        self._weight = None
        self.weight = weight
        self.ratio = ratio

    @property
    def name(self):
        """Get ingredient name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the name with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Ingredient name must be a non-empty string.")
        self._name = value

    @property
    def category(self):
        """Get ingredient category."""
        return self._category

    @category.setter
    def category(self, value):
        """Set a valid category."""
        if value not in self.CATEGORIES:
            raise ValueError(
                f"Category must be one of {self.CATEGORIES}. (Got {value})"
            )
        self._category = value

    @property
    def weight(self):
        """Get ingredient weight in grams."""
        return self._weight

    @weight.setter
    def weight(self, value):
        """Set weight with validation."""
        if value < 0:
            raise ValueError(f"Weight cannot be negative. (got {value})")
        self._weight = float(value)

    def __str__(self):
        ratio_str = f"{self.ratio:.2f} %" if self.ratio else "N/A"
        return f"{self.name}, {self.category}\n  weight: {self.weight} g\n  ratio: {ratio_str}"

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}=(name={self.name!r}, weight={self.weight!r}, cat={self.category!r}, ratio={self.ratio!r})"

    def __add__(self, other):
        """Combine two ingredients of the same type."""
        if self.name != other.name:
            raise ValueError(f"Cannot add {self.name} and {other.name}.")

        new_weight = self.weight + other.weight

        new_ratio = None
        if self.ratio is not None and other.ratio is not None:
            new_ratio = (self.ratio + other.ratio) / 2

        return Ingredient(self.name, new_weight, self.category, new_ratio)

    def __eq__(self, other):
        """Check equality based on name and category."""
        if not isinstance(other, Ingredient):
            return False
        return (
            self.name == other.name
            and abs(self.weight - other.weight) < 0.1
            and self.ratio == other.ratio
            and self.category == other.category
        )

    @classmethod
    def from_ratio(
        cls, name: str, flour_weight: float,
        ratio: float, category: str = "other"):
        """Create ingredient from baker's percentage.

        Usage:
            Creates Ingredient with weight=700g
            ingredient = Ingredient.from_ratio("water", flour_weight=1000, ratio=0.70)
        """
        weight = flour_weight * ratio
        return cls(name=name, weight=weight, category=category, ratio=ratio)

    def scale(self, factor: float):
        """Return a new ingredient scaled by the given factor."""
        if factor <= 0:
            raise ValueError(f"Scale factor must be positive. (got {factor})")

        return Ingredient(self.name, self.weight * factor, self.category, self.ratio)
        

    def to_dict(self) -> dict:
        """Convert to dictionary for saving purposes."""
        return {
            "name": self.name,
            "weight": self.weight,
            "category": self.category,
            "ratio": self.ratio,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create ingredient from dictionary"""
        return cls(
            data["name"],
            data.get("weight", 0),
            data.get("category", "other"),
            data.get("ratio"),
        )



## TEST ##
rye = Ingredient('rye', 500, "flour")
print(rye)
