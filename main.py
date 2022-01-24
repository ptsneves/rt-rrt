#!/usr/bin/env python3
import sys

import math_utils
import node
import node_clusters
import rt
import world_map
from draw import Draw


# if hasObstacle([[15.0, 0]], [3.0, 1.0], [15.0, 0.5], 0.4):
#  raise Exception("Tangent failed")

# C = [15.0, 3.0]
# A = [3.0, 5.0]
# B = [15.0, 3.5]
# r = 1.0
# draw.circle(C[.x()], C.y(), [0,0,0], r)
# draw.drawLine(A, B)
# if not rt.hasObstacle([C], A, B, r):
#     raise Exception("1 Intersection failed")

# C = [15.0, 3.0]
# A = [3.0, 5.0]
# B = [18.0, 3.5]
# r = 1.0
# draw.circle(C[.x()], C.y(), [0,0,0], r)
# draw.drawLine(A, B)
# if not rt.hasObstacle([C], A, B, r):
#     raise Exception("2 Intersection failed")

# C = [15.0, 3.0]
# A = [14.6, 2.5]
# B = [15.6, 2.5]
# r = 1.0
# draw.circle(C[.x()], C.y(), [0,0,0], r)
# draw.drawLine(A, B)
# if hasObstacle([C], A, B, r):
#  raise Exception("Interior failed")

# C = [15.0, 3.0]
# A = [2.0, 2.0]
# B = [15.6, 2.00001]
# r = 1.0
# # draw.circle(C[.x()], C.y(), [0,0,0], r)
# # draw.drawLine(A, B)
# if not rt.hasObstacle([C], A, B, r):
#     raise Exception("Tangent failed")
#
# if rt.hasObstacle([[2.0, 20.0]], [3.0, 1.0], [2.414938958075008, 19.628051833539704], 0.1):
#     raise Exception("Error")
# print("Succ")

# ---------------------


def main():
    pos_0 = math_utils.Point(6.0, 3.0)
    pos_goal = math_utils.Point(15.0, 15.0)
    grid_width = 20
    grid_height = 20

    draw = Draw(grid_width, grid_height)
    space = world_map.WorldMap([pos_0, pos_goal], grid_width, grid_height)
    space.drawWorld(draw.obstacle, draw.walls, draw.start_end)

    # draw.line([5.0, 5.0], [6.0, 5.0], [0, 0, 1])

    x_goal = node.Node(pos_goal, 0.0, [])
    x_0 = node.Node(
        pos_0,
        pos_0.vectorTo(x_goal.position()).norm(),
        None)

    clusters = node_clusters.NodeClusters()
    clusters.addNode(x_0)

    x = x_0
    x.print()
    while x.distance(x_goal) >= 0.6:
        x = rt.algorithm2(space, x, x_goal, clusters, [], [], 10.0, 10.0, None)

    print("Reached")

    draw.tree(clusters)
    draw.route(x)
    x = rt.optimizePath(space, x_0, x)
    draw.route(x, [0, 0, 0])
    return 0


if __name__ == '__main__':
    sys.exit(main())
