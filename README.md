
# Python scoring algorithm

This python script implement a generic scoring method.

## The story

A group of `N` persons would like to devise a fair way of determining a `score` for each of them
(the score could represent anything one like: best volleyball player, best politician...)

Each person score the others with a number between 0 and 100, which is normalized (sum of score given by each person is 100).
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

The weight is the product of the two normalized values.
The final score is then multiplied by the final fairness factor (we call it the `punished score`)
and normalized again to have an average of 100 (this step is optional, but handy).

In order to have a good score, each person thus should:

1. Have a good scoring from each other person;
2. Have a fair notation to each other person.

The given set of equation is rather complex to solve analytically given it's nature,
but we use the fact that the system is bound to be stable so an iterative solution will
quickly converge to the optimal solution.

The code itself is rather straightforward. The number of iterations is fixed;
but we could instead use a condition on real convergence (computing the relative delta between each iteration).
Given the quick computation and convergence it's probably not worth it.

This code and algorithm are published in the public-domain.

## Example

An example could help. Below the code run on example matrix S3 (see code to see):

```
                     A    B    C    D    E    F    G    H    I
Scoring matrix:  [  --,  95, 114, 152, 114,  38,  38, 152,  95 ] A
                 [  77,  --, 116, 155, 116,  42,  38, 155,  97 ] B
                 [  97,  78,  --, 175, 117,  19,  58, 175,  78 ] C
                 [  84, 105, 147,  --,  84,  63,  42, 168, 105 ] D
                 [  45,  67, 158, 180,  --,  45,  54, 135, 112 ] E
                 [  44,  44,  44, 222, 133,  --,  88, 133,  88 ] F
                 [ 100, 100, 100, 100, 100, 100,  --, 100, 100 ] G
                 [   0,   0,   0,   0,   0, 400, 400,  --,   0 ] H
                 [  34,  34,  69, 417, 139,  34,  34,  34,  -- ] I

                     A    B    C    D    E    F    G    H    I
Raw scores:      [  60,  65,  93, 175, 100,  92,  94, 131,  84 ] 
Adjusted scores: [  69,  77, 113, 175, 102,  62,  63, 142,  92 ] 
Punished scores: [  89, 101, 139, 217, 127,  67,  67,  34,  55 ] 
Fairness factor: [ 124, 127, 118, 119, 120, 104, 103,  23,  57 ] 
```

The scoring matrix reads as follows:
- Row X is the score **given by** X to others.
- Column X is the score **received by** X from others.

Here we have different profiles of scoring:
* A is very fair and precise and has a low raw score of 60.
* B is also very fair and has a raw score a bit higher, 65.
* C is somehow fair, with a medium raw score of 93.
* D is fair, with a large raw score of 175.
* E is fair with a raw score of 100.
* F has a tendancy to exaggerate it's scoring and has a medium raw score of 92.
* G is indecise (score everybody with the same score) with a raw score of 94.
* H is a "cheater" with F and G, with a high raw score of 131.
* I is not fair, tend to exagerate, and has a medium raw score of 84.

In the result, we see 3 rows:

1. The first row is the raw score: the simple normalized average of each score, w/o any weight.
2. The second row is the adjusted score: that's the output of the iterative algorithm.
3. The third row is the punished score: that's the adjusted score weighted with the final fairness factor.
4. The fourth row is the final fairness factor.

Here we see that the fairness factor for H is very low (23). It's final score (34) is rather low compared to its real "raw" score (131). The unpunished score (adjusted score) is 142.

On the other hand, the fairness factor for A and B are very high (124 and 127).
Their final scores (89 and 101) are higher than the raw scores (60 and 65).


