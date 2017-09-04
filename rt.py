#!/usr/bin/python3

import random
import math

X = 0
Y = 1

DISTANCE = 0
NODE = 1

#NODE
POSITION = 0
PARENT = 1
COST = 2
def isPointInSegment(pv1, pv2, point):
  return isColinear(pv1, pv2, point) and isPointContainedInRange(pv1, point, pv2)

def isPointContainedInRange(p1, p2, p3):
  return (p1 <= p2 <= p3 or p3 <= p2 <= p1) and (p1 != p3 or p1 == p2 == p3)

#def getObstaclesInRange(vector, origin, space):
#  obstacles = []
#  x_min = x_max = math.ceil(origin[X])
#  y_min = y_max = math.ceil(origin[Y])
#
#  if vector[X] <= 0:
#    x_min = max(math.ceil(origin[X] + vector[X]), 0)
#  else:
#    x_max = min(math.ceil(origin[X] + vector[X]), len(space))
#
#  if vector[Y] <= 0:
#    y_min = max(math.ceil(origin[Y] + vector[Y]), 0)
#  else:
#    y_max = min(math.ceil(origin[Y] + vector[Y]), len(space[0]))
#
#  print(x_min, x_max, y_min, y_max)
#  if x_min != x_max:
#    for x in range(x_min, x_max):
#      if y_min != y_max:
#        for y in range(y_min, y_max):
#          if space[x][y] == 1:
#            obstacles.append([x,y])
#      else:
#        if space[x][y_min] == 1:
#          obstacles.append([x,y_min])
#  else:
#    for y in range(y_min, y_max):
#      if space[x_min][y] == 1:
#        obstacles.append([x_min,y])
#
#  return obstacles

def doCrossProduct(vector1, vector2):
  return vector1[X] * vector2[Y] - vector1[Y] * vector2[X]

def isColinear(point1, point2, point3):
  v1 = getVector(point1, point2)
  v2 = getVector(point1, point3)
  r = doCrossProduct(v1, v2)
  if r == 0:
    return True
  else:
    return False

def getVector(point1, point2):
  dx = point2[X] - point1[X]
  dy = point2[Y] - point1[Y]
  return [dx, dy]

def generateSpace(xdim, ydim):
  space = [[0] * xdim for x in range(ydim)]
  for x in range(0, xdim):
    for y in range(0, ydim):
      if x == 0 or y == 0 or x == xdim-1 or y == ydim-1:
        space[x][y] = 1
      #elif random.randint(1,6) == 2:
      #  space[x][y] = 1

  return space

def getDotProduct(vector1, vector2):
  return vector1[X] * vector2[X] + vector1[Y] * vector2[Y]

def getScalarProjection(vector1, vector2):
  vector2_norm = getVectorNorm(vector2)
  normalized_vector2 = [vector2[0]/vector2_norm, vector2[1]/vector2_norm]
  return getDotProduct(vector1, normalized_vector2)

def getScalarProduct(a, v1):
  return [a * v1[X], a * v1[Y]]

def getProjectedPoint(p, v):
  return [p[X] + v[X], p[Y] + v[Y]]

def getVectorProjection(vector1, vector2):
  a_dot_b = getDotProduct(vector1, vector2)
  b_dot_b = getDotProduct(vector2, vector2)
  return getScalarProduct(a_dot_b / b_dot_b, vector2)

def getVectorNorm(v):
  return math.sqrt(getSquaredLength(v))

def getSquaredLength(v):
  return v[X]**2 + v[Y]**2

def getObstaclesInRange(vector, origin, space):
  obstacles = []
  for x in range(0, xdim):
    for y in range(0, ydim):
      if space[x][y] == 1 and getVectorNorm(getVector(origin, [x, y])) < getVectorNorm(vector):
        obstacles.append([x, y])
  return obstacles

def printSpace(space):
  for row in space:
    print(row)

xdim = 20
ydim = 20
origin = [1.0, 0.0]
vector = [-5.0, 0.0]

