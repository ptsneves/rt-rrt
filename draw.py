import math

import cairo


class Draw:
    SCALE = 20.0
    narrow_line_width = 0.05
    line_width = 0.1
    BLACK = [0, 0, 0]

    def __init__(self, x_dimension, y_dimension):
        self.x_dimension = x_dimension
        self.y_dimension = y_dimension
        self.surface = cairo.SVGSurface("output.svg", self.x_dimension * Draw.SCALE, self.y_dimension * Draw.SCALE)
        self.ctx = cairo.Context(self.surface)
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.set_line_width(self.line_width)
        self.ctx.scale(Draw.SCALE, Draw.SCALE)

    def line(self, p1, p2, color):
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(self.line_width)
        self.ctx.move_to(p1.x(), p1.y())
        self.ctx.line_to(p2.x(), p2.y())
        self.ctx.stroke()

    def narrowLine(self, p1, p2, color):
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(self.narrow_line_width)
        self.ctx.move_to(p1.x(), p1.y())
        self.ctx.line_to(p2.x(), p2.y())
        self.ctx.stroke()

    def nodes(self, node1, node2):
        self.circle(node1.position().x(), node1.position().y(), [0, 1.0, 0], 0.1)
        self.line(node1.position(), node2.position(), Draw.BLACK)

    def obstacle(self, x, y):
        self.ctx.set_source_rgb(1.0, 0, 0)
        self.ctx.move_to(x, y)
        self.ctx.arc(x, y, 0.6, -math.pi, math.pi)
        self.ctx.stroke()

    def circle(self, x, y, color, radius=1.0):
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.move_to(x, y)
        self.ctx.arc(x, y, radius, -math.pi, math.pi)
        self.ctx.stroke()

    def walls(self, x, y):
        self.ctx.set_source_rgb(255, 0, 0)
        self.ctx.rectangle(x, y, 1, 1)
        self.ctx.stroke()

    def route(self, x_goal, color=[0, 255, 0]):
        x = x_goal
        while x and x.parent():
            self.line(x.position(), x.parent().position(), color)
            x = x.parent()

    def tree(self, grid):
        for grid_element in grid.clusters:
            for node in grid_element.nodes:
                if node.parent():
                    self.narrowLine(node.position(), node.parent().position(), [0, 0, 0])
