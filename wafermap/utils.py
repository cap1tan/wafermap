"""Utility functions"""

import colorsys
import math

import numpy

# Color functions


def rgb_to_html(red: float, green: float, blue: float) -> str:
    """Convert given rgb color to an HTML code"""
    return "#%02X%02X%02X" % (red, green, blue)


def complementary(red: int, green: int, blue: int) -> (int, int, int):
    """returns RGB components of complementary color"""
    hsv = colorsys.rgb_to_hsv(red, green, blue)
    return colorsys.hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])


# Utility functions


def euclidean_distance(point: (float, float), origin: (float, float) = None) -> float:
    """Calculate euclidean distance from the origin"""
    if origin is None:
        return math.sqrt(sum((p**2 for p in point)))
    assert len(origin) == len(point)
    return math.sqrt(sum(((p - o) ** 2 for p, o in zip(point, origin))))


def bounded_rectangle(
    rect: [(float, float)], bounds: [(float, float)]
) -> [(float, float)]:
    """
    Resize rectangle given by points into a rectangle that fits within bounds,
    preserving the aspect ratio.
    :param rect: Input rectangle [ll, ur], where each point is (y, x)
    :param bounds: Input bounding rectangle [ll, ur]
    :return: Bounded rectangle with same aspect ratio
    """
    assert len(rect) == len(bounds) == 2
    assert rect[0][0] <= rect[1][0] and rect[0][1] <= rect[1][1]
    assert bounds[0][0] <= bounds[1][0] and bounds[0][1] <= bounds[1][1]

    width_input = rect[1][1] - rect[0][1]
    height_input = rect[1][0] - rect[0][0]
    width_bound = bounds[1][1] - bounds[0][1]
    height_bound = bounds[1][0] - bounds[0][0]

    width = width_input
    height = height_input

    # find new rect points
    while width > width_bound or height > height_bound:
        if width > width_bound:
            # need to bound w
            a_w = width_bound / width
            width = width_bound
            height = height * a_w

        if height > height_bound:
            # need to bound w
            a_h = height_bound / height
            height = height_bound
            width = width * a_h

    rect_out = [rect[0], (rect[0][0] + height, rect[0][1] + width)]

    return rect_out


def rotate(
    points: [(float, float)], anchor: (float, float), angle: float = 90.0
) -> [(float, float)]:
    """Rotates points (nx2) about anchor (x, y) by angle in degrees"""
    points = numpy.array(points)
    anchor = numpy.array(anchor)
    angle = math.radians(-angle)
    return (
        numpy.dot(
            points - anchor,
            [[math.cos(angle), math.sin(angle)], [-math.sin(angle), math.cos(angle)]],
        )
        + anchor
    )


def cart2pol(x: float, y: float) -> (float, float):
    """Convert cartesian coordinates x, y into polar rho, phi"""
    rho = numpy.sqrt(x**2 + y**2)
    phi = numpy.arctan2(y, x)
    return rho, phi


def pol2cart(rho: float, phi: float) -> (float, float):
    """Convert polar coordinates rho, phi into cartesian x, y"""
    x = rho * numpy.cos(phi)
    y = rho * numpy.sin(phi)
    return x, y