space = generateSpace(xdim, ydim)

obstacles = getObstaclesInRange(vector, origin, space)
print(obstacles)
printSpace(space)

#https://stackoverflow.com/a/1079478/227990
def getObstacle(obstacles, current_position, move_vector, obstacle_radius = 1.0):
  obstacles_in_the_way = []
  for obstacle in obstacles:
    a = current_position
    c = obstacle
    AB = move_vector
    AC = getVector(a, obstacle)

    #if distance from origin to radius is already in the circle, its a match
    if getVectorNorm(AC) < obstacle_radius:
      obstacles_in_the_way.append(obstacle)
    else:
      AD = getVectorProjection(AC, AB)

      #if the projection is null then point a = d
      #the projection may be null if c is perpendicular to AB passing through a
      #Distance still needs to be checked because it can be perpendicular but out
      #outside radius
      d = getProjectedPoint(a, AD)

      #if the projected point is not inside the segment AB then distance
      #check is not valid.
      if isPointInSegment(a, getProjectedPoint(a, AB), d):
        distance = getVectorNorm(getVector(d, c))
        if distance < obstacle_radius:
          obstacles_in_the_way.append(obstacle)
  return obstacles_in_the_way

def hasNoObstacle(obstacle, current_position, move_vector, obstacle_radius = 1.0):
  return len(getObstacle(obstacle, current_position, move_vector, obstacle_radius)) == 0

def getLineTo(a, b):
  return getVector(a, b)

def getUniform(start, end):
    return random.uniform(end, start)

def getSamplePosition(x_0, x_goal, a = 0.1, b = 0.5):
  current_position = x_0[POSITION]
  goal = x_goal[POSITION]

  Pr = random.random()
  sample_position = [0, 0]
  if Pr > 1 - a:
    random_vector = getScalarProduct(random.uniform(0.0, 1.0), getLineTo(current_position, goal))
    sample_position = getProjectedPoint(current_position, random_vector)
  #elif Pr <= (1 - a) / b:
  else:
    print(current_position, goal)
    sample_position[X] = getUniform(current_position[X], goal[X])
    sample_position[Y] = getUniform(current_position[Y], goal[Y])

  return sample_position

def getNodeDistance(node1, node2):
  return getVectorProjection(getVector(node1[POSITION], node2[POSITION]))

def getNodesFromGrid(X_SI, node):
  if X_SI:
    return X_SI[math.floor(node[POSITION][X])][math.floor(node[POSITION][Y])]
  else:
    return []

def addNodeToGrid(X_SI, node):
  X_SI[math.floor(node[POSITION][X])][math.floor(node[POSITION][Y])].append(node)

#closest nodes cannot be empty no checking is done
def getClosestNode(position, closest_nodes):
  smallest_distance = getNodeDistance(position, closest_node[0][POSITION])
  closest_node = closest_nodes[0]

  if len(closest_nodes) > 1:
    for node in closest_nodes[1:]:
      distance = getNodeDistance(position, node[POSITION])
      if distance < smallest_distance:
        closest_node = node
        smallest_distance = distance

  ret_val[NODE] = closest_node
  ret_val[DISTANCE] = smallest_distance
  return ret_val

def getCost(x_parent, x_new):
  return x_parent[COST] + getNodeDistance(x_parent, x_new)

def addNodeToTree(obstacles, x_new, x_closest, X_near):
  x_min = x_closest
  c_min = getCost(x_closest, x_new)
  if len(X_near) > 1:
    for x in X_near[1:]:
      c_new = getCost(x, x_new)
      if c_new < c_min and hasNoObstacle(obstacles, x[POSITION], x_new[POSITION]):
        x_min = x
        c_min = c_new
  x_new[PARENT] = x_min

