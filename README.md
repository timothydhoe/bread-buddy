# Bread Mate

*Bake by Numbers*

A calculator app that helps bakers

## TODOs

~~**Baker's percentage calculator** - the bread baker's holy grail. Input flour weight, get all other ingredients as percentages or vice versa~~

~~**Hydration calculator** - water/flour ratio, shows if dough will be sticky/stiff~~

~~**Desired dough weight** → ingredients - "I want 800g of dough" → breaks down flour, water, salt, yeast~~

~~**Recipe scaler** - scale any recipe up/down by portions or total weight~~

Really handy:

~~**Water temperature calculator** - factors in flour temp, room temp, friction factor to hit target dough temp~~

~~**Autolyse timer** - just a simple reminder, but bakers forget~~

~~**Bulk fermentation time adjuster** - warmer room = shorter time~~

Nice-to-haves:

**Sourdough feeding calculator** - starter ratios

**Flour substitution ratios** - swapping whole wheat for AP flour (affects hydration)

**Oven spring estimator** - how much will dough rise in oven

**Unit conversions** - cups to grams? Necessary?

## Refactoring:

**Check variable names** --> are they meaningful? Clear?

**check keyword arguments consistency** --> Same words/patterns across functions

⚠️ **Add docstrings to all functions** --> complete and consistency. I'm going to forget what functions do!

⚠️ **Add input validation** --> negative temps? flour = 0? Check edge cases

**Extract magic numbers to constants** --> like the 1.12 factor in fermentation, friction factors, etc. Put them at top of file

**Add a constants.py file?** --> for default temps, common ratios, friction factors ?too much??

⚠️ **Consistent return types** --> some functions return dicts, some tuples, some strings. Pick one pattern? Which one would suit the app better?

**Add type hints** --> `def bakers_percentage(flour_weight: int, percentages: dict) -->> dict:` Good idea! 💡

⚠️ **Error handling in calculators** --> How to deal with bad/wrong data(types) in your functions?

At the end:

**Remove debug print statements** --> in main.py

**DRY principle** --> repeating any logic that could be a helper function?

**Error handling** --> check for crashes, make them failures.

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


## Resources

As an amateur baker, I like good resources on bread baking. So, I'll be listing all resources I'm using here. Most will be books, as I prefer that medium when baking bread and researching topics.

> Leo M. (2022), *The perfect Loaf, The Craft and Science of Sourdough Breads, Sweets, and More*. Clarkson Potter Publishers