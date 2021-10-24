#!/usr/bin/env python
# pylint: disable=redefined-outer-name

import random as rnd
import unittest

from wafermap import common, wafermap


class FunctionalTestsWafermap(unittest.TestCase):
    """Functional tests for the wafermap package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_wafermap_coverage_and_size(self):

        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=(13.702e-3, 24.846e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
            edge_exclusion=2.2e-3,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_full.html")

        wm = wafermap.WaferMap(
            wafer_radius=150e-3,
            cell_size=(13.702e-3, 24.846e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
            edge_exclusion=2.2e-3,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_full_150.html")

        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=(13.702e-3, 24.846e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
            edge_exclusion=2.2e-3,
            coverage="inner",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_inner.html")

        wm = wafermap.WaferMap(
            wafer_radius=150e-3,
            cell_size=(13.702e-3, 24.846e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
            edge_exclusion=2.2e-3,
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
            conversion_factor=1e-3,
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
            conversion_factor=1e-3,
        )
        wm.save_html(".\\tests\\test_wafermap_150_sipp27.html")

    def test_wafermap_notch(self):

        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=(13.702e-3, 24.846e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
            edge_exclusion=2.2e-3,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_notch_270.html")

        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=(13.702e-3, 24.846e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
            edge_exclusion=2.2e-3,
            coverage="full",
            notch_orientation=180,
        )
        wm.save_html(".\\tests\\test_wafermap_notch_180.html")

        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=(13.702e-3, 24.846e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
            edge_exclusion=2.2e-3,
            coverage="full",
            notch_orientation=67,
        )
        wm.save_html(".\\tests\\test_wafermap_notch_67.html")

    def test_wafermap_grid(self):

        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=(10e-3, 20e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
            edge_exclusion=2.2e-3,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_10_20.html")

        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=(1e-3, 10e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
            edge_exclusion=2.2e-3,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_1_10.html")

        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=(50e-3, 10e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
            edge_exclusion=2.2e-3,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_50_10.html")

    def test_wafermap_cell_margin(self):

        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=(13.702e-3, 24.846e-3),
            cell_margin=(8e-3, 15e-3),
            grid_offset=(-2.05e-3, -4.1e-3),
            edge_exclusion=2.2e-3,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_margin_8_15.html")

    def test_wafermap_edge_exclusion(self):

        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=(13.702e-3, 24.846e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
            edge_exclusion=10e-3,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(".\\tests\\test_wafermap_ee_10.html")

    def test_wafermap_png(self):

        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=(13.702e-3, 24.846e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
            coverage="full",
            notch_orientation=270,
        )
        _ = wm.save_png(".\\tests\\test_wafermap.png")

    def test_wafermap_add_image1(self):

        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=(13.702e-3, 24.846e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
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
            offset=(2.0e-3, 2.0e-3),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_17_147378.jpg",
            cell=(3, 0),
            offset=(0.5e-3, 0.5e-3),
            marker_style={},
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_2_125416.jpg",
            cell=(0, -2),
            offset=(12.0e-3, 5.0e-3),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_17_147378.jpg",
            cell=(0, -2),
            offset=(28.0e-3, 3e-3),
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
            wafer_radius=150e-3,
            cell_size=(13.702e-3, 24.846e-3),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05e-3, -4.1e-3),
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
            offset=(2.0e-3, 2.0e-3),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_17_147378.jpg",
            cell=(3, 0),
            offset=(0.5e-3, 0.5e-3),
            marker_style={},
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_2_125416.jpg",
            cell=(0, -2),
            offset=(12.0e-3, 5.0e-3),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_17_147378.jpg",
            cell=(0, -2),
            offset=(28.0e-3, 3e-3),
        )
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_2_125416.jpg",
            cell=(0, 1),
            offset=(0.0, 0.0),
            marker_style={},
        )
        wm.save_html(".\\tests\\test_wafermap_image2.html")

    def test_wafermap_add_vectors1(self):

        cell_size = (26e-3, 14e-3)
        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=cell_size,
            cell_margin=(0.0, 0.0),
            grid_offset=(0e-3, 0e-3),
            coverage="full",
            notch_orientation=270,
        )

        vectors = [
            ((3, 0), [(0, 0), (1e-3, 1e-3)]),
            ((3, 0), [(1e-3, 0), (-5e-3, 5e-3)]),
            ((3, 0), [(0, 1e-3), (10e-3, -10e-3)]),
            ((3, 0), [(1e-3, 1e-3), (-20e-3, -20e-3)]),
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

        cell_size = (26e-3, 14e-3)
        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=cell_size,
            cell_margin=(0.0, 0.0),
            grid_offset=(0e-3, 0e-3),
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
            for cell in wm.cell_map.keys()
        ]
        for cell, vector in vectors:
            wm.add_vector(
                vector_points=vector,
                cell=cell,
                root_style={"radius": 1, "color": "black"},
            )

        wm.save_html(".\\tests\\test_wafermap_vectors2.html")

    def test_wafermap_add_points1(self):

        cell_size = (26e-3, 14e-3)
        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=cell_size,
            cell_margin=(0.0, 0.0),
            grid_offset=(0e-3, 0e-3),
            coverage="full",
            notch_orientation=270,
        )

        wafer_points = [
            common.pol2cart(rnd.gauss(0, 100e-3 / 3), rnd.gauss(0, 360))
            for _ in range(1000)
        ]
        for wafer_point in wafer_points:
            wm.add_point(cell=None, offset=wafer_point)

        wm.save_html(".\\tests\\test_wafermap_points1.html")

    def test_wafermap_add_points2(self):

        cell_size = (26e-3, 14e-3)
        wm = wafermap.WaferMap(
            wafer_radius=100e-3,
            cell_size=cell_size,
            cell_margin=(0.0, 0.0),
            grid_offset=(0e-3, 0e-3),
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
            for cell in wm.cell_map.keys()
        ]
        for cell, cell_points_ in cell_points:
            for cell_point in cell_points_:
                wm.add_point(cell=cell, offset=cell_point)

        wm.save_html(".\\tests\\test_wafermap_points2.html")

    def test_example_wafermap(self):

        # define the wafermap
        wm = wafermap.WaferMap(
            wafer_radius=100e-3,  # all length dimensions in meters
            cell_size=(10e-3, 20e-3),  # (sizeX, sizeY)
            cell_margin=(2.5e-3, 4e-3),  # distance between cell borders (x, y)
            grid_offset=(-2.05e-3, -4.1e-3),  # grid offset in (x, y)
            edge_exclusion=3.2e-3,
            # margin from the wafer edge where a red edge exclusion ring is drawn
            coverage="full",  # 'full': will cover wafer with cells, partial cells allowed
            # 'inner': only full cells allowed
            notch_orientation=270,
        )  # angle of notch in degrees. 270 corresponds to a notch at the bottom

        # add an image
        wm.add_image(
            image_source_file=".\\tests\\INS3300_Lot_1_Wafer_17_147378.jpg",
            cell=(1, 0),  # (cell_index_x, cell_index_y)
            offset=(2.0e-3, 2.0e-3),
        )  # relative coordinate of the image within the cell

        # add vectors
        vectors = [
            ((3, 0), [(0, 0), (1e-3, 1e-3)]),
            ((3, 0), [(1e-3, 0), (-5e-3, 5e-3)]),
            ((3, 0), [(0, 1e-3), (10e-3, -10e-3)]),
            ((3, 0), [(1e-3, 1e-3), (-20e-3, -20e-3)]),
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
        cell_size = (10e-3, 20e-3)
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
            for cell in wm.cell_map.keys()
        ]
        for cell, cell_points_ in cell_points:
            for cell_point in cell_points_:
                wm.add_point(cell=cell, offset=cell_point)

        # save to html
        wm.save_html(".\\tests\\test_wafermap_example.html")

        # save to png (Mozilla must be installed)
        wm.save_png(".\\tests\\test_wafermap_example.png")
