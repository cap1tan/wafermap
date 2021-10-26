import colorsys
import math
import os
import random
from typing import List, Tuple, Union

import numpy

# Color functions


def get_random_html_colormap_hsl(
    num_of_colors: int,
    hu: float = None,
    sa: float = None,
    lu: float = None,
    uniqueness_threshold: float = 0.1,
    hsl_out=False,
) -> Union[List[str], List[Tuple[float]]]:
    """
    Creates a list of colors in HTML format.
    :param num_of_colors: Numver of colors to create.
    :param hu: Hue value (0-1). If set, it will be propagated to all colors.
    :param sa: Saturation value (0-1). If set, it will be propagated to all colors.
    :param lu: Luminance value (0-1). If set, it will be propagated to all colors.
    :param uniqueness_threshold: Minimum distance between colormap colors.
    :param hsl_out: Return list of (h, s, l) tuples instead of HTML strings.
    :return: List of HTML colors.
    """

    ITERATION_LIMIT = num_of_colors * 100
    colors_hsl = []
    colors = []
    number_of_fixed_parameters = len(list(filter(None, [hu, sa, lu])))

    if number_of_fixed_parameters == 3:
        raise ValueError(
            "Cannot generate unique color map with all three H, S, L fixed."
        )

    for i in range(num_of_colors):
        _h = hu if hu else random.random()
        _s = sa if sa else random.random()
        _l = lu if lu else random.random()

        # check if generated random color is too close to previous values
        past_hsl_checked = 0
        iterations = 0
        while past_hsl_checked < len(colors_hsl) and iterations < ITERATION_LIMIT:
            past_hsl_color = colors_hsl[
                past_hsl_checked
            ]  # TODO: Check for all uniqueness in all past colors
            if (
                abs(sum(past_hsl_color) - _h - _s - _l)
                / (3 - number_of_fixed_parameters)
                < uniqueness_threshold
            ):
                # new color is too close to previously generated color. Re-generate new color
                _h = hu if hu else random.random()
                _s = sa if sa else random.random()
                _l = lu if lu else random.random()
                past_hsl_checked = 0  # re-check from scratch
            else:
                past_hsl_checked += 1
            iterations += 1  # safeguard against infinite loops

        colors_hsl.append((_h, _s, _l))
        colors.append(hsl_to_html(_h, _s, _l))
    if hsl_out:
        return colors_hsl
    else:
        return colors


def hsl_to_html(hu: float, sa: float, lu: float) -> str:
    """Convert given hsl color to an HTML code"""
    _rgb = colorsys.hls_to_rgb(hu, lu, sa)
    return "#%02X%02X%02X" % (
        round(255 * _rgb[0]),
        round(255 * _rgb[1]),
        round(255 * _rgb[2]),
    )


def rgb_to_html(r: float, g: float, b: float) -> str:
    """Convert given rgb color to an HTML code"""
    return "#%02X%02X%02X" % (r, g, b)


def complementary(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """returns RGB components of complementary color"""
    hsv = colorsys.rgb_to_hsv(r, g, b)
    return colorsys.hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])


# Utility functions


def euclidean_distance(
    point: Tuple[float, float], origin: Tuple[float, float] = None
) -> float:
    """Calculate euclidean distance from the origin"""
    if origin is None:
        return math.sqrt(sum((p ** 2 for p in point)))
    else:
        assert len(origin) == len(point)
        return math.sqrt(sum(((p - o) ** 2 for p, o in zip(point, origin))))


def append_to_filename(filename: str, suffix: str):
    splitext = os.path.splitext(filename)
    return splitext[0] + suffix + splitext[1]


def bounded_rectangle(
    rect: List[Tuple[float, float]], bounds: List[Tuple[float, float]]
) -> List[Tuple[float, float]]:
    """
    Resize rectangle given by points into a rectangle that fits within bounds, preserving the aspect ratio
    :param rect: Input rectangle [ll, ur], where each point is (y, x)
    :param bounds: Input bounding rectangle [ll, ur]
    :return: Bounded rectangle with same aspect ratio
    """
    assert len(rect) == len(bounds) == 2
    assert rect[0][0] <= rect[1][0] and rect[0][1] <= rect[1][1]
    assert bounds[0][0] <= bounds[1][0] and bounds[0][1] <= bounds[1][1]

    w_input = rect[1][1] - rect[0][1]
    h_input = rect[1][0] - rect[0][0]
    w_bound = bounds[1][1] - bounds[0][1]
    h_bound = bounds[1][0] - bounds[0][0]

    w = w_input
    h = h_input

    # find new rect points
    while w > w_bound or h > h_bound:

        if w > w_bound:
            # need to bound w
            a_w = w_bound / w
            w = w_bound
            h = h * a_w

        if h > h_bound:
            # need to bound w
            a_h = h_bound / h
            h = h_bound
            w = w * a_h

    rect_out = [rect[0], (rect[0][0] + h, rect[0][1] + w)]

    return rect_out


def rotate(
    points: List[Tuple[float, float]], anchor: Tuple[float, float], angle: float = 90.0
) -> List[Tuple[float, float]]:
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


def cart2pol(x: float, y: float) -> Tuple[float, float]:
    rho = numpy.sqrt(x ** 2 + y ** 2)
    phi = numpy.arctan2(y, x)
    return (rho, phi)


def pol2cart(rho: float, phi: float) -> Tuple[float, float]:
    x = rho * numpy.cos(phi)
    y = rho * numpy.sin(phi)
    return (x, y)


def round_to(num: float, tnum: float) -> float:
    """
    Rounds num to nearest tnum
    :param num: number to round (must be float/int)
    :param tnum: target number to round to (must be float/int)
    :return: rounded number
    """
    return round(num / tnum) * tnum


def floor_to(num: float, tnum: float) -> float:
    """
    Floors num to nearest tnum
    :param num: number to round (must be float/int)
    :param tnum: target number to round to (must be float/int)
    :return: rounded number
    """
    return math.floor(num / tnum) * tnum


def ceil_to(num: float, tnum: float) -> float:
    """
    Floors num to nearest tnum
    :param num: number to round (must be float/int)
    :param tnum: target number to round to (must be float/int)
    :return: rounded number
    """
    return math.ceil(num / tnum) * tnum


def trunc(x: Union[str, float], n: int) -> str:
    """Truncates x to n decimal points, regardless if x is a str or a number"""
    try:
        x_f = float(x)
        return ("%0." + str(n) + "f") % x_f
    except ValueError:
        # x not a number
        return x


################################################################################
