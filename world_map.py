from random import randint

import math_utils


class WorldMap:
    _EmptyMarker = 0
    _ObstacleMarker = 1
    _WallMarker = 2

    def __init__(self, reserved_positions, width, height):
        self._width = width
        self._height = height
        self._space = [[WorldMap._EmptyMarker] * width for _ in range(height)]

        for x in range(0, width):
            for y in range(0, height):
                cur_point = math_utils.Point(x, y)
                is_reserved_pos = any([pos for pos in reserved_positions if pos.equalInt(cur_point)])
                if self.isVerticalWall(cur_point) or self.isHorizontalWall(cur_point):
                    self._space[x][y] = WorldMap._WallMarker
                elif not is_reserved_pos and self.isRandomObstacle():
                    self._space[x][y] = WorldMap._ObstacleMarker


    def isVerticalWall(self, current_point):
        return current_point.x() == 0 or current_point.x() == self._width - 1

    def isHorizontalWall(self, current_point):
        return current_point.y() == 0 or current_point.y() == self._height - 1

    def isRandomObstacle(self):
        return randint(1, 6) == 2

    # This method is broken and just returns all obstacles
    def getObstaclesInRange(self, vector, origin, all=False):
        obstacles = []
        for x in range(0, self._width):
            for y in range(0, self._height):
                if self._space[x][y] != WorldMap._EmptyMarker:  # and (all or vectorNorm(getVector(origin, [x, y])) < vectorNorm(vector)):
                    obstacles.append(math_utils.Point(x, y))
        return obstacles

    def drawWorld(self, obstacle_callback, wall_callback):
        for x in range(0, self._width):
            for y in range(0, self._height):
                if self._space[x][y] == WorldMap._ObstacleMarker:
                    obstacle_callback(x, y)
                elif self._space[x][y] == WorldMap._WallMarker:
                    wall_callback(x, y)
