"""Utility functions"""

import base64
import math
from io import BytesIO

from PIL import Image

# Color functions


def rgb_to_html(red: float, green: float, blue: float) -> str:
    """Convert given rgb 0-1 color to an HTML code"""
    r, g, b = to255(red, green, blue)
    return "#%02X%02X%02X" % (r, g, b)


def invert(red: float, green: float, blue: float) -> tuple[float, float, float]:
    """returns RGB components of inverted color"""
    return 1.0 - red, 1.0 - green, 1.0 - blue


def to255(red: float, green: float, blue: float) -> tuple[int, int, int]:
    """returns RGB color to 0-255 scale"""
    return tuple(max(0, min(round(c * 255), 255)) for c in (red, green, blue))


def solid_color_png_url(rgb: tuple[int, int, int]) -> str:
    """Return a data URL of a 2x2 PNG filled with the given 0-255 RGB color"""
    buffered = BytesIO()
    Image.new("RGB", (2, 2), tuple(rgb)).save(buffered, "PNG")
    return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()


# Utility functions


def euclidean_distance(
    point: tuple[float, float], origin: tuple[float, float] = None
) -> float:
    """Calculate euclidean distance from the origin"""
    if origin is None:
        return math.sqrt(sum((p**2 for p in point)))
    assert len(origin) == len(point)
    return math.sqrt(sum(((p - o) ** 2 for p, o in zip(point, origin))))


def bounded_rectangle(
    rect: list[tuple[float, float]], bounds: list[tuple[float, float]]
) -> list[tuple[float, float]]:
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
    points: list[tuple[float, float]], anchor: tuple[float, float], angle: float = 90.0
) -> list[tuple[float, float]]:
    """Rotates points (nx2) about anchor (x, y) by angle in degrees, clockwise"""
    cos_a = math.cos(math.radians(angle))
    sin_a = math.sin(math.radians(angle))
    a_x, a_y = anchor
    return [
        (
            a_x + (x - a_x) * cos_a + (y - a_y) * sin_a,
            a_y - (x - a_x) * sin_a + (y - a_y) * cos_a,
        )
        for x, y in points
    ]


def arc(
    center: tuple[float, float],
    radius: float,
    start_angle: float,
    end_angle: float,
    step: float = 0.5,
) -> list[tuple[float, float]]:
    """Points (x, y) on a circular arc from start_angle to end_angle, in degrees counterclockwise from the +x axis, including both ends"""
    n = max(2, math.ceil(abs(end_angle - start_angle) / step) + 1)
    return [
        (
            center[0] + radius * math.cos(math.radians(angle)),
            center[1] + radius * math.sin(math.radians(angle)),
        )
        for angle in (
            start_angle + (end_angle - start_angle) * i / (n - 1) for i in range(n)
        )
    ]


def wafer_outline(
    radius: float,
    notch_orientation: float = 270.0,
    notch_depth: float = 1.0,
    notch_angle: float = 90.0,
    notch_bottom_radius: float = 0.9,
    arc_step: float = 0.5,
) -> list[tuple[float, float]]:
    """
    Closed outline (x, y) of a wafer centered at (0, 0), with a V-shaped notch with a
    rounded bottom. The notch is built at the top of the wafer and then rotated to
    notch_orientation.
    :param radius: Wafer radius
    :param notch_orientation: Notch position in degrees counterclockwise from the +x
    axis, e.g. 270 is at the bottom
    :param notch_depth: Distance from the wafer edge to the notch bottom
    :param notch_angle: Included angle between the notch sides in degrees
    :param notch_bottom_radius: Radius of the rounded notch bottom
    :param arc_step: Angular step in degrees used to draw the arcs
    """
    half_angle = math.radians(notch_angle / 2)
    sin_a, cos_a = math.sin(half_angle), math.cos(half_angle)

    # the rounded bottom is tangent to both notch sides
    bottom_center = (0.0, radius - notch_depth + notch_bottom_radius)
    # tangent point of the right notch side and the rounded bottom
    tangent_x = notch_bottom_radius * cos_a
    tangent_y = bottom_center[1] - notch_bottom_radius * sin_a
    # follow the right notch side, direction (sin_a, cos_a), up to the wafer edge
    along = tangent_x * sin_a + tangent_y * cos_a
    side_length = -along + math.sqrt(along**2 - tangent_x**2 - tangent_y**2 + radius**2)
    edge_angle = math.degrees(
        math.atan2(tangent_y + side_length * cos_a, tangent_x + side_length * sin_a)
    )
    notch_half_width = 90.0 - edge_angle  # angular half width of the notch opening

    # wafer edge counterclockwise from the left to the right notch side, then the
    # rounded notch bottom from right to left. The straight notch sides connect them.
    points = arc(
        (0.0, 0.0), radius, 90.0 + notch_half_width, 450.0 - notch_half_width, arc_step
    )
    points += arc(
        bottom_center,
        notch_bottom_radius,
        360.0 - math.degrees(half_angle),
        180.0 + math.degrees(half_angle),
        arc_step,
    )
    points.append(points[0])

    # rotate the notch from the top (90 degrees) to notch_orientation
    return rotate(points, (0.0, 0.0), angle=90.0 - notch_orientation)


def cart2pol(x: float, y: float) -> tuple[float, float]:
    """Convert cartesian coordinates x, y into polar rho, phi"""
    rho = math.hypot(x, y)
    phi = math.atan2(y, x)
    return rho, phi


def pol2cart(rho: float, phi: float) -> tuple[float, float]:
    """Convert polar coordinates rho, phi into cartesian x, y"""
    x = rho * math.cos(phi)
    y = rho * math.sin(phi)
    return x, y


def swap(x):
    """Swaps iterables of size 2, except strings and dicts, from (x, y) to (y, x), recursively"""
    if hasattr(x, "__iter__") and not (isinstance(x, str) or isinstance(x, dict)):
        if len(x) == 2:
            return type(x)((swap(x[1]), swap(x[0])))
        else:
            return type(x)(swap(x_i) for x_i in x)
    else:
        return x
