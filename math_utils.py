import math
import random

X = 0
Y = 1


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def x(self):
        return self._x

    def y(self):
        return self._y

    def equalInt(self, p2):
        return self.x() == p2.x() and self.y() == p2.y()

    def vectorTo(self, point2):
        dx = point2.x() - self.x()
        dy = point2.y() - self.y()
        return Vector(dx, dy)

    def projectedPoint(self, v):
        return Point(self.x() + v.x(), self.y() + v.y())

class Vector:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def x(self):
        return self._x

    def y(self):
        return self._y

    def scalarProduct(self, a):
        return Vector(a * self.x(), a * self.y())

    def norm(self):
        return math.sqrt(self.squaredLength())

    def squaredLength(self):
        return self.x() ** 2 + self.y() ** 2


def solveQuadratic(c, b, a):
    disc = b ** 2.0 - 4.0 * a * c
    if disc < 0.0:
        # print("Disc: " + str(disc))
        return None
    disc = math.sqrt(disc)
    x1 = None
    x2 = None
    if b >= 0.0:
        if a >= 0.00000001:
            x1 = (-b - disc) / (2.0 * a)
        x2 = (2.0 * c) / (-b - disc)
    else:
        x1 = (2.0 * c) / (-b + disc)
        if a >= 0.00000001:
            x2 = (-b + disc) / (2.0 * a)
    return [x1, x2]


def getUniform(start, end):
    return random.uniform(0, 20)


def getLineTo(a, b):
    return a.getVector(b)
