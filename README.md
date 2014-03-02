polynomials-python
==================

Implementations for Polynomials for Real Numbers and Finite Fields

polynomials.py
--------------

Contains a Polynomial class for defining polynomials and performing all sorts of arithmetic operations on them.

Initialize a Polynomial with a list of coefficients with the left-most coefficient being the constant term with powers increasing toward the right.

polymod.py
----------

Contains a Mod class for performing modular arithmetic and other operations associated with Mods. All Mods exist in the same space, so call Mod.set_mod(n) prior to using.

This Mod class is then implemented in conjunction with the PolyMod class for performing arithmetic operations on polynomials with modular coefficients. The space in which one is working is mod the number set for all Mod instances using Mod.set_mod.

This class also contains PolyMod.interpolate(points) which takes a list of points (x,y) and produces a unique PolyMod using Lagrange interpolation.
