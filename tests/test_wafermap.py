"""Automated testing functions"""

import math
import os.path
import random as rnd
import unittest

import folium

from wafermap import utils, wafermap

# pylint: disable=redefined-outer-name, missing-function-docstring, invalid-name


TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


class FunctionalTestsWafermap(unittest.TestCase):
    """Functional tests for the wafermap package."""

    @classmethod
    def setUpClass(cls):
        cls.output_dir = os.path.join(TESTS_DIR, "tests_output")
        cls.input_dir = TESTS_DIR
        os.makedirs(cls.output_dir, exist_ok=True)

        # delete contents of output dir
        for f in os.listdir(cls.output_dir):
            file_path = os.path.join(cls.output_dir, f)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

    def test_wafermap_invalid(self):

        raised = False
        try:
            _ = wafermap.WaferMap(
                wafer_radius=-100,
                cell_size=(13.702, 24.846),
                cell_margin=(0.0, 0.0),
                grid_offset=(-2.05, -4.1),
                edge_exclusion=2.2,
                coverage="full",
                notch_orientation=270,
            )
        except ValueError:
            raised = True
        if not raised:
            raise ValueError("Test failed")

        try:
            _ = wafermap.WaferMap(
                wafer_radius=100,
                cell_size=(0, 24.846),
                cell_margin=(0.0, 0.0),
                grid_offset=(-2.05, -4.1),
                edge_exclusion=2.2,
                coverage="full",
                notch_orientation=180,
            )
        except ValueError:
            raised = True
        if not raised:
            raise ValueError("Test failed")

        try:
            _ = wafermap.WaferMap(
                wafer_radius=100,
                cell_size=(13.702, 24.846),
                cell_margin=(0.0, -1),
                grid_offset=(-2.05, -4.1),
                edge_exclusion=2.2,
                coverage="full",
                notch_orientation=67,
            )
        except ValueError:
            raised = True
        if not raised:
            raise ValueError("Test failed")

        try:
            _ = wafermap.WaferMap(
                wafer_radius=100,
                cell_size=(13.702, 24.846),
                cell_margin=(0.0, 0.0),
                grid_offset=(-2.05, -4.1),
                edge_exclusion=-0.1,
                coverage="full",
                notch_orientation=67,
            )
        except ValueError:
            raised = True
        if not raised:
            raise ValueError("Test failed")

        try:
            _ = wafermap.WaferMap(
                wafer_radius=100,
                cell_size=(13.702, 24.846),
                cell_margin=(0.0, 0.0),
                grid_offset=(-2.05, -4.1),
                edge_exclusion=1,
                coverage="test",
                notch_orientation=67,
            )
        except ValueError:
            raised = True
        if not raised:
            raise ValueError("Test failed")

    def test_wafermap_swap(self):

        swap = utils.swap

        test1 = (3, 4)
        assert swap(test1) == (4, 3)
        test2 = (3, 3)
        assert swap(test2) == (3, 3)
        test3 = [3, 4]
        assert swap(test3) == [4, 3]
        test5 = [(1, 2), (3, 4), (0, 0)]
        assert swap(test5) == [(2, 1), (4, 3), (0, 0)]
        test6 = ["ab", (1, 2), "c", 42, [1, 2, 3], (0, -1)]
        assert swap(test6) == ["ab", (2, 1), "c", 42, [1, 2, 3], (-1, 0)]
        test7 = ((1, 2), (3, 4), (5, 6), (7, 8), (9, 10), {"a": 1, "b": 2})
        assert swap(test7) == (
            (2, 1),
            (4, 3),
            (6, 5),
            (8, 7),
            (10, 9),
            {"a": 1, "b": 2},
        )
        test8 = [(1, 2), (3, 4)]
        assert swap(test8) == [(4, 3), (2, 1)]

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
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_full.html"))
        assert os.path.isfile(os.path.join(self.output_dir, "test_wafermap_full.html"))
        wm = wafermap.WaferMap(
            wafer_radius=150,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_full_150.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_full_150.html")
        )
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="inner",
            notch_orientation=270,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_inner.html"))
        assert os.path.isfile(os.path.join(self.output_dir, "test_wafermap_inner.html"))
        wm = wafermap.WaferMap(
            wafer_radius=150,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="inner",
            notch_orientation=270,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_inner_150.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_inner_150.html")
        )
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
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_150_sipp27.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_150_sipp27.html")
        )
        wm = wafermap.WaferMap(
            wafer_radius=150,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="none",
            notch_orientation=270,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_none_150.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_none_150.html")
        )

    def test_wafermap_conversion_factor(self):

        wm = wafermap.WaferMap(
            wafer_radius=150,
            cell_size=(23.24, 31.4),
            cell_margin=(0.0, 0.0),
            grid_offset=(9.854, 2.512),
            edge_exclusion=0.0,
            coverage="inner",
            notch_orientation=270,
            conversion_factor=1e-2,
        )
        wm.save_html(
            os.path.join(self.output_dir, "test_wafermap_conversion_1e-2.html")
        )
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_conversion_1e-2.html")
        )

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
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_notch_270.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_notch_270.html")
        )
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=180,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_notch_180.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_notch_180.html")
        )
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=67,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_notch_67.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_notch_67.html")
        )

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
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_10_20.html"))
        assert os.path.isfile(os.path.join(self.output_dir, "test_wafermap_10_20.html"))
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(1, 10),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_1_10.html"))
        assert os.path.isfile(os.path.join(self.output_dir, "test_wafermap_1_10.html"))
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(2, 6),
            cell_margin=(0.0, 0.0),
            grid_offset=(40, 0),
            edge_exclusion=0,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_2_6.html"))
        assert os.path.isfile(os.path.join(self.output_dir, "test_wafermap_2_6.html"))
        wm = wafermap.WaferMap(
            wafer_radius=150,
            cell_size=(25.96, 15.504),
            cell_margin=(0.0, 0.0),
            grid_offset=(0, 0),
            edge_exclusion=0,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_26_15.5_ee0.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_26_15.5_ee0.html")
        )
        wm = wafermap.WaferMap(
            wafer_radius=150,
            cell_size=(25.96, 15.504),
            cell_margin=(0.0, 0.0),
            grid_offset=(0, 0),
            edge_exclusion=3,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_26_15.5_ee3.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_26_15.5_ee3.html")
        )

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
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_margin_8_15.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_margin_8_15.html")
        )

    def test_wafermap_cell_origin(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0, 0),
            cell_origin=(0, 0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_origin_0_0.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_origin_0_0.html")
        )
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0, 0),
            cell_origin=(2, 1),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_origin_2_1.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_origin_2_1.html")
        )
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0, 0),
            cell_origin=(0, -2),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_origin_0_-2.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_origin_0_-2.html")
        )
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0, 0),
            cell_origin=(0, -10),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_origin_0_-10.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_origin_0_-10.html")
        )

    def test_wafermap_colors(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0, 0),
            cell_origin=(0, 0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
            wafer_edge_color=(0.0, 0.1, 0.9),
            map_bg_color=None,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_color1.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_color1.html")
        )
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0, 0),
            cell_origin=(0, 0),
            grid_offset=(-2.05, -4.1),
            edge_exclusion=2.2,
            coverage="full",
            notch_orientation=270,
            wafer_edge_color=(0, 0, 0),
            map_bg_color=(0.3, 0.9, 1.0),
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_color2.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_color2.html")
        )

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
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_ee_10.html"))
        assert os.path.isfile(os.path.join(self.output_dir, "test_wafermap_ee_10.html"))

    def test_wafermap_png1(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            coverage="full",
            notch_orientation=270,
        )
        wm.save_png(
            os.path.join(self.output_dir, "test_wafermap_png1.png"), autocrop=False
        )
        assert os.path.isfile(os.path.join(self.output_dir, "test_wafermap_png1.png"))

    def test_wafermap_png2(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.2, 21.9),
            cell_margin=(0.1, 0.1),
            grid_offset=(-3.1, 0.0),
            coverage="full",
            notch_orientation=270,
        )
        wm.save_png(
            os.path.join(self.output_dir, "test_wafermap_png2_autocrop.png"),
            autocrop=True,
        )
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_png2_autocrop.png")
        )

    def test_wafermap_add_image1(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(13.702, 24.846),
            cell_margin=(0.0, 0.0),
            grid_offset=(-2.05, -4.1),
            coverage="full",
            notch_orientation=270,
        )
        # cell coordinates
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_17_147375.jpg"
            ),
            cell=(0, 0),
            offset=(0.0, 0.0),
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_2_125416.jpg"
            ),
            cell=(1, 0),
            offset=(2.0, 2.0),
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_17_147378.jpg"
            ),
            cell=(3, 0),
            offset=(0.5, 0.5),
            marker_style={},
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_2_125416.jpg"
            ),
            cell=(0, -2),
            offset=(12.0, 5.0),
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_17_147378.jpg"
            ),
            cell=(0, -2),
            offset=(28.0, 3),
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_2_125416.jpg"
            ),
            cell=(0, 1),
            offset=(0.0, 0.0),
            marker_style={},
        )
        # wafer coordinates
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_17_147375.jpg"
            ),
            cell=None,
            offset=(10.0, 100.0),
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_2_125416.jpg"
            ),
            cell=None,
            offset=(-5, 78.6),
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_17_147378.jpg"
            ),
            cell=None,
            offset=(-121.2, -24.9),
            marker_style={},
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_image1.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_image1.html")
        )

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
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_17_147375.jpg"
            ),
            cell=(0, 0),
            offset=(0.0, 0.0),
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_2_125416.jpg"
            ),
            cell=(1, 0),
            offset=(2.0, 2.0),
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_17_147378.jpg"
            ),
            cell=(3, 0),
            offset=(0.5, 0.5),
            marker_style={},
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_2_125416.jpg"
            ),
            cell=(0, -2),
            offset=(5, 12),
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_17_147378.jpg"
            ),
            cell=(0, -2),
            offset=(3, 28),
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_2_125416.jpg"
            ),
            cell=(0, 1),
            offset=(0.0, 0.0),
            marker_style={},
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_image2.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_image2.html")
        )

    def test_wafermap_add_image3(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(15.29, 14.985),
            cell_margin=(0.33, 0.735),
            grid_offset=(0.5, 8.5),
            edge_exclusion=2.0,
            coverage="full",
            notch_orientation=270,
            conversion_factor=1.0,
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_17_147375.jpg"
            ),
            cell=(1, -5),
            offset=(0.0, 0.0),
            marker_style={},
        )
        wm.add_point(cell=(1, -5), offset=(0, 0))
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_17_147375.jpg"
            ),
            cell=None,
            offset=(9.0, 62.0),
            marker_style={},
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_image3.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_image3.html")
        )

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
            (None, [(0, 0), (100, 75)]),  # wafer coordinates
            (None, [(-12.3, -62.33), (5, 21.0)]),  # wafer coordinates
            (None, [(-10, 0), (-12, 3.2)]),  # wafer coordinates
            (None, [(-151, 0), (-152, 3.2)]),  # wafer coordinates
        ]
        colors = ["green", "red", "blue", "black", "purple", "orange", "brown", "grey"]
        for cell, vector in vectors:
            random_color = rnd.choice(colors)
            wm.add_vector(
                vector_points=vector,
                cell=cell,
                vector_style={"color": random_color},
                root_style={"radius": 1, "color": random_color},
            )

        wm.save_html(os.path.join(self.output_dir, "test_wafermap_vectors1.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_vectors1.html")
        )

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
                    (rnd.uniform(0, cell_size[0]), rnd.uniform(0, cell_size[1])),
                    (rnd.uniform(0, cell_size[0]), rnd.uniform(0, cell_size[1])),
                ],
            )
            for cell in wm
        ]
        for cell, vector in vectors:
            wm.add_vector(
                vector_points=vector,
                cell=cell,
                root_style={"radius": 1, "color": "black"},
            )

        wm.save_html(os.path.join(self.output_dir, "test_wafermap_vectors2.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_vectors2.html")
        )

    def test_wafermap_add_vectors3(self):
        wafer_radius = 100
        n_vectors = 1000
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(26, 14),
            cell_margin=(0.0, 0.0),
            grid_offset=(0, 0),
            coverage="full",
            notch_orientation=270,
        )

        vectors = [
            (
                None,
                [
                    (rnd.gauss(0, wafer_radius / 10), rnd.gauss(0, wafer_radius / 10)),
                    (rnd.gauss(0, wafer_radius / 2), rnd.gauss(0, wafer_radius / 2)),
                ],
            )
            for _ in range(n_vectors)
        ]
        for cell, vector in vectors:
            wm.add_vector(
                vector_points=vector,
                cell=cell,
                root_style={"radius": 1, "color": "black"},
            )

        wm.save_html(os.path.join(self.output_dir, "test_wafermap_vectors3.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_vectors3.html")
        )

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

        wm.save_html(os.path.join(self.output_dir, "test_wafermap_points1.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_points1.html")
        )

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
            for cell in wm
        ]
        for cell, cell_points_ in cell_points:
            for cell_point in cell_points_:
                wm.add_point(cell=cell, offset=cell_point)

        wm.save_html(os.path.join(self.output_dir, "test_wafermap_points2.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_points2.html")
        )

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

        for cell in wm:
            if sum(cell) % 3 == 0:
                wm.add_label(
                    cell=cell,
                    offset=(cell_size[0] / 2, cell_size[1] / 2),
                    label_text=f"Label: {cell}",
                )
            elif sum(cell) % 3 == 1:
                wm.add_label(
                    cell=cell,
                    offset=(cell_size[0] / 2, cell_size[1] / 2),
                    label_text=f"Multiline\nlabel\ncell: {cell}",
                )
            else:
                wm.add_label(
                    cell=cell,
                    offset=(cell_size[0] / 2, cell_size[1] / 2),
                    label_text=f"This is a longer label: {cell}",
                )

        wm.save_html(os.path.join(self.output_dir, "test_wafermap_labels1.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_labels1.html")
        )

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
        for cell in wm:
            random_cell_style = {
                "fill": rnd.random() > 0.5,
                "fillColor": named_html_colors[
                    rnd.randint(0, len(named_html_colors) - 1)
                ],
                "fillOpacity": rnd.random(),
            }
            wm.style_cell(cell=cell, cell_style=random_cell_style)

        wm.save_html(os.path.join(self.output_dir, "test_wafermap_style_cells1.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_style_cells1.html")
        )

    def test_wafermap_heatmap1(self):

        cell_size = (26, 14)
        N_cell = 100
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=cell_size,
            cell_margin=(0.0, 0.0),
            grid_offset=(0, 0),
            coverage="full",
            notch_orientation=270,
        )

        data = {}
        for cell_x, cell_y in wm:
            n = rnd.randint(0, N_cell)
            for _ in range(n):
                data[
                    (
                        cell_x,
                        cell_y,
                        rnd.gauss(cell_size[0] / 2, cell_size[0] / 4),
                        rnd.gauss(cell_size[1] / 2, cell_size[1] / 4),
                    )
                ] = rnd.gauss(0, 1)

        wm.add_heatmap(data)

        wm.save_html(os.path.join(self.output_dir, "test_wafermap_heatmap1.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_heatmap1.html")
        )

    def test_wafermap_heatmap2(self):

        wafer_radius = 100
        N = 1000
        wm = wafermap.WaferMap(
            wafer_radius=wafer_radius,
            cell_size=(26, 14),
            cell_margin=(0.0, 0.0),
            grid_offset=(0, 0),
            coverage="full",
            notch_orientation=270,
            conversion_factor=1e-2,
        )

        data = [
            (
                rnd.gauss(0, wafer_radius / 4),
                rnd.gauss(0, wafer_radius / 4),
                rnd.gauss(0, 1),
            )
            for _ in range(N)
        ]

        wm.add_heatmap(data)

        wm.save_html(os.path.join(self.output_dir, "test_wafermap_heatmap2.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_heatmap2.html")
        )

    def test_wafermap_example1(self):
        # define the wafermap
        cell_size = (10, 20)
        wm = wafermap.WaferMap(
            wafer_radius=100,  # all length dimensions in meters
            cell_size=cell_size,  # (sizeX, sizeY)
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
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_17_147378.jpg"
            ),
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
        for color, (cell, vector) in zip(colors, vectors, strict=True):
            wm.add_vector(
                vector_points=vector,
                cell=cell,
                vector_style={"color": color},
                root_style={"radius": 1, "color": color},
            )

        # add 50 points per cell, in a random distribution
        cell_points = [
            (
                cell,
                [
                    (
                        rnd.gauss(cell_size[0] / 2, cell_size[0] / 6),
                        rnd.gauss(cell_size[1] / 2, cell_size[1] / 6),
                    )
                    for _ in range(50)
                ],
            )
            for cell in wm
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
        for i, cell_idx in enumerate(wm):
            if i > rnd.randint(0, len(wm)) / 1.5:
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
                    offset=(cell_size[0] / 2, cell_size[1] / 2),
                    label_text=picked_fg_color,
                    label_html_style=random_label_style,
                )

        # save to png
        wm.save_png(
            os.path.join(self.output_dir, "test_wafermap_example1.png"), autocrop=True
        )
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_example1.png")
        )
        # save to html
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_example1.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_example1.html")
        )

    def test_wafermap_example2(self):
        # define the wafermap
        wm = wafermap.WaferMap(
            wafer_radius=150.0,
            cell_size=(6.0, 10.0),
            cell_origin=(-6, -12),
            cell_margin=(0.0, 0.0),
            grid_offset=(0.0, 0.0),
            edge_exclusion=0,
            coverage="inner",
            notch_orientation=270,
            conversion_factor=1e-2,
        )

        # save to png
        wm.save_png(
            os.path.join(self.output_dir, "test_wafermap_example2.png"), autocrop=False
        )
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_example2.png")
        )
        # save to html
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_example2.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_example2.html")
        )

    def test_wafermap_cells1(self):
        cells = []
        cell_size = (5.4, 12.55)
        cell_margin = (1.0, 2.5)
        wafer_radius = 150.0
        num_of_cells_x = int(2 * wafer_radius / (cell_size[0] + cell_margin[0])) + 1
        num_of_cells_y = int(2 * wafer_radius / (cell_size[1] + cell_margin[1])) + 1

        for i in range(num_of_cells_y):
            for j in range(num_of_cells_x):
                cells.append(
                    (
                        j * (cell_size[0] + cell_margin[0]) - wafer_radius,
                        i * (cell_size[1] + cell_margin[1]) - wafer_radius,
                        j,
                        i,
                    )
                )

        wm = wafermap.WaferMap(
            wafer_radius=wafer_radius,
            cell_size=cell_size,
            cell_margin=cell_margin,
            edge_exclusion=2.2,
            coverage="none",
            notch_orientation=270,
            cells=cells,
            conversion_factor=1,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_cells1.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_cells1.html")
        )

    def test_wafermap_cells2(self):
        cells = []
        cell_size = (5, 10)
        cell_margin = (0.0, 0.0)
        wafer_radius = 150.0
        edge_exclusion = 50
        coverage = "full"
        useful_area = 2 * (wafer_radius - edge_exclusion)
        num_of_cells_x = int(useful_area / (cell_size[0] + cell_margin[0])) + 1
        num_of_cells_y = int(useful_area / (cell_size[1] + cell_margin[1])) + 1

        for i in range(num_of_cells_y):
            for j in range(num_of_cells_x):
                cells.append(
                    (
                        j * (cell_size[0] + cell_margin[0]) - useful_area / 2,
                        i * (cell_size[1] + cell_margin[1]) - useful_area / 2,
                        j,
                        i,
                    )
                )

        wm = wafermap.WaferMap(
            wafer_radius=wafer_radius,
            cell_size=cell_size,
            cell_margin=cell_margin,
            edge_exclusion=edge_exclusion,
            coverage=coverage,
            notch_orientation=270,
            cells=cells,
            conversion_factor=1,
        )
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_cells2.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_cells2.html")
        )

    def test_wafermap_pop_cell1(self):
        # define the wafermap
        wm = wafermap.WaferMap(
            wafer_radius=100,  # all length dimensions in mm
            cell_size=(15.29, 14.985),  # (sizeX, sizeY)
            cell_margin=(0.33, 0.735),  # distance between cell borders (x, y)
            cell_origin=(0, 0),  # which cell to select as origin (0, 0), in (x, y)
            grid_offset=(0.5, 8.5),  # grid offset in (x, y)
            edge_exclusion=2,  # margin from the wafer edge
            coverage="full",  # 'full': will cover wafer with cells
            notch_orientation=270,
            conversion_factor=1.0,  # angle of notch in degrees
        )

        # save to html
        wm.save_html(os.path.join(self.output_dir, "test_wafermap_pop_cell1.html"))
        assert os.path.isfile(
            os.path.join(self.output_dir, "test_wafermap_pop_cell1.html")
        )

    def test_wafermap_grid_cells(self):
        grid = wafermap.WaferMapGrid(wafer_radius=100, cell_size=(10, 20))
        assert len(grid) == 183
        # cell (0, 0) is centered on the wafer center
        assert grid[(0, 0)] == (
            (-5.0, -10.0),
            (5.0, -10.0),
            (-5.0, 10.0),
            (5.0, 10.0),
            (0.0, 0.0),
        )
        assert grid.cell_to_wafer_coordinates((1, 1), (2.0, 3.0)) == (7.0, 13.0)
        assert grid.cell_to_wafer_coordinates(None, (2.0, 3.0)) == (2.0, 3.0)
        with self.assertRaises(ValueError):
            grid.cell_to_wafer_coordinates((100, 100))

    def test_wafermap_iteration(self):
        grid = wafermap.WaferMapGrid(wafer_radius=50, cell_size=(10, 10))
        cells = list(grid)
        assert cells == list(grid.cell_map)
        assert [next(grid) for _ in range(len(grid))] == cells
        with self.assertRaises(StopIteration):
            next(grid)

    def test_wafermap_coverage_edge_crossing_cell(self):
        # a wide cell crossing the top edge of the wafer with no corner inside it
        cells = [(-30.0, 98.0, 0, 0)]
        full = wafermap.WaferMapGrid(
            wafer_radius=100, cell_size=(60, 10), cells=cells, edge_exclusion=0
        )
        inner = wafermap.WaferMapGrid(
            wafer_radius=100,
            cell_size=(60, 10),
            cells=cells,
            edge_exclusion=0,
            coverage="inner",
        )
        assert (0, 0) in full
        assert (0, 0) not in inner

    def test_wafermap_add_image_position(self):
        wm = wafermap.WaferMap(
            wafer_radius=100,
            cell_size=(15.29, 14.985),
            cell_margin=(0.33, 0.735),
            grid_offset=(0.5, 8.5),
        )
        wm.add_image(
            image_source_file=os.path.join(
                self.input_dir, "INS3300_Lot_1_Wafer_2_125416.jpg"
            ),
            cell=(1, -5),
            offset=(3.0, 2.0),
            marker_style={},
        )
        (overlay,) = wm._images_layer._children.values()
        assert isinstance(overlay, folium.raster_layers.ImageOverlay)
        cell_x, cell_y = wm[(1, -5)][0]
        upper_right_y, upper_right_x = overlay.bounds[1]
        assert overlay.bounds[0] == (cell_y + 2.0, cell_x + 3.0)
        # the image is resized to fit within the cell
        assert upper_right_x <= wm[(1, -5)][3][0]
        assert upper_right_y <= wm[(1, -5)][3][1]

    def test_wafermap_add_vector_input_unchanged(self):
        wm = wafermap.WaferMap(
            wafer_radius=100, cell_size=(10, 20), conversion_factor=0.5
        )
        vector_points = [(0, 0), (2, 4)]
        wm.add_vector(vector_points, cell=(0, 0), vector_length_scale=2)
        assert vector_points == [(0, 0), (2, 4)]
        (vector,) = wm._vectors_layer._children.values()
        assert isinstance(vector, folium.PolyLine)
        cell_x, cell_y = wm[(0, 0)][0]
        assert vector.locations == [[cell_y, cell_x], [cell_y + 4.0, cell_x + 2.0]]

    def test_wafermap_style_cell_default(self):
        wm = wafermap.WaferMap(wafer_radius=100, cell_size=(10, 20))
        wm.style_cell(cell=(0, 0))
        wm.style_cell(cell=None, cell_style={"fill": True, "fillColor": "red"})
        assert all(cell[5].options["fill"] for cell in wm.cell_map.values())
        with self.assertRaises(ValueError):
            wm.style_cell(cell=(100, 100), cell_style={"fill": True})

    def test_wafermap_save_html_string(self):
        wm = wafermap.WaferMap(wafer_radius=100, cell_size=(10, 20))
        html = wm.save_html(None)
        assert html is not None
        assert html.count('"zoomControl": true') == 1
        assert 'zoomControl": false' not in html
        with self.assertRaises(ValueError):
            wm.save_html("wafermap.png")

    def test_wafermap_save_png_without_html2image(self):
        wm = wafermap.WaferMap(wafer_radius=100, cell_size=(10, 20))
        html2image = wafermap.Html2Image
        wafermap.Html2Image = None
        try:
            with self.assertRaises(ImportError):
                wm.save_png(os.path.join(self.output_dir, "no_html2image.png"))
        finally:
            wafermap.Html2Image = html2image

    def test_wafermap_notch_shape(self):
        radius = 100.0
        for orientation in (0.0, 67.0, 270.0):
            outline = utils.wafer_outline(radius, notch_orientation=orientation)
            assert outline[0] == outline[-1]
            distances = [math.hypot(x, y) for x, y in outline]
            assert max(distances) <= radius + 1e-9
            # the notch bottom is 1 mm deep, in the notch direction
            deepest = min(range(len(outline)), key=distances.__getitem__)
            assert math.isclose(distances[deepest], radius - 1.0)
            x, y = outline[deepest]
            angle_error = (math.degrees(math.atan2(y, x)) - orientation + 180) % 360
            assert math.isclose(angle_error, 180.0)

        # notch sides at 45 degrees from the notch axis, i.e. a 90 degree notch
        outline = utils.wafer_outline(radius, notch_orientation=90.0)
        first_notch_point = next(
            i
            for i, point in enumerate(outline)
            if not math.isclose(math.hypot(*point), radius)
        )
        (edge_x, edge_y), (tangent_x, tangent_y) = outline[
            first_notch_point - 1 : first_notch_point + 1
        ]
        assert math.isclose(
            math.degrees(math.atan2(edge_x - tangent_x, edge_y - tangent_y)), 45.0
        )

    def test_wafermap_utils(self):
        assert utils.to255(-0.5, 0.5, 2.0) == (0, 128, 255)
        assert utils.rgb_to_html(1.0, 0.0, 0.0) == "#FF0000"
        assert utils.solid_color_png_url((255, 255, 255)).startswith(
            "data:image/png;base64,"
        )
        ((x, y),) = utils.rotate([(0.0, 1.0)], (0.0, 0.0), 90.0)
        assert math.isclose(x, 1.0) and math.isclose(y, 0.0, abs_tol=1e-12)
        ((x, y),) = utils.rotate([(2.0, 1.0)], (1.0, 1.0), 180.0)
        assert math.isclose(x, 0.0, abs_tol=1e-12) and math.isclose(y, 1.0)
        rho, phi = utils.cart2pol(0.0, 2.0)
        assert math.isclose(rho, 2.0) and math.isclose(phi, math.pi / 2)
        x, y = utils.pol2cart(rho, phi)
        assert math.isclose(x, 0.0, abs_tol=1e-12) and math.isclose(y, 2.0)
        assert utils.bounded_rectangle([(0, 0), (4, 2)], [(0, 0), (2, 2)]) == [
            (0, 0),
            (2, 1),
        ]
