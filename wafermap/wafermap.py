"""Wafermap class implementation"""

import base64
import math
import os
from io import BytesIO
from typing import List, Tuple, Union

import branca
import folium
from folium import Element, IFrame, plugins
from PIL import Image

from wafermap import utils

try:
    import selenium
    from selenium import webdriver
except ImportError:
    selenium = None
    webdriver = None


class WaferMap:
    """Main WaferMap class. Represents a circular wafer layout, with a grid, an edge
    exclusion, cells and several types of markers (points, vectors, images)."""

    NOTCH_HEIGHT = 1
    NOTCH_WIDTH = 2.8284
    DEFAULT_MARKER_STYLE = {"color": "#ff0000", "fill": True}
    DEFAULT_VECTOR_STYLE = {"color": "#009900", "weight": 1}
    DEFAULT_POINT_STYLE = {"radius": 0.5, "fill": True}
    DEFAULT_LABEL_FONT_SIZE = 8
    DEFAULT_LABEL_HTML_STYLE = (
        f"font-size: {DEFAULT_LABEL_FONT_SIZE}pt; color: black; text-align: center;"
    )
    IMAGE_SIZE_IN_POPUP = (400, 400)
    IMAGE_FOLDER = "\\_images\\"
    MAP_PADDING = (100, 100)  # in pixels (x, y)

    def __init__(
        self,
        wafer_radius: float,
        cell_size: Tuple[float, float],
        cell_margin=(0.0, 0.0),
        grid_offset=(0.0, 0.0),
        edge_exclusion=3,
        coverage="full",
        notch_orientation=270,
        bg_color=(1, 1, 1),
        conversion_factor=1,
    ):
        """
        The wafermap origin is always the central die.
        :param wafer_radius: Wafer diameter in mm
        :param cell_size: Cell size in mm, (x, y)
        :param cell_margin: Distance between cells in mm, (x, y)
        :param grid_offset: Grid offset in mm, (x, y)
        :param edge_exclusion: Margin from the wafer edge where a red edge exclusion
        ring is drawn in mm.
        :param coverage: Options of 'full', 'inner'. Option 'full' will cover wafer with
         cells, partial cells allowed, 'inner' will only allow full cells
        :param bg_color: Tuple of (r, g, b), 0-255.
        :param conversion_factor: Factor to multiply input dimensions with.
        """

        assert cell_size[0] > 0
        assert cell_size[1] > 0
        assert coverage.lower() in ["full", "inner"]

        self.coverage = coverage.lower()
        self.cell_size_x = conversion_factor * cell_size[0]
        self.cell_size_y = conversion_factor * cell_size[1]
        self.cell_margin_x = conversion_factor * cell_margin[0]
        self.cell_margin_y = conversion_factor * cell_margin[1]
        self.wafer_radius = conversion_factor * wafer_radius
        self.edge_exclusion = conversion_factor * edge_exclusion
        self.grid_offset_x = conversion_factor * grid_offset[0]
        self.grid_offset_y = conversion_factor * grid_offset[1]
        self._num_of_cells_x = math.ceil(2 * self.wafer_radius / self.cell_size_x)
        self._num_of_cells_y = math.ceil(2 * self.wafer_radius / self.cell_size_y)
        self.notch_orientation = notch_orientation
        wafer_edge_color = utils.rgb_to_html(*utils.complementary(*bg_color))

        # init the _cell_map
        # the cell map is a dict that corresponds the pixel coordinates of the bounding
        # box of each cell to the cell index:
        # {(cell_y, cell_x): ((y_lower_left, x_lower_left),
        #                     (y_lower_right, x_lower_right),
        #                     (y_upper_left, x_upper_left),
        #                     (y_upper_right, x_upper_right),
        #                     (y_cell_center, x_cell_center),
        #                     folium.vector_layers.Rectangle
        #                     )}
        # We consider the cell origin to be its lower left corner
        # y is latitude, x is longitude
        self._cell_map = {}

        # Init the folium map
        folium_map = folium.Map(
            tiles=None,
            crs="Simple",
            prefer_canvas=True,
            control_scale=False,
            zoom_control=False,
            zoom_start=1,
            min_zoom=0.1,
            max_zoom=1000,
            zoomSnap=0,
            zoomDelta=0.1,
            png_enabled=True,
        )

        # Add the base layer
        # Create a white image of 4 pixels, and embed it in an url.
        white_tile = branca.utilities.image_to_url([[bg_color] * 2, [bg_color] * 2])
        # create base TileLayer (white background)
        self._tile_layer = folium.raster_layers.TileLayer(
            tiles=white_tile,
            name="base",
            attr="white tile",
        )
        self._tile_layer.add_to(folium_map)

        # Init rest of layers
        self._grid_layer = folium.map.FeatureGroup(name="grid")
        self._cell_labels_layer = folium.map.FeatureGroup(
            name="cell labels", show=False
        )
        self._labels_layer = folium.map.FeatureGroup(name="labels", show=False)
        self._edge_exclusion_layer = folium.map.FeatureGroup(name="edge exclusion")
        self._images_layer = folium.map.FeatureGroup(name="images")
        self._markers_layer = folium.map.FeatureGroup(name="markers")
        self._vectors_layer = folium.map.FeatureGroup(name="vectors")

        # Add wafer edge
        folium.Circle(
            radius=self.wafer_radius,
            location=(0.0, 0.0),
            color=wafer_edge_color,
            fill=False,
        ).add_to(folium_map)

        # Add notch
        folium.Polygon(
            locations=utils.rotate(
                [
                    (0.0, self.wafer_radius - WaferMap.NOTCH_HEIGHT),
                    (WaferMap.NOTCH_WIDTH, self.wafer_radius),
                    (-WaferMap.NOTCH_WIDTH, self.wafer_radius),
                    (0.0, self.wafer_radius - WaferMap.NOTCH_HEIGHT),
                ],
                (0, 0),
                angle=self.notch_orientation,
            ),
            color=wafer_edge_color,
            fill=False,
        ).add_to(folium_map)

        # Add wafer edge exclusion
        if self.edge_exclusion > 0:
            folium.Circle(
                radius=self.wafer_radius - self.edge_exclusion,
                location=(0.0, 0.0),
                color="#ff4d4d",
                weight=1,
                fill=False,
            ).add_to(self._edge_exclusion_layer)

        # Add grid
        min_index_x = -math.ceil(self._num_of_cells_x / 2) - 1
        max_index_x = math.ceil(self._num_of_cells_x / 2) + 1
        min_index_y = -math.ceil(self._num_of_cells_y / 2) - 1
        max_index_y = math.ceil(self._num_of_cells_y / 2) + 1
        for i_x in range(min_index_x, max_index_x):
            for i_y in range(min_index_y, max_index_y):
                cell_label = (i_y, i_x)
                # print a box
                lower_bound = (
                    (i_y - 0.5) * (self.cell_size_y + self.cell_margin_y)
                    + self.grid_offset_y,
                    (i_x - 0.5) * (self.cell_size_x + self.cell_margin_x)
                    + self.grid_offset_x,
                )
                upper_bound = (
                    (i_y + 0.5) * (self.cell_size_y + self.cell_margin_y)
                    + self.grid_offset_y,
                    (i_x + 0.5) * (self.cell_size_x + self.cell_margin_x)
                    + self.grid_offset_x,
                )
                lower_left = (
                    lower_bound[0] + self.cell_margin_y / 2,
                    lower_bound[1] + self.cell_margin_x / 2,
                )
                lower_right = (
                    lower_bound[0] + self.cell_margin_y / 2,
                    lower_bound[1] + self.cell_size_x - self.cell_margin_x / 2,
                )
                upper_left = (
                    upper_bound[0] - self.cell_margin_y / 2,
                    upper_bound[1] - self.cell_size_x + self.cell_margin_x / 2,
                )
                upper_right = (
                    upper_bound[0] - self.cell_margin_y / 2,
                    upper_bound[1] - self.cell_margin_x / 2,
                )
                bounds = (lower_left, lower_right, upper_left, upper_right)
                center = (
                    (lower_left[0] + upper_left[0]) / 2,
                    (lower_left[1] + lower_right[1]) / 2,
                )

                in_for_full = any(
                    list(
                        map(
                            lambda points: utils.euclidean_distance(points)
                            <= self.wafer_radius,
                            bounds,
                        )
                    )
                )
                in_for_inner = all(
                    list(
                        map(
                            lambda points: utils.euclidean_distance(points)
                            <= self.wafer_radius,
                            bounds,
                        )
                    )
                )

                if (self.coverage == "full" and in_for_full) or (
                    self.coverage == "inner" and in_for_inner
                ):
                    self._cell_map[cell_label] = bounds + (center,)  # in (y,x)
                    self._cell_map[cell_label] += (
                        folium.vector_layers.Rectangle(
                            [lower_left, upper_right],
                            popup=None,
                            tooltip=None,
                            color="#142d2d",
                            weight=0.2,
                            fill=False,
                        ),
                    )
                    self._cell_map[cell_label][5].add_to(self._grid_layer)

                    # print labels
                    folium.map.Marker(
                        [
                            lower_left[0] + (0.5 * self.cell_size_y),
                            lower_left[1] + (0.5 * self.cell_size_x),
                        ],
                        icon=folium.features.DivIcon(
                            icon_size=(50, 20),
                            icon_anchor=(25, 10),
                            html=f'<div style="font-size: 8pt; color: black;'
                            f'text-align: center">{str(cell_label)}</div>',
                        ),
                    ).add_to(self._cell_labels_layer)

        self._grid_layer.add_to(folium_map)
        self._cell_labels_layer.add_to(folium_map)
        self._labels_layer.add_to(folium_map)
        self._edge_exclusion_layer.add_to(folium_map)
        self._images_layer.add_to(folium_map)
        self._markers_layer.add_to(folium_map)
        self._vectors_layer.add_to(folium_map)
        # add extra controls
        plugins.MousePosition(
            position="topright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            prefix="Wafer Coordinates:",
        ).add_to(folium_map)
        folium.LayerControl().add_to(folium_map)

        self.map = folium_map

        # default zoom
        self.map.fit_bounds(
            [
                (-self.wafer_radius, -self.wafer_radius),
                (self.wafer_radius, self.wafer_radius),
            ],
            padding=(WaferMap.MAP_PADDING[0], WaferMap.MAP_PADDING[1]),
        )  # padding is in pixels while the zoom box is in (long, lat)

    @property
    def cell_map(self):
        # Internal attribute _cell_map uses (y,x) convention while WaferMap interfaces
        # with (x,y). Therefore, we provide cell_map as a property to interface with
        # outside the class, which fully converts _cell_map from (y,x) to (x,y)
        cell_map = {}
        for _cell_idx, _cell in self._cell_map.items():
            cell_idx = _cell_idx[1], _cell_idx[0]
            cell = ()
            for _cell_item in _cell:
                if type(_cell_item) is tuple:
                    cell += ((_cell_item[1], _cell_item[0]),)
                else:
                    cell += (_cell_item,)
            cell_map[cell_idx] = cell
        return cell_map

    def save_html(self, output_file="wafermap.html") -> str:
        """Save current Folium Map to HTML."""
        assert os.path.splitext(output_file)[1].lower() == ".html"
        # turn on/off relevant layers/controls
        self._cell_labels_layer.show = False
        self._labels_layer.show = False
        self.map.options["zoomControl"] = True
        self.map.save(output_file)
        return output_file

    def save_png(self, output_file="wafermap.png") -> Union[str, None]:
        """Save current Folium Map to a PNG image. Selenium is required."""
        if webdriver is None or selenium is None:
            raise EnvironmentError(
                "Error: Selenium is required to export to png and is not installed."
            )
        assert os.path.splitext(output_file)[1].lower() == ".png"
        # turn on/off relevant layers/controls
        self._cell_labels_layer.show = False
        self._labels_layer.show = True
        self.map.options["zoomControl"] = False
        try:
            options = webdriver.edge.options.Options()
            options.add_argument("--headless=new")
            edge_driver = webdriver.Edge(options=options)
            png_image = self.map._to_png(delay=1, driver=edge_driver)
        except selenium.common.exceptions.SessionNotCreatedException as exc:
            raise EnvironmentError(
                f"Error: Edge is not installed. Could not export wafermap to image "
                f"{output_file}."
            ) from exc

        with open(output_file, "wb") as png_file:
            png_file.write(png_image)

        # crop rest of controls out of image
        image = Image.open(output_file)
        width, height = image.size
        image = image.crop(
            (
                WaferMap.MAP_PADDING[0],
                WaferMap.MAP_PADDING[1],
                width - WaferMap.MAP_PADDING[0],
                height - WaferMap.MAP_PADDING[1],
            )
        )  # (left, top, right, bottom), origin (0,0) is at the top left of the image
        image.save(output_file)
        return output_file

    def add_image(
        self,
        image_source_file: str,
        marker_style=None,
        cell: Union[Tuple[int, int], None] = (0, 0),
        offset: Tuple[float, float] = (0.0, 0.0),
    ):
        """
        Add an image at the location specified by cell + offset. If marker_style flag is
         an empty dict, the image will be embedded directly on the wafermap, else a
         marker with a popup will be created.
        :param image_source_file: The path to the image file.
        :param marker_style: if not empty, a marker will be created with the defined
        style that when clicked, opens the image in a popup. If empty the image will be
        embedded directly on the wafermap and the image will be resized to fit the cell.
        :param cell: Tuple of cell index (x,y).  If None is passed, the offset is
        interpreted as (x,y) wafer coordinates.
        :param offset: Tuple of (x,y) offset from cell origin in mm.  Cell origin is
         the bottom left corner.
        """

        if marker_style is None:
            marker_style = WaferMap.DEFAULT_MARKER_STYLE
        if not os.path.isfile(image_source_file) or cell not in self._cell_map:
            return

        # given in (x,y) but internally we use (y,x) = (long, lat)
        if cell:
            cell = cell[1], cell[0]
        offset = offset[1], offset[0]

        if cell:
            if cell in self._cell_map:
                # offset is cell coordinates
                origin = self._cell_map[cell][0]
                image_origin = (
                    offset[0] + origin[0],
                    offset[1] + origin[1],
                )
            else:
                raise ValueError(f"{str(cell)} does not exist in wafermap.")
        else:
            # offset is wafer coordinates
            image_origin = (
                offset[0],
                offset[1],
            )

        # Open and read image
        with Image.open(image_source_file) as imf:
            try:
                imf.thumbnail(WaferMap.IMAGE_SIZE_IN_POPUP)
                image_width, image_height = imf.size
                buffered = BytesIO()
                imf.save(buffered, "JPEG")
                image_file = base64.b64encode(buffered.getvalue())
            except IOError:
                print(f"Error: Cannot create thumbnail for {image_source_file}")
        # find position to put image
        if cell:
            image_coordinates = (
                image_origin[0] + offset[0],
                image_origin[1] + offset[1],
            )
        else:
            # offset is wafer coordinates
            image_coordinates = (
                image_origin[0],
                image_origin[1],
            )
        image_bounds = [
            (image_coordinates[0], image_coordinates[1]),
            (
                image_coordinates[0] + image_height * 1 / 10,
                image_coordinates[1] + image_width * 1 / 10,
            ),
        ]
        cell_bounds = [
            (image_coordinates[0], image_coordinates[1]),
            (self._cell_map[cell][3][0], self._cell_map[cell][3][1]),
        ]
        if not marker_style:
            # add image as ImageOverlay
            folium.raster_layers.ImageOverlay(
                image=image_source_file,
                bounds=utils.bounded_rectangle(rect=image_bounds, bounds=cell_bounds),
                origin="lower",
                pixelated=False,
            ).add_to(self._images_layer)
        else:
            html_popup = (
                f'<html><head></head><body><img src="data:image/jpeg;base64,'
                f'{image_file.decode("utf-8")}" '
                f'alt="{os.path.basename(image_source_file)}"></body><html>'
            )
            iframe = IFrame(
                html_popup, width=image_width + 20, height=image_height + 20
            )
            image_popup = folium.Popup(iframe, parse_html=True, max_width=800)

            folium.CircleMarker(
                location=image_coordinates, radius=2, popup=image_popup, **marker_style
            ).add_to(self._markers_layer)

    def add_vector(
        self,
        vector_points: List[Tuple[float, float]],
        vector_length_scale: float = 1.0,
        cell: Union[Tuple[int, int], None] = (0, 0),
        vector_style=None,
        root_style=None,
    ):
        """
        Add a vector to the map.
        :param root_style: If given, the vector will have a point as root with the given
         style.
        :param vector_points: [(x_start, y_start), (x_end, y_end)] in mm. Cell origin is
         the bottom left corner.
        :param vector_length_scale: Value to multiply the vector length by
        :param cell: Tuple of cell index (x, y). If None is passed, the vector_points
        are interpreted as wafer coordinates.
        :param vector_style: A dict with style options.
        """

        if root_style is None:
            root_style = {}
        if vector_style is None:
            vector_style = WaferMap.DEFAULT_VECTOR_STYLE
        if not len(vector_points) == 2:
            return
        if vector_style != WaferMap.DEFAULT_VECTOR_STYLE:
            vector_style = {**WaferMap.DEFAULT_VECTOR_STYLE, **vector_style}

        # given in (x,y) but internally we use (y,x) = (long, lat)
        if cell:
            cell = cell[1], cell[0]
        for i, vector_point in enumerate(vector_points):
            vector_points[i] = vector_point[1], vector_point[0]

        if cell:
            if cell in self._cell_map:
                # vector_points is cell coordinates
                origin = self._cell_map[cell][0]  # already converted to MAP coordinates
                vector_points = [
                    (
                        vector_points[0][0] + origin[0],
                        vector_points[0][1] + origin[1],
                    ),
                    (
                        (
                            vector_points[0][0]
                            + vector_length_scale
                            * (vector_points[1][0] - vector_points[0][0])
                        )
                        + origin[0],
                        (
                            vector_points[0][1]
                            + vector_length_scale
                            * (vector_points[1][1] - vector_points[0][1])
                        )
                        + origin[1],
                    ),
                ]
            else:
                return  # do nothing when cell doesn't exist
        else:
            # vector_points is wafer coordinates
            vector_points = [
                (
                    vector_points[0][0],
                    vector_points[0][1],
                ),
                (
                    (
                        vector_points[0][0]
                        + vector_length_scale
                        * (vector_points[1][0] - vector_points[0][0])
                    ),
                    (
                        vector_points[0][1]
                        + vector_length_scale
                        * (vector_points[1][1] - vector_points[0][1])
                    ),
                ),
            ]

        if root_style:
            root_point = vector_points[0]
            folium.CircleMarker(location=root_point, **root_style).add_to(
                self._vectors_layer
            )

        vector_line = folium.PolyLine(vector_points, **vector_style).add_to(
            self._vectors_layer
        )
        plugins.PolyLineTextPath(vector_line, "", repeat=False, offset=5).add_to(
            self._vectors_layer
        )

    def add_point(
        self,
        cell: Union[Tuple[int, int], None] = (0, 0),
        offset: Tuple[float, float] = (0.0, 0.0),
        point_style=None,
        popup_text=None,
    ):
        """
        :param point_style: Draw a point with the given style
        :param offset: Tuple of (x,y) offset from cell origin in mm.  Cell origin is
         the bottom left corner.
        :param cell: Tuple of cell index (x,y). If None is passed, the offset is interpreted
        as wafer coordinates.
        :param popup_text: The text to display as a popup upon clicking the point. If
        None, no popup will be shown.
        """

        if point_style is None:
            point_style = WaferMap.DEFAULT_POINT_STYLE
        if point_style != WaferMap.DEFAULT_POINT_STYLE:
            point_style = {**WaferMap.DEFAULT_POINT_STYLE, **point_style}

        # given in (x,y) but internally we use (y,x) = (long, lat)
        if cell:
            cell = cell[1], cell[0]
        offset = offset[1], offset[0]

        if cell:
            if cell in self._cell_map:
                # offset is cell coordinates
                origin = self._cell_map[cell][0]
                point_origin = (
                    offset[0] + origin[0],
                    offset[1] + origin[1],
                )
            else:
                raise ValueError(f"{str(cell)} does not exist in wafermap.")
        else:
            # offset is wafer coordinates
            point_origin = (
                offset[0],
                offset[1],
            )

        folium.CircleMarker(
            location=point_origin, popup=popup_text, **point_style
        ).add_to(self._markers_layer)

    def add_label(
        self,
        cell: Union[Tuple[int, int], None] = (0, 0),
        offset: Tuple[float, float] = (0.0, 0.0),
        label_text="",
        label_html_style=None,
        popup_text=None,
    ):
        """
        :param label_html_style: Write a label with the given HTML style, e.g:
        'font-size: 8pt; color: black; text-align: center'
        :param offset: Tuple of (x,y) offset from cell origin in mm. Cell origin is the
        bottom left corner.
        :param label_text: The text of the label.
        :param cell: Tuple of cell index (x,y). If None is passed, the offset is
        interpreted as wafer coordinates.
        :param popup_text: The text to display as a popup upon clicking the label. If
        None, no popup will be shown.
        """

        if label_html_style is None:
            label_html_style = WaferMap.DEFAULT_LABEL_HTML_STYLE

        # given in (x,y) but internally we use (y,x) = (long, lat)
        if cell:
            cell = cell[1], cell[0]
        offset = offset[1], offset[0]

        if cell:
            if cell in self._cell_map:
                # offset is cell coordinates
                origin = self._cell_map[cell][0]  # already converted to MAP coordinates
                label_origin = (
                    offset[0] + origin[0],
                    offset[1] + origin[1],
                )
            else:
                raise ValueError(f"{str(cell)} does not exist in wafermap.")
        else:
            # offset is wafer coordinates. Origin is the center
            label_origin = (
                offset[0],
                offset[1],
            )
        # we multiply so that we have some scaling the label size with the
        # label size
        # 1pt is 1.333px
        label_size_px = (
            min(len(label_text) * WaferMap.DEFAULT_LABEL_FONT_SIZE * 1.333, 100),
            min(WaferMap.DEFAULT_LABEL_FONT_SIZE * 1.333, 100),
        )
        # put the label anchor at the center of the label
        label_anchor_px = (label_size_px[0] / 2, label_size_px[1] / 2)
        folium.map.Marker(
            location=label_origin,
            icon=folium.features.DivIcon(
                icon_size=label_size_px,
                icon_anchor=label_anchor_px,
                html=f'<div style="{label_html_style}">{label_text}</div>',
            ),
            popup=popup_text,
        ).add_to(self._labels_layer)

    def style_cell(
        self,
        cell: Union[Tuple[int, int], None] = (0, 0),
        cell_style=dict,
    ):
        """
        :param cell_style: Define the cell style
        :param cell: Tuple of cell index (x,y). If None is passed, all cells are styled.
        """

        # given in (x,y) but internally we use (y,x) = (long, lat)
        if cell:
            cell = cell[1], cell[0]

        if not cell:
            cells_to_style = [c for c in self._cell_map]
        else:
            if cell not in self._cell_map:
                raise ValueError(f"{str(cell)} does not exist in wafermap.")
            cells_to_style = [cell]

        for cell_to_style in cells_to_style:
            self._cell_map[cell_to_style][5].options |= cell_style