def rewireFromRoot(obstacles, x0, qs, X_SI):
  if len(qs) == 0:
    qs.append(x0)

  qs_popped = []
  while len(qd) != 0:
    x_s = qs.pop(0)
    qs_popped.append(x_s)
    X_near = getNodesFromGrid(X_SI, x_s)
    for x_near in X_near:
      c_old = x_near[COST]
      c_new = getCost(x_s, x_near)
      if c_new < c_old and hasNoObstacle(obstacles, x_s[POSITION], x_near[POSITION]):
        x_near[PARENT] = x_s
      if x_near not in qs_popped:
        qs.append(x_near)

def rewireRandomNode(obstacles, qr, X_SI):
  while len(qr) != 0:
    x_r = qr.pop(0)
    X_near = getNodesFromGrid(X_SI, x_r)
    for x_near in X_near:
      c_old = x_near[COST]
      c_new = getCost(x_r, x_near)
      if c_new < c_old and hasNoObstacle(obstacles, x_r[POSITION], x_near[POSITION]):
          x_near[PARENT] = x_r
          qr.append(x_near)

def algorithm2(x_0, x_goal, obstacles, X_SI, qr, qs, kmax, rs):
  x_rand[POSITION] = getSamplePosition(x_0, goal)
  x_rand[COST] = float('nan')
  x_rand[PARENT] = []

  X_near = getNodesFromGrid(X_SI, x_0)
  if len(X_near) != 0:
    result = getClosestNode(x_0, X_near)
    x_closest = result[NODE]
    distance_closest = result[DISTANCE]
  else:
    x_closest = x_0
    distance_closest = getNodeDistance(x_0, x_rand)

  if hasNoObstacle(obstacles, x_closest[POSITION], x_rand[POSITION]):
    if len(X_near) < k_max or distance_closest > rs:
      addNoteToTree(obstacles, x_rand, x_closest, X_near, obstacles)
      addNodeToGrid(X_SI, x_rand)
      qr.insert(0, x_rand)
      if getNodeDistance(x_rand, x_goal) <= rs:
        goal_node = x_rand
    else:
      qr.insert(0, x_closest[NODE])
    rewireRandomNode(obstacles, qr, X_SI)
  rewireFromRoot(obstacles, x_0, qs, X_SI)
  return goal_node

def algorithm6(x_0, x_goal):

x_goal[POSITION] = [10.0, 10.0]
x_goal[COST] = 0
x_goal[PARENT] = []

x_0[POSITION] = [3.0, 1.0]
x_0[COST] = getNodeDistance(x_goal, x_0)
x_0[PARENT] = []

algorithm2(x_0, x_goal, [], [], 10.0, 1)

if getVectorProjection([3.0, -8.0], [1.0, 2.0]) != [-2.6, -5.2]:
  raise Exception("Error")

if not isColinear([1,1], [2,2], [3,3]):
  raise Exception("Error")

if isColinear([1,0.9], [2,2], [3,3]):
  raise Exception("Error")

if isPointInSegment([1.0, 1.0], [1.0, 1.0], [2.0, 2.0]):
  raise Exception("Error")

if not isPointInSegment([1.0, 1.0], [1.0, 1.0], [1.0, 1.0]):
  raise Exception("Error")

if not isPointInSegment([1,1], [3,3], [2,2]):
  raise Exception("Error")

if isPointInSegment([1,1], [2,2], [3,3]):
  raise Exception("Error")

if not isPointInSegment([1,1], [2,2], [2,2]):
  raise Exception("Error")

if isPointInSegment([1.0, 0.0], [-4.0, 0.0], [5.0, 0.0]):
  raise Exception("Error")

if getObstacle([1.0, 0.0], [-5.0, 0.0]) != [[0.0, 0.0], [1.0, 0.0]]:
  raise Exception("Error")

if getObstacle([6.0, 1.0], [-5.0, 0.0]):
  raise Exception("Error")

if getObstacle([0.0, 0.0], [0.0, -1.0]) != [[0.0, 0.0]]:
  raise Exception("Error")

if getObstacle([0.0, 1.0], [0.0, -1.0]) != [[0.0, 0.0], [0.0, 1.0]]:
  raise Exception("Error")

