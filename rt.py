#!/usr/bin/python3

import random
import math

import cairo

X = 0
Y = 1

DISTANCE = 0
NODE = 1

#NODE
POSITION = 0
PARENT = 1
COST = 2

XDIM = 20
YDIM = 20

START_POSITION = [3.0, 1.0]
END_POSITION = [15.0, 10.0]

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


class Draw:
  def __init__(self):
    self.surface = cairo.SVGSurface("output.svg", XDIM*20, YDIM*20)
    self.ctx = cairo.Context(self.surface)
    self.ctx.set_source_rgb(0,0,0)
    self.ctx.set_line_width(0.1)
    self.ctx.scale(20, 20)

  def drawLine(self, p1, p2 = [0.0, 0.0], finish = True):
    self.ctx.move_to(p1[X], p1[Y])
    self.ctx.line_to(p2[X], p2[Y])
    if finish:
      self.finishDrawing()

  def drawNodes(self, node1, node2):
    self.drawLine(node1[POSITION], node2[POSITION])

  def drawObstacle(self, x, y):
    self.ctx.move_to(x, y)
    self.ctx.arc(x, y, 1/20, -math.pi, math.pi)

  def finishDrawing(self):
    self.ctx.stroke()
    #self.ctx.scale(10, 10)

def getVector(point1, point2):
  dx = point2[X] - point1[X]
  dy = point2[Y] - point1[Y]
  return [dx, dy]

def generateSpace(XDIM, YDIM, draw = None):
  space = [[0] * XDIM for x in range(YDIM)]
  for x in range(0, XDIM):
    for y in range(0, YDIM):
      if [x,y] != START_POSITION and [x,y] != END_POSITION and(  x == 0 or y == 0 or x == XDIM-1 or y == YDIM-1 or random.randint(1,6) == 2):
        space[x][y] = 1
        if draw:
          draw.drawObstacle(x, y)
  space[8][8] = 1
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
  for x in range(0, XDIM):
    for y in range(0, YDIM):
      if space[x][y] == 1 and getVectorNorm(getVector(origin, [x, y])) < getVectorNorm(vector):
        obstacles.append([x, y])
  return obstacles

def printSpace(space):
  for row in space:
    print(row)

#https://stackoverflow.com/a/1079478/227990
def getObstacle(obstacles, current_position, move_vector, obstacle_radius = 10.0):
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
    sample_position[X] = getUniform(current_position[X], goal[X])
    sample_position[Y] = getUniform(current_position[Y], goal[Y])

  return sample_position

def getNodeDistance(node1, node2):
  return getVectorNorm(getVector(node1[POSITION], node2[POSITION]))

class NodeGrid:

  class GridElement:
    def __init__(self, node):
      self.x = math.floor(node[POSITION][X])
      self.y = math.floor(node[POSITION][Y])
      self.nodes = [node]

    def containsNode(self, node):
      return math.floor(node[POSITION][X]) == self.x and math.floor(node[POSITION][Y]) == self.y

  def __init__(self):
    self.grid_elements = []

  def getNodesFromGrid(self, node):
    for e in self.grid_elements:
      if e.containsNode(node):
        return e.nodes
    return []

  def addNodeToGrid(self, node):
    for e in self.grid_elements:
      if e.containsNode(node):
        e.nodes.append(node)
        return
    self.grid_elements.append(self.GridElement(node))


#closest nodes cannot be empty no checking is done
def getClosestNode(position, closest_nodes):
  smallest_distance = getNodeDistance(position, closest_nodes[0])
  closest_node = closest_nodes[0]

  if len(closest_nodes) > 1:
    for node in closest_nodes[1:]:
      distance = getNodeDistance(position, node)
      if distance < smallest_distance:
        closest_node = node
        smallest_distance = distance

  ret_val = [0,0]
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
  x_new[COST] = c_min

