"""
filename: dough.py
-------------------

This file contains the Dough class for bread recipes.
All temperature units are in Celsius. Use utils.celsius_to_fahrenheit() for display.
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


class Dough:
    def __init__(self, recipe):
        self.recipe = recipe

    def __str__(self):
        return f"Dough({self.recipe})"

    def __repr__(self):
        return f"Dough({self.recipe})"

    @property
    def hydration(self):
        """ Returns the hydration percentage of the recipe. """
        return self.recipe.hydration_percentage

    @property
    def hydration_description(self):
        """ Calculates hydration % and returns feedback """
        hydration = self.recipe.hydration_percentage
        if hydration <= HYDRATION_LOW:
            return f"{hydration} - Stiff dough. Good for [...]"
        elif hydration <= HYDRATION_MEDIUM:
            return f"{hydration} - Standard Hydration. Good for [...]"
        elif hydration <= HYDRATION_HIGH:
            return f"{hydration} - High Hydration. Good for [...]"
        else:
            return f"{hydration} - Very wet... Get a wetsuit on before tackling this dough."

    def calculate_water_temperature(self, target_temp=DEFAULT_DDT, flour_temp=DEFAULT_FLOUR_TEMP, levain_temp=DEFAULT_LEVAIN_TEMP, ambient_temp=DEFAULT_AMBIENT_TEMP, friction_factor=0, celsius=True):
        """ Calculate water temperature for target dough temp.

        Args:
            target_temp: Desired dough temperature in °C. Default 25.
            flour_temp: Flour temperature in °C. Default 22.
            levain_temp: Levain/starter temperature in °C. Default 22.
            ambient_temp: Room temperature in °C. Default 22.
            friction_factor: Heat from mixing (0 for hand, 10-30 for machine). Default 0.
            celsius: Return in Celsius if True, Fahrenheit if False. Default True.

        Returns:
            Dict {"water_temp": float, "unit": str}
        """
        if not celsius:
            target_temp = utils.celsius_to_fahrenheit(target_temp)
            flour_temp = utils.celsius_to_fahrenheit(flour_temp)
            levain_temp = utils.celsius_to_fahrenheit(levain_temp)
            ambient_temp = utils.celsius_to_fahrenheit(ambient_temp)

        water_temp = round((target_temp * WATER_TEMP_MULTIPLIER) - (flour_temp + levain_temp + ambient_temp + friction_factor), 1)

        if water_temp < 15 or water_temp > 48:
            raise ValueError("That temperature would either freeze or boil your dough. Let's keep it real!\n")

        return {
            "water_temp": water_temp,
            "unit": "°F" if not celsius else "°C"
        }

    def calculate_fermentation_time(self, base_hours=4,
        reference_temp: float=DEFAULT_REFERENCE_TEMP,
        ambient_temp: float=DEFAULT_AMBIENT_TEMP):
        """Adjusts fermentation time based on room temperature.

        Args:
            base_hours: Fermentation time at reference temp, in hours.
            reference_temp: Recipe's designed temperature in Celsius. Default 21°C.
            ambient_temp: Actual room temperature in Celsius. Default 22°C.

        Returns:
            dict: Original and adjusted times, temperatures.
        """
        if base_hours <= 0:
            raise ValueError("Negative fermentation time? We can't go back in time... yet!\n")

        temp_difference = reference_temp - ambient_temp
        # For every 1°C change, fermentation time changes by ~10-15%
        adjustment_factor = FERMENTATION_ADJUSTMENT_FACTOR ** temp_difference
        adjusted_time_hours = base_hours * adjustment_factor

        return {
            "base_time": utils.decimal_hours_to_time(base_hours),
            "adjusted_time": utils.decimal_hours_to_time(adjusted_time_hours),
            "reference_temp": reference_temp,
            "ambient_temp": ambient_temp
        }
