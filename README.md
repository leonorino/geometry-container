# geometry-container

This repository contains:
* Point module.
* Vector module.
* Container module.
* An interactive CLI in main.py.

To-Do list:
- [x] 3D features.
- [x] Documentation.
- [ ] 2D features.

By the way, point is [this](https://en.wikipedia.org/wiki/Point_(geometry)) and vector is [this](https://en.wikipedia.org/wiki/Euclidean_vector).

If you didn't really understand what a vector is from a link above, here's an image:
![Vector](https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Vector_from_A_to_B.svg/2880px-Vector_from_A_to_B.svg.png)

Now *that* is one **big**, and I mean **HUGE** vector. Am I obsessed with *vectors*? ~~Absolutely not~~ **Maybe**.

## Did you know how to calculate Vector's length?
$$l = \sqrt{a^2 + b^2+c^2}$$

That's how!!!

### Ah, almost forgot.

Here's how you create a vector using my modules:

```py
beautiful_vector = Vector(2, 3, 5)
# or even like that:
even_more_beautiful_vector = Vector(2, 3, 6, start_point=Point(1, 1, 1))
```