def rewireFromRoot(obstacles, x0, qs, X_SI):
  if len(qs) == 0:
    qs.append(x0)

  qs_popped = []
  while len(qs) != 0:
    x_s = qs.pop(0)
    qs_popped.append(x_s)
    X_near = X_SI.getNodesFromGrid(x_s)
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
    X_near = X_SI.getNodesFromGrid(x_r)
    for x_near in X_near:
      c_old = x_near[COST]
      c_new = getCost(x_r, x_near)
      if c_new < c_old and hasNoObstacle(obstacles, x_r[POSITION], x_near[POSITION]):
          x_near[PARENT] = x_r
          qr.append(x_near)

def printNode(node):
  if node[PARENT]:
    print("POSITION {}\nCOST{}\nPARENT_POS {}\n".format(node[POSITION], node[COST], node[PARENT][POSITION]))
  else:
    print("ROOT: POSITION {}\nCOST{}\n".format(node[POSITION], node[COST]))

def algorithm2(space, x_0, x_goal, X_SI, qr, qs, k_max, rs, draw = None):
  new_node = x_0

  x_rand = [[], 0.0, []]
  x_rand[POSITION] = getSamplePosition(x_0, x_goal)
  x_rand[COST] = float('nan')
  x_rand[PARENT] = []


  X_near = X_SI.getNodesFromGrid(x_0)
  if len(X_near) != 0:
    result = getClosestNode(x_0, X_near)
    x_closest = result[NODE]
    distance_closest = result[DISTANCE]
  else:
    x_closest = x_0
    distance_closest = getNodeDistance(x_0, x_rand)

  obstacles = getObstaclesInRange(getVector(x_0[POSITION], x_rand[POSITION]), x_0[POSITION], space)
  if hasNoObstacle(obstacles, x_closest[POSITION], x_rand[POSITION]):
    if len(X_near) < k_max or distance_closest > rs:
      X_SI.addNodeToGrid(x_rand)
      addNodeToTree(obstacles, x_rand, x_closest, X_near)
      printNode(x_rand)
      if draw:
        draw.drawNodes(x_rand[PARENT], x_rand)
      qr.insert(0, x_rand)
      new_node = x_rand
    else:
      qr.insert(0, x_closest[NODE])
    rewireRandomNode(obstacles, qr, X_SI)
    rewireFromRoot(obstacles, x_0, qs, X_SI)
  return new_node

def algorithm6(x_0, x_goal):
  x = x_goal
  while x[PARENT] != []:
    print(x[PARENT])
    x = x[PARENT]

draw = Draw()
space = generateSpace(XDIM, YDIM, draw)
printSpace(space)


x_goal = [[], 0.0, []]
x_goal[POSITION] = END_POSITION
x_goal[COST] = 0.0
x_goal[PARENT] = []

x_0 = [[], 0.0, []]
x_0[POSITION] = START_POSITION
x_0[COST] = getNodeDistance(x_goal, x_0)
x_0[PARENT] = None

X_SI = NodeGrid()
X_SI.addNodeToGrid(x_0)

x = x_0
printNode(x)
while getNodeDistance(x, x_goal) >= 1.0:
  x = algorithm2(space, x, x_goal, X_SI, [], [], 10.0, 1.0, draw)



print("Reached")
#algorithm6(x_0, x)

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

#if getObstacle(obstacles, [1.0, 0.0], [-5.0, 0.0]) != [[0.0, 0.0], [1.0, 0.0]]:
#  raise Exception("Error")
#
#if getObstacle(obstacles, [6.0, 1.0], [-5.0, 0.0]):
#  raise Exception("Error")
#
#if getObstacle(obstacles, [0.0, 0.0], [0.0, -1.0]) != [[0.0, 0.0]]:
#  raise Exception("Error")
#
#if getObstacle(obstacles, [0.0, 1.0], [0.0, -1.0]) != [[0.0, 0.0], [0.0, 1.0]]:
#  raise Exception("Error")
#
