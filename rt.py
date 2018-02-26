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

START_POSITION = [3.0, 3.0]
END_POSITION = [15.0, 15.0]

class Draw:
  SCALE = 20.0
  narrow_line_width = 0.05
  line_width = 0.1

  def __init__(self):
    self.surface = cairo.SVGSurface("output.svg", XDIM * Draw.SCALE, YDIM * Draw.SCALE)
    self.ctx = cairo.Context(self.surface)
    self.ctx.set_source_rgb(0,0,0)
    self.ctx.set_line_width(self.line_width)
    self.ctx.scale(Draw.SCALE, Draw.SCALE)

  def drawLine(self, p1, p2 = [0.0, 0.0], color = [0,0,0]):
    self.ctx.set_source_rgb(color[0], color[1], color[2])
    self.ctx.set_line_width(self.line_width)
    self.ctx.move_to(p1[X], p1[Y])
    self.ctx.line_to(p2[X], p2[Y])
    self.ctx.stroke()

  def drawNarrowLine(self, p1, p2 = [0.0, 0.0], color = [.7, .7, .7]):
    self.ctx.set_source_rgb(color[0], color[1], color[2])
    self.ctx.set_line_width(self.narrow_line_width)
    self.ctx.move_to(p1[X], p1[Y])
    self.ctx.line_to(p2[X], p2[Y])
    self.ctx.stroke()

  def drawNodes(self, node1, node2):
    self.drawCircle(node1[POSITION][X], node1[POSITION][Y], [0,1.0,0], 0.1)
    self.drawLine(node1[POSITION], node2[POSITION])

  def drawObstacle(self, x, y):
    self.ctx.set_source_rgb(1.0,0,0)
    self.ctx.move_to(x, y)
    self.ctx.arc(x, y, 0.6, -math.pi, math.pi)
    self.ctx.stroke()

  def drawCircle(self, x, y, color, radius= 1.0):
    self.ctx.set_source_rgb(color[0],color[1],color[2])
    self.ctx.move_to(x, y)
    self.ctx.arc(x, y, radius, -math.pi, math.pi)
    self.ctx.stroke()


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

def getScalarProduct(a, v1):
  return [a * v1[X], a * v1[Y]]

def getProjectedPoint(p, v):
  return [p[X] + v[X], p[Y] + v[Y]]

def getVectorNorm(v):
  return math.sqrt(getSquaredLength(v))

def getSquaredLength(v):
  return v[X]**2 + v[Y]**2

def getObstaclesInRange(vector, origin, space, all = False):
  obstacles = []
  for x in range(0, XDIM):
    for y in range(0, YDIM):
      if space[x][y] == 1:# and (all or getVectorNorm(getVector(origin, [x, y])) < getVectorNorm(vector)):
        obstacles.append([x, y])
  return obstacles

def printSpace(space):
  for row in space:
    print(row)

def solveQuadratic(c, b, a):
  disc = b**2.0 - 4.0*a*c
  if disc < 0.0:
    #print("Disc: " + str(disc))
    return None
  disc = math.sqrt(disc)
  x1 = None
  x2 = None
  if b >= 0.0:
    if a >= 0.00000001:
      x1 = (-b - disc) / (2.0*a)
    x2 = (2.0 * c) / (-b - disc)
  else:
    x1 = (2.0 * c) / (-b + disc)
    if a >= 0.00000001:
      x2 = (-b + disc) / (2.0 *a)
  return [x1, x2]

def getObstacle(obstacles, current_position, new_position, obstacle_radius = 1.0, return_on_obstacle = False):

  obstacles_in_the_way = []
  for obstacle in obstacles:
    if getVectorNorm(getVector(current_position, obstacle)) <= obstacle_radius:
      print("Point inside obstacle", current_position, obstacle)
      exit(1)
    cx = obstacle[X]
    cy = obstacle[Y]
    ax = current_position[X]
    ay = current_position[Y]
    bx = new_position[X]
    by = new_position[Y]
    r = obstacle_radius
    ax -= cx
    ay -= cy
    bx -= cx
    by -= cy
    a = ax**2.0 + ay**2.0 - r**2.0
    b = 2.0*(ax*(bx - ax) + ay*(by - ay))
    c = (bx - ax)**2.0 + (by - ay)**2.0
    t = solveQuadratic(a,b,c)

    if not t:
      continue

    if (t[0] and 0.0 < t[0] and t[0] < 1.0) or (t[1] and 0.0 < t[1] and t[1] < 1.0):
        obstacles_in_the_way.append(obstacle)
        print("Cur, New, obstacle, radius:", current_position, new_position, obstacle, obstacle_radius)
        print("a,b,c,t:", a,b,c,t)
        print()

        if return_on_obstacle:
          break
  #print(len(obstacles_in_the_way))
  return obstacles_in_the_way

