# Bread Buddy

*Bake by Numbers*

A calculator app that helps bakers

## TODOs

essentials and must-haves:

~~**Baker's percentage calculator** - the bread baker's holy grail. Input flour weight, get all other ingredients as percentages or vice versa~~

~~**Hydration calculator** - water/flour ratio, shows if dough will be sticky/stiff~~

~~**Desired dough weight** → ingredients - "I want 800g of dough" → breaks down flour, water, salt, yeast~~

~~**Recipe scaler** - scale any recipe up/down by portions or total weight~~

~~**Water temperature calculator** - factors in flour temp, room temp, friction factor to hit target dough temp~~

~~**Autolyse timer** - just a simple reminder, but bakers forget~~

~~**Bulk fermentation time adjuster** - warmer room = shorter time~~

~~**Sourdough feeding calculator** - starter ratios~~

Nice-to-haves:

**Process time calculator** -- When to start if you want to finish by a certain time
                            --> need full recipe for that?

**Pre-fermented Flour percentage** -- pp.130-131

**Levain percentage** -- pp.130-131

**Flour substitution ratios** - swapping T60 wheat for T150 wheat? Or swapping Rye for Spelt? (affects hydration)

**Oven spring estimator** - how much will dough rise in oven? Can this be calculated?

**Unit conversions** - cups to grams? Necessary? --> maybe not, use grams only? 🤔


## Refactoring:

**Check variable names** --> are they meaningful? Clear?

**check keyword arguments consistency** --> Same words/patterns across functions

~~⚠️ **Add docstrings to all functions** --> complete and consistency. I'm going to forget what functions do!~~

⚠️ **Add input validation** --> negative temps? flour = 0? Check edge cases

**Extract magic numbers to constants** --> like the 1.12 factor in fermentation, friction factors, etc. Put them at top of file

**Add a constants.py file?** --> for default temps, common ratios, friction factors ? too much, though??

~⚠️ **Consistent return types** --> some functions return dicts, some tuples, some strings. Pick one pattern? Which one would suit the app better? ALL SHOULD RETURN DICT.~

**Add type hints** --> `def bakers_percentage(flour_weight: int, percentages: dict) -->> dict:` Good idea! 💡

⚠️ **Error handling in calculators** --> How to deal with bad/wrong data(types) in your functions?

At the end:

**Remove debug print statements** --> in main.py

**DRY principle** --> repeating any logic that could be a helper function?

**Error handling** --> check for crashes, make them failures.
                   --> adding exit codes?

**Unit tests** --> test calculations (pytest!)

## App Name ideas

**Bread Mate**
**Baker's Mate**
**Baker's Buddy**
**Bread Buddy**

**Baker's Compass**
**Dough Math**
**The Crumb Calculator**
**Levain Logic**
**The Baker's Atlas**
**Dough Decoder**
**Baker's Metric**

## Comments and Docstrings

I'm using [Google's docstring style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

All ratios in the ap

## Baker's percentage *aka baker's math*

The baker's percentage is a bit different from how mathematicians would look at percentages.

The key part to understand about using baker's percentages is that all the flour used in a formula will always add up to 100%.
The flour is the main ingredient to which all other ingredients are compared, and the other ingredients are expressed as a percentage of the total flour weight.

## Ratios and weights

All ratios in the app are programmed as 1 for 100%. This makes it easier to do the math.
```bash
.2 = 20%
.02 = 2%

.5 = 50%
.05 = 5%

1 = 100%
1.02 = 102%
1.2 = 120%
```

All weights are in grams. Yes, even liquids. This makes it accurate to measure and makes a recipe repeatable.

## Terminology

I will assume that not every programmer is a baker. So, here's a list that you can reference if some jargon ever leaves you baffled.
I will do my utmost best to keep this list both updated and alphabetical. Yet, I won't make any promises that this is list will be up-to-date at all times.

**Inoculation**
: *Ripe Sourdough Carryover*


## Resources

As an amateur baker, I like good resources on bread baking. So, I'll be listing all resources I'm using here. Most will be books, as I prefer that medium when baking bread and researching topics.

> Leo M. (2022), *The perfect Loaf, The Craft and Science of Sourdough Breads, Sweets, and More*. Clarkson Potter Publishers