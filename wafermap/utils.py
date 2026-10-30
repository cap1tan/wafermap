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
