"""
filename: utils.py
-------------------------------

This file contains all helper/auxiliary functions for the "Bread Buddy" programme.
"""

# Temperature conversion
FAHRENHEIT_MULTIPLIER = 1.8
FAHRENHEIT_OFFSET = 32

# Time conversion
MINUTES_PER_HOUR = 60

def user_input():
    """
    Takes user input and checks for valid integer or float.

    Returns int.
    """
    user_input = int((input("How many grams of flour do you plan to use? ")))

    if not isinstance(user_input, (int, float)):
        raise TypeError(f"'{user_input}' isn't a number, mate. We're baking, not doing poetry!\n")
    if user_input == 0:
        raise ValueError("Zero flour means zero bread. Let's be a bit more ambitious!\n")
    if user_input < 0:
        raise ValueError("Negative flour? That's some quantum baking you're attempting, mate!\n")

    return user_input

def celsius_to_fahrenheit(C):
    """Converts Celsius to Fahrenheit.

    Returns int"""
    return round((C * FAHRENHEIT_MULTIPLIER) + FAHRENHEIT_OFFSET, 1)

def fahrenheit_to_Celsius(F):
    """Converts Fahrenheit to Celsius.
    
    Returns int"""
    return round((F - FAHRENHEIT_OFFSET) * (5/9), 1)

def decimal_hours_to_time(hours):
    """Convert decimal 'time' to hours and minutes.

    Returns string.
    """
    h = int(hours)
    m = int((hours - h) * MINUTES_PER_HOUR)
    return f"{h}h {m}min"

""" QUICK CONVERSION TEST
print("Celsius to Fahrenheit")
print("---------------------")
print(f"flour:      {celsius_to_fahrenheit(22)}")
print(f"levain:     {celsius_to_fahrenheit(25)}")
print(f"ambient:    {celsius_to_fahrenheit(22)}")
print(f"friction:   {celsius_to_fahrenheit(0)}")
print(f"ddt:        {celsius_to_fahrenheit(25)}")

print("\nFahrenheit to Celsius")
print("---------------------")
print(f"flour:      {fahrenheit_to_Celsius(72)}")
print(f"levain:     {fahrenheit_to_Celsius(78)}")
print(f"ambient:    {fahrenheit_to_Celsius(72)}")
print(f"friction:   {fahrenheit_to_Celsius(32)}")
print(f"ddt:        {fahrenheit_to_Celsius(78)}")
"""