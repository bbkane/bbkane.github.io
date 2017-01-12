from collections import namedtuple
from enum import Enum
from statistics import mean

import matplotlib.pyplot as plt


class Orientation(Enum):
    left = 1
    right = 2


Point = namedtuple('Point', 'x y')


Rectangle = namedtuple('Rectangle', 'bl br tl tr')


def make_doodle_coords(orientation, rect, depth, coord_list=None):
    coord_list = coord_list or []
    if depth == 0:
        return coord_list
    mid_x = mean([rect.bl.x, rect.br.x])
    mid_y = mean([rect.bl.y, rect.tl.y])
    if orientation == Orientation.left:
        coord_list.append([rect.bl, rect.br, rect.tl])
        new_rect = Rectangle(bl=Point(mid_x, mid_y),
                             br=Point(rect.br.x, mid_y),
                             tl=Point(mid_x, rect.tl.y),
                             tr=rect.tr)
        return make_doodle_coords(Orientation.right, new_rect, depth - 1, coord_list)
    if orientation == Orientation.right:
        coord_list.append([rect.bl, rect.br, rect.tr])
        new_rect = Rectangle(bl=Point(rect.bl.x, mid_x),
                             br=Point(mid_x, mid_y),
                             tl=rect.tl,
                             tr=Point(mid_x, rect.tr.y))
        return make_doodle_coords(Orientation.left, new_rect, depth - 1, coord_list)


def plot_matplotlib(rect, doodle_triangles):
    for triangle in doodle_triangles:
        print(triangle)
        plt.gca().add_patch(plt.Polygon(triangle))

    # plt.axis('off')
    plt.axis('scaled')
    plt.axis('off')
    plt.show()


def plot_bokeh(rect, doodle_triangles):
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#patch-glyphs
    pass


def main():
    # plt.axes()
    rect = Rectangle(Point(0, 0), Point(100, 0), Point(0, 100), Point(100, 100))
    # TODO: matplotlib stops working when depth is > 4 and orientation is left
    # or orientation is > 3 and orientation is right
    # Is this matplotlib or my function?
    doodle_triangles = make_doodle_coords(Orientation.right, rect, depth=4)
    plot_matplotlib(rect, doodle_triangles)


if __name__ == "__main__":
    main()
