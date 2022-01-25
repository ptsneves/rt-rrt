import math

import cairo

import math_utils


class Draw:
    SCALE = 20.0
    narrow_line_width = 0.05
    line_width = 0.1
    BLACK = [0, 0, 0]
    _CENTER_OFFSET = 0.5

    def __init__(self, x_dimension, y_dimension):
        self.x_dimension = x_dimension
        self.y_dimension = y_dimension
        # We need to increase the whole surface dimension if we want to draw things like a legend
        self.surface = cairo.SVGSurface("output.svg", self.x_dimension * 2 * Draw.SCALE,
                                        self.y_dimension * 2 * Draw.SCALE)
        self.ctx = cairo.Context(self.surface)
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.set_line_width(self.line_width)
        self.ctx.scale(Draw.SCALE, Draw.SCALE)

    def line(self, p1, p2, color):
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(self.line_width)
        self.ctx.move_to(p1.x() + Draw._CENTER_OFFSET, p1.y() + Draw._CENTER_OFFSET)
        self.ctx.line_to(p2.x() + Draw._CENTER_OFFSET, p2.y() + Draw._CENTER_OFFSET)
        self.ctx.stroke()

    def narrowLine(self, p1, p2, color):
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(self.narrow_line_width)
        self.ctx.move_to(p1.x() + Draw._CENTER_OFFSET, p1.y() + Draw._CENTER_OFFSET)
        self.ctx.line_to(p2.x() + Draw._CENTER_OFFSET, p2.y() + Draw._CENTER_OFFSET)
        self.ctx.stroke()

    def node(self, node):
        self.circle(node.position().x() + Draw._CENTER_OFFSET/2.0,
                    node.position().y() + Draw._CENTER_OFFSET/2.0, [0.5, 0.5, 0.5], 0.2)

    def obstacle(self, x, y):
        self.circle(x, y, [1.0, 0, 0], Draw._CENTER_OFFSET)

    def start_end(self, x, y):
        self.circle(x, y, [0, 0, 40], Draw._CENTER_OFFSET)

    def circle(self, x, y, color, radius=1.0):
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.move_to(x + radius, y + radius)
        self.ctx.new_path()  # required to remove a centerline in the circle
        self.ctx.arc(x + radius, y + radius, radius, 0, 2 * math.pi)
        self.ctx.close_path()
        self.ctx.stroke()

    def legend(self):
        self.start_end(self.x_dimension + 1, 5)
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.set_font_size(1)
        self.ctx.move_to(self.x_dimension + 3, 5 + Draw._CENTER_OFFSET)
        self.ctx.show_text("edges - start and end")
        self.obstacle(self.x_dimension + 1, 7)
        self.ctx.move_to(self.x_dimension + 3, 7 + Draw._CENTER_OFFSET)
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.show_text("obstacles")
        self.walls(self.x_dimension + 1, 9)
        self.ctx.move_to(self.x_dimension + 3, 9 + Draw._CENTER_OFFSET)
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.show_text("walls")
        self.line(
            math_utils.Point(self.x_dimension + Draw._CENTER_OFFSET, 11),
            math_utils.Point(self.x_dimension + Draw._CENTER_OFFSET + 1, 11),
            [0, 255, 0])
        self.ctx.move_to(self.x_dimension + 3, 11 + Draw._CENTER_OFFSET)
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.show_text("unoptimized path rt-rrt from paper")
        self.line(
            math_utils.Point(self.x_dimension + Draw._CENTER_OFFSET, 13),
            math_utils.Point(self.x_dimension + Draw._CENTER_OFFSET + 1, 13),
            [0, 0, 0])
        self.ctx.move_to(self.x_dimension + 3, 13 + Draw._CENTER_OFFSET)
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.show_text("custom final cleanup path")
        self.circle(self.x_dimension + 1 + Draw._CENTER_OFFSET, 15 + Draw._CENTER_OFFSET, [0.5, 0.5, 0.5], 0.2)
        self.ctx.move_to(self.x_dimension + 3, 15 + Draw._CENTER_OFFSET)
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.show_text("intermediate node")
        self.ctx.stroke()

    def walls(self, x, y):
        self.ctx.set_source_rgb(255, 0, 0)
        self.ctx.rectangle(x, y, 1, 1)
        self.ctx.stroke()

    def route(self, x_goal, color=[0, 255, 0]):
        x = x_goal
        while x and x.parent():
            self.node(x)
            self.line(x.position(), x.parent().position(), color)
            x = x.parent()

    def tree(self, grid):
        for grid_element in grid.clusters:
            for node in grid_element.nodes:
                if node.parent():
                    self.narrowLine(node.position(), node.parent().position(), [0, 0, 0])
