"""
filename: utils.py
-------------------------------

Helper functions for Bread Buddy.
"""

FAHRENHEIT_MULTIPLIER = 1.8
FAHRENHEIT_OFFSET = 32
MINUTES_PER_HOUR = 60


def celsius_to_fahrenheit(C):
    """Converts Celsius to Fahrenheit."""
    return round((C * FAHRENHEIT_MULTIPLIER) + FAHRENHEIT_OFFSET, 1)


def decimal_hours_to_time(hours):
    """Convert decimal hours to a human-readable string (e.g. 1.5 → '1h 30min')."""
    h = int(hours)
    m = int((hours - h) * MINUTES_PER_HOUR)
    return f"{h}h {m}min"
