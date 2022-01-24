#!/usr/bin/python3
import random
import math_utils
import node
from node_clusters import NodeClusters


def getObstacle(obstacles, current_position, new_position, obstacle_radius=1.0, return_on_obstacle=False):
    obstacles_in_the_way = []
    for obstacle in obstacles:
        vec_to_obstacle = current_position.vectorTo(obstacle)
        if vec_to_obstacle.norm() <= obstacle_radius:
            print("Point inside obstacle")
            exit(1)
        cx = obstacle.x()
        cy = obstacle.y()
        ax = current_position.x()
        ay = current_position.y()
        bx = new_position.x()
        by = new_position.y()
        r = obstacle_radius
        ax -= cx
        ay -= cy
        bx -= cx
        by -= cy
        a = ax ** 2.0 + ay ** 2.0 - r ** 2.0
        b = 2.0 * (ax * (bx - ax) + ay * (by - ay))
        c = (bx - ax) ** 2.0 + (by - ay) ** 2.0
        t = math_utils.solveQuadratic(a, b, c)

        if not t:
            continue

        if (t[0] and 0.0 < t[0] < 1.0) or (t[1] and 0.0 < t[1] < 1.0):
            obstacles_in_the_way.append(obstacle)
            print("Cur, New, obstacle, radius:", current_position, new_position, obstacle, obstacle_radius)
            print("a,b,c,t:", a, b, c, t)
            print()

            if return_on_obstacle:
                break
    # print(len(obstacles_in_the_way))
    return obstacles_in_the_way


def hasObstacle(obstacles, current_position, new_position, obstacle_radius=0.6):
    return len(getObstacle(obstacles, current_position, new_position, obstacle_radius, True)) != 0


def getSamplePosition(x_0, x_goal, a=0.1, b=0.5):
    current_position = x_0.position()
    goal = x_goal.position()

    pr = random.random()
    if pr > 1 - a:
        curpos_to_goal_vector = current_position.vectorTo(goal)
        random_vector = curpos_to_goal_vector.scalarProduct(random.uniform(0.0, 1.0))
        return current_position.projectedPoint(random_vector)
    # elif pr <= (1 - a) / b:
    # I do not know how to calculate b
    else:
        return math_utils.Point(
            math_utils.getUniform(current_position.x(), goal.x()),
            math_utils.getUniform(current_position.y(), goal.y())
        )


def addNodeToTree(obstacles, x_new, x_closest, near_nodes):
    x_min = x_closest
    minimum_cost = x_closest.costTo(x_new)
    for x in near_nodes:
        new_cost = x.costTo(x_new)
        if new_cost < minimum_cost and not hasObstacle(obstacles, x.position(), x_new.position()):
            x_min = x
            minimum_cost = new_cost
    x_new.setParent(x_min)
    x_new.setCost(minimum_cost)


def rewireFromRoot(obstacles, x0, qs, node_clusters):
    if len(qs) == 0:
        qs.append(x0)

    qs_popped = []
    while len(qs) != 0:
        x_s = qs.pop(0)
        qs_popped.append(x_s)
        cluster_nodes = node_clusters.getNodes(x_s)
        for x_near in cluster_nodes:
            if x_s.costTo(x_near) < x_near.cost() and not hasObstacle(obstacles, x_s.position(), x_near.position()):
                x_near.setParent(x_s)
            if x_near not in qs_popped:
                qs.append(x_near)


def rewireRandomNode(obstacles, qr, clusters):
    while len(qr) != 0:
        x_r = qr.pop(0)
        cluster_nodes = clusters.getNodes(x_r)
        for x_near in cluster_nodes:
            if x_r.costTo(x_near) < x_near.cost() and not hasObstacle(obstacles, x_r.position(), x_near.position()):
                x_near.setParent(x_r)
                qr.append(x_near)


def algorithm2(space, x_0, x_goal, clusters, qr, qs, k_max, rs, draw=None):
    new_node = x_0

    x_rand = node.Node(getSamplePosition(x_0, x_goal), float('nan'), None)

    cluster_nodes = clusters.getNodes(x_0)
    if len(cluster_nodes) == 0:
        raise Exception("We always assume the node is in some cluster, so at least it should return itself")
    result = x_0.closest(cluster_nodes)
    x_closest = result.closest()
    distance_closest = result.distance()

    x0_to_xrand = x_0.position().vectorTo(x_rand.position())
    obstacles = space.getObstaclesInRange(x0_to_xrand, x_0.position())

    if not hasObstacle(obstacles, x_closest.position(), x_rand.position()):
        if len(cluster_nodes) < k_max or distance_closest > rs:
            clusters.addNode(x_rand)
            addNodeToTree(obstacles, x_rand, x_closest, cluster_nodes)

            x_rand.print()
            # if draw:
            #     draw.nodes(x_rand[NodeClusters.PARENT], x_rand)
            qr.insert(0, x_rand)
            new_node = x_rand
        else:
            qr.insert(0, x_closest)
        rewireRandomNode(obstacles, qr, clusters)

    rewireFromRoot(obstacles, x_0, qs, clusters)
    return new_node


def optimizePath(space, x_0, x_goal):
    x = x_goal
    while x.parent():
        x_try = x.parent()
        best_parent_node = x_try
        best_cost = x_0.distance(x_try)
        while x_try:
            obstacles = space.getObstaclesInRange(x.vector(x_try), x.position())
            if not hasObstacle(obstacles, x.position(), x_try.position()):
                current_cost = x_0.distance(x_try)
                if current_cost < best_cost:
                    best_parent_node = x_try
                    best_cost = current_cost
            x_try = x_try.parent()

        x.setParent(best_parent_node)
        x = best_parent_node

    return x_goal


