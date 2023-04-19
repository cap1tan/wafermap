"""Automated testing functions"""

# pylint: disable=redefined-outer-name, missing-function-docstring, invalid-name

import random as rnd
import unittest

from wafermap import utils, wafermap


class FunctionalTestsWafermap(unittest.TestCase):
    """Functional tests for the wafermap package."""

    def test_wafermap_coverage_and_size(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_full.html")

        wm = wafermap.WaferMap(
            wafer_radius=150,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_full_150.html")

        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="inner",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_inner.html")

        wm = wafermap.WaferMap(
            wafer_radius=150,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="inner",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_inner_150.html")

        wm = wafermap.WaferMap(
            wafer_radius=150,
            cell_size=(23.24, 31.4),
            cell_margin=(0.0, 0.0),
            grid_offset=(9.854, 2.512),
            edge_exclusion=0.0,
            coverage="inner",
            notch_orientation=270,
            conversion_factor=1,
        )
        wm.save_html(".\\tests\\test_wafermap_inner_150_with_conversion.html")

        wm = wafermap.WaferMap(
            wafer_radius=150,
            cell_size=(25.87, 15.31),
            cell_margin=(0.0, 0.0),
            grid_offset=(0.0, 0.0),
            edge_exclusion=0.0,
            coverage="full",
            notch_orientation=270,
            conversion_factor=1,
        )
        wm.save_html(".\\tests\\test_wafermap_150_sipp27.html")

    def test_wafermap_notch(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_notch_270.html")

        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=180,
        )
        wm.save_html(".\\tests\\test_wafermap_notch_180.html")

        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=67,
        )
        wm.save_html(".\\tests\\test_wafermap_notch_67.html")

    def test_wafermap_grid(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(10, 20),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_10_20.html")

        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(1, 10),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_1_10.html")

        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(50, 10),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_50_10.html")

    def test_wafermap_cell_margin(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(8, 15),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_margin_8_15.html")

    def test_wafermap_edge_exclusion(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=10,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_ee_10.html")

    def test_wafermap_png(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            coverage="full",
            notch_orientation=270,
        )
        _ = wm.save_png(".\\tests\\test_wafermap.png")

    def test_wafermap_add_image1(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            coverage="full",
            notch_orientation=270,
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_17_147375.jpg",
            cell=(0, 0),
            offset=(0.0, 0.0),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_2_125416.jpg",
            cell=(1, 0),
            offset=(2.0, 2.0),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_17_147378.jpg",
            cell=(3, 0),
            offset=(0.5, 0.5),
            marker_style={},
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_2_125416.jpg",
            cell=(0, -2),
            offset=(12.0, 5.0),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_17_147378.jpg",
            cell=(0, -2),
            offset=(28.0, 3),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_2_125416.jpg",
            cell=(0, 1),
            offset=(0.0, 0.0),
            marker_style={},
        )
        wm.save_html(".\\tests\\test_wafermap_image1.html")

    def test_wafermap_add_image2(self):
        wm = wafermap.WaferMap(
            wafer_radius=150,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            coverage="full",
            notch_orientation=270,
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_17_147375.jpg",
            cell=(0, 0),
            offset=(0.0, 0.0),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_2_125416.jpg",
            cell=(1, 0),
            offset=(2.0, 2.0),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_17_147378.jpg",
            cell=(3, 0),
            offset=(0.5, 0.5),
            marker_style={},
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_2_125416.jpg",
            cell=(0, -2),
            offset=(5, 12),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_17_147378.jpg",
            cell=(0, -2),
            offset=(3, 28),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_2_125416.jpg",
            cell=(0, 1),
            offset=(0.0, 0.0),
            marker_style={},
        )
        wm.save_html(".\\tests\\test_wafermap_image2.html")

    def test_wafermap_add_vectors1(self):
        cell_size = (26, 14)
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=cell_size,
            cell_margin=(0.0, 0.0),
            grid_offset=(0, 0),
            coverage="full",
            notch_orientation=270,
        )

        vectors = [
            ((3, 0), [(0, 0), (1, 1)]),
            ((3, 0), [(1, 0), (-5, 5)]),
            ((3, 0), [(0, 1), (10, -10)]),
            ((3, 0), [(1, 1), (-20, -20)]),
        ]
        colors = ["green", "red", "blue", "black"]
        for color, (_, vector) in zip(colors, vectors):
            wm.add_vector(
                vector_points=vector, cell=None, vector_style={"color": color}
            )
        for color, (cell, vector) in zip(colors, vectors):
            wm.add_vector(
                vector_points=vector,
                cell=cell,
                vector_style={"color": color},
                root_style={"radius": 1, "color": color},
            )

        wm.save_html(".\\tests\\test_wafermap_vectors1.html")

    def test_wafermap_add_vectors2(self):
        cell_size = (26, 14)
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=cell_size,
            cell_margin=(0.0, 0.0),
            grid_offset=(0, 0),
            coverage="full",
            notch_orientation=270,
        )

        vectors = [
            (
                cell,
                [
                    (cell_size[1] / 2, cell_size[0] / 2),
                    (rnd.uniform(0, cell_size[1]), rnd.uniform(0, cell_size[0])),
                ],
            )
            for cell in wm.cell_map
        ]
        for cell, vector in vectors:
            wm.add_vector(
                vector_points=vector,
                cell=cell,
                root_style={"radius": 1, "color": "black"},
            )

        wm.save_html(".\\tests\\test_wafermap_vectors2.html")

    def test_wafermap_add_points1(self):
        cell_size = (26, 14)
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=cell_size,
            cell_margin=(0.0, 0.0),
            grid_offset=(0, 0),
            coverage="full",
            notch_orientation=270,
        )

        wafer_points = [
            utils.pol2cart(rnd.gauss(0, 100 / 3), rnd.gauss(0, 360))
            for _ in range(1000)
        ]
        for wafer_point in wafer_points:
            wm.add_point(cell=None, offset=wafer_point)

        wm.save_html(".\\tests\\test_wafermap_points1.html")

    def test_wafermap_add_points2(self):
        cell_size = (26, 14)
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=cell_size,
            cell_margin=(0.0, 0.0),
            grid_offset=(0, 0),
            coverage="full",
            notch_orientation=270,
        )

        cell_points = [
            (
                cell,
                [
                    (
                        rnd.gauss(cell_size[1] / 2, cell_size[1] / 6),
                        rnd.gauss(cell_size[0] / 2, cell_size[0] / 6),
                    )
                    for _ in range(50)
                ],
            )
            for cell in wm.cell_map
        ]
        for cell, cell_points_ in cell_points:
            for cell_point in cell_points_:
                wm.add_point(cell=cell, offset=cell_point)

        wm.save_html(".\\tests\\test_wafermap_points2.html")

    def test_wafermap_add_labels1(self):
        cell_size = (26, 14)
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=cell_size,
            cell_margin=(0.0, 0.0),
            grid_offset=(0, 0),
            coverage="full",
            notch_orientation=270,
        )

        for cell in wm.cell_map:
            if sum(cell) % 2 == 0:
                wm.add_label(
                    cell=cell,
                    offset=(cell_size[1] / 2, cell_size[0] / 2),
                    label_text=f"Label: {cell}",
                )
            else:
                wm.add_label(
                    cell=cell,
                    offset=(cell_size[1] / 2, cell_size[0] / 2),
                    label_text=f"This is a longer label: {cell}",
                )

        wm.save_html(".\\tests\\test_wafermap_labels1.html")

    def test_wafermap_style_cells1(self):
        cell_size = (26, 14)
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=cell_size,
            cell_margin=(0.0, 0.0),
            grid_offset=(0, 0),
            coverage="full",
            notch_orientation=270,
        )

        named_html_colors = [
            "AliceBlue",
            "red",
            "green",
            "blue",
            "yellow",
            "Aquamarine",
            "Bisque",
            "Brown",
            "BlueViolet",
            "Gold",
            "Grey",
            "Magenta",
            "MidnightBlue",
            "MintCream",
            "Orange",
            "Purple",
            "Salmon",
        ]
        for cell in wm.cell_map:
            random_cell_style = {
                "fill": rnd.random() > 0.5,
                "fillColor": named_html_colors[
                    rnd.randint(0, len(named_html_colors) - 1)
                ],
                "fillOpacity": rnd.random(),
            }
            wm.style_cell(cell=cell, cell_style=random_cell_style)

        wm.save_html(".\\tests\\test_wafermap_style_cells1.html")

    def test_example_wafermap(self):
        # define the wafermap
        wm = wafermap.WaferMap(
            wafer_radius=100,  # all length dimensions in meters
            cell_size=(10, 20),  # (sizeX, sizeY)
            cell_margin=(2.5, 4),  # distance between cell borders (x, y)
            grid_offset=(-2.05, -4.1),  # grid offset in (x, y)
            edge_exclusion=3.2,
            # margin from the wafer edge where a red edge exclusion ring is drawn
            coverage="full",  # partial cells allowed
            # 'inner': only full cells allowed
            notch_orientation=270,
        )  # angle of notch in degrees. 270 corresponds to a notch at the bottom

        # add an image
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_17_147378.jpg",
            cell=(0, 1),
            offset=(2.0, 5.0),
        )  # relative coordinate of the image within the cell

        # add vectors
        vectors = [
            ((3, 0), [(0, 0), (1, 1)]),
            ((3, 0), [(1, 0), (-5, 5)]),
            ((3, 0), [(0, 1), (10, -10)]),
            ((3, 0), [(1, 1), (-20, -20)]),
        ]
        colors = ["green", "red", "blue", "black"]
        for color, (cell, vector) in zip(colors, vectors):
            wm.add_vector(
                vector_points=vector,
                cell=cell,
                vector_style={"color": color},
                root_style={"radius": 1, "color": color},
            )

        # add 50 points per cell, in a random distribution
        cell_size = (10, 20)
        cell_points = [
            (
                cell,
                [
                    (
                        rnd.gauss(cell_size[1] / 2, cell_size[1] / 6),
                        rnd.gauss(cell_size[0] / 2, cell_size[0] / 6),
                    )
                    for _ in range(50)
                ],
            )
            for cell in wm.cell_map
        ]
        for cell, cell_points_ in cell_points:
            for i, cell_point in enumerate(cell_points_):
                wm.add_point(
                    cell=cell, offset=cell_point, popup_text=f"Cell marker {i}"
                )

        # randomly add a label in cells
        named_html_colors = [
            "AliceBlue",
            "red",
            "green",
            "blue",
            "yellow",
            "Aquamarine",
            "Bisque",
            "Brown",
            "BlueViolet",
            "Gold",
            "Grey",
            "Magenta",
            "MidnightBlue",
            "MintCream",
            "Orange",
            "Purple",
            "Salmon",
        ]
        for i, cell_idx in enumerate(wm.cell_map):
            if i > rnd.randint(0, len(wm.cell_map)) / 1.5:
                # randomly print a random label
                picked_fg_color = named_html_colors[
                    rnd.randint(0, len(named_html_colors) - 1)
                ]
                random_label_style = (
                    f"font-size: {rnd.randint(1, 16)}pt; "
                    f"color: {picked_fg_color}; "
                    f"text-align: center;"
                    f" background-color:"
                    f"{named_html_colors[rnd.randint(0, len(named_html_colors) - 1)]};"
                )
                wm.add_label(
                    cell=cell_idx,
                    offset=(cell_size[1] / 2, cell_size[0] / 2),
                    label_text=picked_fg_color,
                    label_html_style=random_label_style,
                )

        # save to html
        wm.save_html(".\\tests\\test_wafermap_example.html")

        # save to png (Mozilla must be installed)
        wm.save_png(".\\tests\\test_wafermap_example.png")
