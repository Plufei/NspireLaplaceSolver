# NspireLaplaceSolver
Various calculators designed to deconstruct complex laplace tranformations problems and solve in a stepwise manner, without the use of python libraries like numpy.

_How to use_

**laplaceuf.py**

Find the properties of P(t), the function preceeding the unit function.

Enter the degree of the polynomial. 

Enter coefficients in ascending order:

c0 = constant

c1 = coefficient of t

c2 = coefficient of t^2

Enter the shift a from U(t-a)

**laplacetbl.py (laplacetranformer)**

Choose mode

Number of terms

Input the turms

Produces time-domain result, stepwise

**laplaceivprr.py (initialvalueproblem)**

This script solves:

First and second order non-homogenous differentials

g(t) is a sum of terms, Ce^rt

select mode and input terms.

Produces stepwise results.

**pydiffy.py (simpledifferentialsolver)**

This script solves simple 1st and 2nd order differentials

Use is self-explanatory

**laplacespecial.py**

Solves highly complex laplace transformations, Impulse, RLC problems, exponential-shift laplace, convolution, and piecewise-constant laplace transformers.

Use of the script varies depending on the selected function.

Use is largely self-explanatory.

**laplacespecial.py, impulsesolver**

Select mode 5.

For a problem in the form

y'' + ω²y = A δ(t − a)

Solution will be outputted stepwise.

**impulseode.py, impulseodesolver**

Capable of solving complicated ODE impulse problems.

Solution will be outputted stepwise.