def hasObstacle(obstacles, current_position, new_position, obstacle_radius = 0.6):
  return len(getObstacle(obstacles, current_position, new_position, obstacle_radius, True)) != 0

def getLineTo(a, b):
  return getVector(a, b)

def getUniform(start, end):
    return random.uniform(0, 20)

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
  for x in X_near:
    c_new = getCost(x, x_new)
    if c_new < c_min and not hasObstacle(obstacles, x[POSITION], x_new[POSITION]):
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
      if c_new < c_old and not hasObstacle(obstacles, x_s[POSITION], x_near[POSITION]):
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
      if c_new < c_old and not hasObstacle(obstacles, x_r[POSITION], x_near[POSITION]):
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
  result = getClosestNode(x_0, X_near)
  x_closest = result[NODE]
  distance_closest = result[DISTANCE]

  obstacles = getObstaclesInRange(getVector(x_0[POSITION], x_rand[POSITION]), x_0[POSITION], space)
  if not hasObstacle(obstacles, x_closest[POSITION], x_rand[POSITION]):
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

def optimizePath(space, x_0, x_goal):
  x = x_goal
  while x[PARENT]:
    x_try = x[PARENT]
    best_parent_node = x_try
    best_cost = getNodeDistance(x_0, x_try)
    while x_try:
      obstacles = getObstaclesInRange(getVector(x[POSITION], x_try[POSITION]), x[POSITION], space)
      if not hasObstacle(obstacles, x[POSITION], x_try[POSITION]):
        current_cost = getNodeDistance(x_0, x_try)
        if current_cost < best_cost:
          best_parent_node = x_try
          best_cost = current_cost
      x_try = x_try[PARENT]

    x[PARENT] = best_parent_node
    x = best_parent_node

  return x_goal

def drawRoute(x_goal, color = [0, 255, 0]):
  x = x_goal
  while x[PARENT]:
    draw.drawLine(x[POSITION], x[PARENT][POSITION], color)
    x = x[PARENT]

def drawTree(grid, draw):
  for grid_element in grid.grid_elements:
    for node in grid_element.nodes:
      if node[PARENT]:
        draw.drawNarrowLine(node[POSITION], node[PARENT][POSITION])

draw = Draw()

#if hasObstacle([[15.0, 0]], [3.0, 1.0], [15.0, 0.5], 0.4):
#  raise Exception("Tangent failed")

C = [15.0, 3.0]
A = [3.0, 5.0]
B = [15.0, 3.5]
r = 1.0
#draw.drawCircle(C[X], C[Y], [0,0,0], r)
#draw.drawLine(A, B)
if not hasObstacle([C], A, B, r):
  raise Exception("1 Intersection failed")

C = [15.0, 3.0]
A = [3.0, 5.0]
B = [18.0, 3.5]
r = 1.0
#draw.drawCircle(C[X], C[Y], [0,0,0], r)
#draw.drawLine(A, B)
if not hasObstacle([C], A, B, r):
  raise Exception("2 Intersection failed")

C = [15.0, 3.0]
A = [14.6, 2.5]
B = [15.6, 2.5]
r = 1.0
#draw.drawCircle(C[X], C[Y], [0,0,0], r)
#draw.drawLine(A, B)
#if hasObstacle([C], A, B, r):
#  raise Exception("Interior failed")

C = [15.0, 3.0]
A = [2.0, 2.0]
B = [15.6, 2.00001]
r = 1.0
#draw.drawCircle(C[X], C[Y], [0,0,0], r)
#draw.drawLine(A, B)
if not hasObstacle([C], A, B, r):
  raise Exception("Tangent failed")

if hasObstacle([[2.0, 20.0]], [3.0, 1.0], [2.414938958075008, 19.628051833539704], 0.1):
  raise Exception("Error")
print("Succ")

#---------------------

space = generateSpace(XDIM, YDIM, draw)
printSpace(space)

draw.drawLine([5.0, 5.0], [6.0, 5.0], [0,0,1])

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

draw.drawCircle(START_POSITION[X], START_POSITION[Y], [0,1.0,1])
draw.drawCircle(END_POSITION[X], END_POSITION[Y], [0,1.0,0.9])


x = x_0
printNode(x)
while getNodeDistance(x, x_goal) >= 0.6:
#  x = algorithm2(space, x, x_goal, X_SI, [], [], 10.0, 10.0, draw)
   x = algorithm2(space, x, x_goal, X_SI, [], [], 10.0, 10.0, None)

print("Reached")

drawTree(X_SI, draw)
drawRoute(x)
x = optimizePath(space, x_0, x)
drawRoute(x, [0, 0, 0])
print(x)
