
# Python scoring algorithm

This python script implement a generic scoring method.

## The story

A group of `N` persons would like to devise a fair way of determining a `score` for each of them
(the score could represent anything one like: best volleyball player, best politician...)

Each person score the others with a number between 0 and 100,
the total score given by each person being 100.
Obviously a person does not score itself.

Given this score matrix, how best to determine the fairest score for each person?

## Our solution

We will assume the following:
- The total score for each person is the **weighted average** of each sub-scores,
- The score given by a person is **weighted by its own score** (a person having a high score will have its own scoring having more weight than a person having a low score),
- We neutralize "cheaters" by computing a **fairness factor**, which is based on the standard deviation between the score given by a person and the real computed score
(a person having a low standard deviation between its scoring and the computed score is fair; a high one is unfair).

Each person score is then weighted by:

1. its own score,
2. its fairness factor.

The weight is the product of the two normalized values. The final score is normalized again to have an average of 100 (this step is optional, but handy).

The given set of equation is rather complex to solve analytically given it's nature,
but we use the fact that the system is bound to be stable so an iterative solution will
quickly converge to the optimal solution.

The code itself is rather straightforward. The number of iterations is fixed;
but we could instead use a condition on real convergence (computing the relative delta between each iteration).
Given the quick computation and convergence it's probably not worth it.

This code and algorithm are published in the public-domain.
