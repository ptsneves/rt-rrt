Attempt at implementation of rt-rrt algorithm from the paper in [1].

I am not sure that my implementation is correct, as I assume that the agent does not attempt to have information on all the environment before it calculates the path.

Running this script always generates a different map of obstacles, which in addition to the randomness of the algorithm itself, makes tight test case constraining hard.

The obstacles are deliimited by circles in red.
The start is at the top-left of the map in cyan, while the end is at the bottom-right end of the map.

The green path shows the path done by a supposed agent before it has explored the obstacle map. Basically the output of algorithm2. As can be seen the green line can get messy, and this would reflect the real exploration that an agent would do to reach a given target for the first time.

The black line is an optimized path from x0 to goal, in that it tries to minimize the distance between x0 and goal given the explored nodes. This optimization can improve if multiple passes of algorithm2 could be run but I am not at that stage yet.

I will try to improve the cleaningness of the python code and make it the most readable and self-contained possible.

License is GPLv3 except with permission from me.

[1] https://mediatech.aalto.fi/~phamalainen/FutureGameAnimation/p113-naderi.pdf
