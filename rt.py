#!/usr/bin/python3

import random
import math

X = 0
Y = 1

def isPointInSegment(pv1, pv2, point):
  return isColinear(pv1, pv2, point) and isPointContainedInRange(pv1, point, pv2)

def isPointContainedInRange(p1, p2, p3):
  return p1 != p3 and (p1 <= p2 <= p3 or p3 <= p2 <= p1)

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
def getObstacle(current_position, move_vector, obstacle_radius = 1.0):
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

if getVectorProjection([3.0, -8.0], [1.0, 2.0]) != [-2.6, -5.2]:
  raise Exception("Error")

if not isColinear([1,1], [2,2], [3,3]):
  raise Exception("Error")

if isColinear([1,0.9], [2,2], [3,3]):
  raise Exception("Error")

if isPointInSegment([1.0, 1.0], [1.0, 1.0], [2.0, 2.0]):
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

