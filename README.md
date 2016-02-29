# dogduck.py

## Usage:
```
    python dogduck.py [speed of duck / speed of dog]
```

This is my first attempt at using `pygame` and it turned out to be easier than expected.

Some friends and I were working on [538 blog's dog and duck riddle](http://fivethirtyeight.com/features/will-the-dog-catch-the-duck/), and wanted a tool to visualize / compare different strategies.

At the moment, the `duck_p` and `dog_p` functions return the next position for the dog and duck, given the dog and duck's current position and velocity.

We did not figure out the solution in time, but weren't too far off.
The official solution for the duck's motion is currently in `duck_p`, other ideas are commented out.

Setting `GRAPHICS = False` will disable `pygame` visualization, and simply print the result of the simulation.
