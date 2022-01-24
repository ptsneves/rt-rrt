import math_utils


class Node:
    def __init__(self, position, cost, parent):
        self._position = position
        self._cost = cost
        self._parent = parent

    def cost(self):
        return self._cost

    def setCost(self, c):
        self._cost = c

    def costTo(self, destination):
        return self.cost() + self.distance(destination)

    def parent(self):
        return self._parent

    def setParent(self, n):
        self._parent = n

    def position(self):
        return self._position

    def distance(self, other):
        return self.vector(other).norm()

    def vector(self, to):
        return self.position().vectorTo(to.position())

    class ClosestResult:
        def __init__(self, closest, distance):
            self._closest = closest
            self._distance = distance

        def closest(self):
            return self._closest

        def distance(self):
            return self._distance

    def closest(self, node_list):
        smallest_distance = self.distance(node_list[0])
        closest_node = node_list[0]

        if len(node_list) > 1:
            for node in node_list[1:]:
                distance = self.distance(node)
                if distance < smallest_distance:
                    closest_node = node
                    smallest_distance = distance

        return Node.ClosestResult(closest_node, smallest_distance)

    def print(self):
        if self.parent():
            print("POSITION {}\nNodeGrid.COST{}\nNodeGrid.PARENT_POS {}\n".format(
                self.position(),
                self.cost(),
                self.parent().position()
            ))
        else:
            print("ROOT: POSITION {}\nNodeGrid.COST{}\n".format(self.position(), self.cost()))
