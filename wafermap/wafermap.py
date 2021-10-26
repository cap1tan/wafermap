import base64
import math
import os
from io import BytesIO
from typing import List, Tuple, Union

import branca
import folium
from folium import IFrame, plugins
from PIL import Image
from wafermap import common

try:
    import selenium
except ImportError:
    selenium = None


class WaferMap:

    MAP_CONVERSION = 1e-3  # MAP_CONVERSION meters equal to 1 map meter
    NOTCH_HEIGHT = 1e-3 / MAP_CONVERSION
    NOTCH_WIDTH = 2.8284e-3 / MAP_CONVERSION
    DEFAULT_MARKER_STYLE = {"color": "#ff0000", "fill": True}
    DEFAULT_VECTOR_STYLE = {"color": "#009900", "weight": 1}
    DEFAULT_POINT_STYLE = {"radius": 0.5, "fill": True}
    IMAGE_SIZE_IN_POPUP = (400, 400)
    IMAGE_FOLDER = "\\_images\\"

    def __init__(
        self,
        wafer_radius: float,
        cell_size: Tuple[float, float],
        cell_margin=(0.0, 0.0),
        grid_offset=(0.0, 0.0),
        edge_exclusion=2.2e-3,
        coverage="full",
        notch_orientation=270,
        bg_color=(1, 1, 1),
        conversion_factor=1,
    ):
        """
        The wafermap origin is always the central die.
        :param wafer_radius: Wafer diameter in m
        :param cell_size: Cell size in m, (x, y)
        :param cell_margin: Distance between cells in m, (x, y)
        :param grid_offset: Grid offset in m, (x, y)
        :param edge_exclusion: # margin from the wafer edge where a red edge exclusion ring is drawn
        :param coverage: Options of 'full', 'inner'. 'full' will cover wafer with cells, partial cells allowed,
                         'inner' will only allow full cells
        :param bg_color: Tuple of (r, g, b), 0-255.
        :param conversion_factor: Factor to multiply input dimensions with.
        """

        assert cell_size[0] > 0
        assert cell_size[1] > 0

        self.coverage = coverage.lower()
        self.cell_size_x = conversion_factor * cell_size[0] / WaferMap.MAP_CONVERSION
        self.cell_size_y = conversion_factor * cell_size[1] / WaferMap.MAP_CONVERSION
        self.cell_margin_x = (
            conversion_factor * cell_margin[0] / WaferMap.MAP_CONVERSION
        )
        self.cell_margin_y = (
            conversion_factor * cell_margin[1] / WaferMap.MAP_CONVERSION
        )
        self.wafer_radius = conversion_factor * wafer_radius / WaferMap.MAP_CONVERSION
        self.edge_exclusion = (
            conversion_factor * edge_exclusion / WaferMap.MAP_CONVERSION
        )
        self.grid_offset_x = (
            conversion_factor * grid_offset[0] / WaferMap.MAP_CONVERSION
        )
        self.grid_offset_y = (
            conversion_factor * grid_offset[1] / WaferMap.MAP_CONVERSION
        )
        self._num_of_cells_x = math.ceil(2 * self.wafer_radius / self.cell_size_x)
        self._num_of_cells_y = math.ceil(2 * self.wafer_radius / self.cell_size_y)
        self.notch_orientation = notch_orientation
        wafer_edge_color = common.rgb_to_html(*common.complementary(*bg_color))

        # init the cell map
        # the cell map is a dict that corresponds the pixel coordinates of the bounding box of each cell to the cell
        # index {(0, 0): [(x_lower_left, y_lower_left), (x_lower_right, y_lower_right), (x_upper_left, y_upper_left),
        # (x_upper_right, y_upper_right)]}
        self.cell_map = {}

        # Init the folium map
        m = folium.Map(
            tiles=None, crs="Simple", control_scale=False, zoom_control=False
        )

        # Add the base layer
        # Create a white image of 4 pixels, and embed it in a url.
        white_tile = branca.utilities.image_to_url(
            [[bg_color, bg_color], [bg_color, bg_color]]
        )
        # create base TileLayer (white background)
        base = folium.raster_layers.TileLayer(
            tiles=white_tile,
            name="base",
            attr="white tile",
            zoom_start=2,
            min_zoom=1,
            max_zoom=5,
        )
        base.add_to(m)

        # Init rest of layers
        self._grid_layer = folium.map.FeatureGroup(name="grid")
        self._cell_labels_layer = folium.map.FeatureGroup(
            name="cell labels", show=False
        )
        self._edge_exclusion_layer = folium.map.FeatureGroup(name="edge exclusion")
        self._images_layer = folium.map.FeatureGroup(name="images")
        self._markers_layer = folium.map.FeatureGroup(name="markers")
        self._vectors_layer = folium.map.FeatureGroup(name="vectors")

        # Add wafer edge
        folium.Circle(
            radius=self.wafer_radius,
            location=(0.0, 0.0),
            popup="Wafer edge",
            color=wafer_edge_color,
            fill=False,
        ).add_to(m)

        # Add wafer edge exclusion
        if self.edge_exclusion > 0:
            folium.Circle(
                radius=self.wafer_radius - self.edge_exclusion,
                location=(0.0, 0.0),
                popup="Edge Exclusion",
                color="#ff4d4d",
                weight=1,
                fill=False,
            ).add_to(self._edge_exclusion_layer)

        # Add notch
        folium.Polygon(
            locations=common.rotate(
                [
                    (0.0, self.wafer_radius - WaferMap.NOTCH_HEIGHT),
                    (WaferMap.NOTCH_WIDTH, self.wafer_radius),
                    (-WaferMap.NOTCH_WIDTH, self.wafer_radius),
                    (0.0, self.wafer_radius - WaferMap.NOTCH_HEIGHT),
                ],
                (0, 0),
                angle=self.notch_orientation,
            ),
            popup="Notch",
            color=wafer_edge_color,
            fill=False,
        ).add_to(m)

        # grid v2
        min_index_x = -math.ceil(self._num_of_cells_x / 2) - 1
        max_index_x = math.ceil(self._num_of_cells_x / 2) + 1
        min_index_y = -math.ceil(self._num_of_cells_y / 2) - 1
        max_index_y = math.ceil(self._num_of_cells_y / 2) + 1
        for ix in range(min_index_x, max_index_x):
            for iy in range(min_index_y, max_index_y):
                # print a box
                lower_bound = (
                    (iy - 0.5) * (self.cell_size_y + self.cell_margin_y)
                    + self.grid_offset_y,
                    (ix - 0.5) * (self.cell_size_x + self.cell_margin_x)
                    + self.grid_offset_x,
                )
                upper_bound = (
                    (iy + 0.5) * (self.cell_size_y + self.cell_margin_y)
                    + self.grid_offset_y,
                    (ix + 0.5) * (self.cell_size_x + self.cell_margin_x)
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
                bounds = [lower_left, lower_right, upper_left, upper_right]
                # cell_center = (lower_bound[0] + self.cell_size_y / 2, lower_bound[1] + self.cell_size_x / 2)
                # distance_from_wafer_center = math.sqrt(cell_center[0]**2 + cell_center[1]**2)
                cell_label = (iy, ix)

                if (
                    self.coverage == "full"
                    and any(
                        list(
                            map(
                                lambda points: common.euclidean_distance(points)
                                <= self.wafer_radius,
                                bounds,
                            )
                        )
                    )
                ) or (
                    self.coverage == "inner"
                    and all(
                        list(
                            map(
                                lambda points: common.euclidean_distance(points)
                                <= self.wafer_radius,
                                bounds,
                            )
                        )
                    )
                ):
                    folium.vector_layers.Rectangle(
                        [lower_left, upper_right],
                        popup=None,
                        tooltip=None,
                        color="#404040",
                        weight=0.1,
                        fill=False,
                    ).add_to(self._grid_layer)

                    self.cell_map[cell_label] = bounds
                    # print labels
                    folium.map.Marker(
                        [
                            lower_left[0] + (0.5 * self.cell_size_y),
                            lower_left[1] + (0.5 * self.cell_size_x),
                        ],
                        icon=folium.features.DivIcon(
                            icon_size=(40, 10),
                            icon_anchor=(0, 0),
                            html=f'<div style="font-size: 8pt; color: black; text-align: center">{str(cell_label)}</div>',
                        ),
                    ).add_to(self._cell_labels_layer)

                elif self.coverage != "full" and self.coverage != "inner":
                    raise ValueError("Coverage mode " + coverage + " is not supported.")

        self._grid_layer.add_to(m)
        self._cell_labels_layer.add_to(m)
        self._edge_exclusion_layer.add_to(m)
        self._images_layer.add_to(m)
        self._markers_layer.add_to(m)
        self._vectors_layer.add_to(m)

        self.map = m

    def save_html(self, output_file="wafermap.html") -> str:
        assert os.path.splitext(output_file)[1].lower() == ".html"
        folium.plugins.MousePosition(
            position="topright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            prefix="Wafer Coordinates:",
        ).add_to(self.map)

        folium.LayerControl().add_to(self.map)
        # folium.plugins.MeasureControl().add_to(self.map)
        self.map.fit_bounds(
            [
                (-self.wafer_radius, -self.wafer_radius),
                (self.wafer_radius, self.wafer_radius),
            ]
        )
        self.map.save(output_file)
        return output_file

    def save_png(self, output_file="wafermap.png") -> Union[str, None]:
        # TODO: Do without relying on selenium
        if selenium is None:
            raise EnvironmentError(
                "Error: Selenium is required to export to png and is not installed."
            )
        assert os.path.splitext(output_file)[1].lower() == ".png"
        self._cell_labels_layer.show = False
        try:
            png_image = self.map._to_png(delay=1)
        except selenium.common.exceptions.SessionNotCreatedException:
            raise EnvironmentError(
                f"Error: Mozilla is not installed. Could not export wafermap to image {output_file}."
            )

        with open(output_file, "wb") as png_file:
            png_file.write(png_image)

        # crop image
        im = Image.open(output_file)
        # find image size
        width, height = im.size
        width_to_crop = (
            width - height
        )  # turn image into square by copping its width. Its height will always be representative of the wafer size in pixels
        im = im.crop(
            (width_to_crop / 2, 0, width - width_to_crop / 2, height)
        )  # (left, top, right, bottom), origin (0,0) is at the top left of the image
        im.save(output_file)
        return output_file

    def add_image(
        self,
        image_source_file: str,
        marker_style=None,
        cell: Tuple[int, int] = (0, 0),
        offset: Tuple[float, float] = (0.0, 0.0),
    ):
        """
        Add an image at the location specified by cell + offset. If marker_style flag is an empty dict, the image will
        be embedded directly on the wafermap, else a marker with a popup will be created.
        :param image_source_file: The path to the image file.
        :param marker_style: if not empty, a marker will be created with the defined style that when clicked, opens the
                             image in a popup. If empty the image will be embedded directly on the wafermap and the
                             image will be resized to fit the cell.
        :param cell: Tuple of cell index. If blank, the central cell is taken as default.
        :param offset: Tuple of offset from cell center in meters.
        """

        if marker_style is None:
            marker_style = WaferMap.DEFAULT_MARKER_STYLE
        if not os.path.isfile(image_source_file) or cell not in self.cell_map:
            return
        offset = (
            offset[0] / WaferMap.MAP_CONVERSION,
            offset[1] / WaferMap.MAP_CONVERSION,
        )

        # Open and read image image
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
        image_coordinates = (
            self.cell_map[cell][0][0] + offset[0],
            self.cell_map[cell][0][1] + offset[1],
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
            (self.cell_map[cell][3][0], self.cell_map[cell][3][1]),
        ]
        if not marker_style:

            # add image as ImageOverlay
            folium.raster_layers.ImageOverlay(
                image=image_source_file,
                bounds=common.bounded_rectangle(rect=image_bounds, bounds=cell_bounds),
                origin="lower",
                pixelated=False,
            ).add_to(self._images_layer)
        else:
            html_popup = f'<html><head></head><body><img src="data:image/jpeg;base64,{image_file.decode("utf-8")}" alt="{os.path.basename(image_source_file)}"></body><html>'
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
        :param root_style: If give, trhe vector will have a point as root with the given style
        :param vector_points: [(y_start, x_start), (y_end, x_end)]
        :param vector_length_scale: Value to multiply the vector length by
        :param cell: Tuple of cell index (y, x). If blank, the central cell is taken as default. If None is passed, the
        vector_points are interpreted as wafer coordinates.
        :param vector_style: A dict with style options
        """

        if root_style is None:
            root_style = {}
        if vector_style is None:
            vector_style = WaferMap.DEFAULT_VECTOR_STYLE
        if not len(vector_points) == 2:
            return
        if vector_style != WaferMap.DEFAULT_VECTOR_STYLE:
            vector_style = {**WaferMap.DEFAULT_VECTOR_STYLE, **vector_style}

        if cell:
            if cell in self.cell_map:
                # vector_points is cell coordinates
                origin = self.cell_map[cell][0]  # already converted to MAP coordinates
                vector_points = [
                    (
                        vector_points[0][0] / WaferMap.MAP_CONVERSION + origin[0],
                        vector_points[0][1] / WaferMap.MAP_CONVERSION + origin[1],
                    ),
                    (
                        (
                            vector_points[0][0]
                            + vector_length_scale
                            * (vector_points[1][0] - vector_points[0][0])
                        )
                        / WaferMap.MAP_CONVERSION
                        + origin[0],
                        (
                            vector_points[0][1]
                            + vector_length_scale
                            * (vector_points[1][1] - vector_points[0][1])
                        )
                        / WaferMap.MAP_CONVERSION
                        + origin[1],
                    ),
                ]
            else:
                return  # do nothing when cell doesnt exist
        else:
            # vector_points is wafer coordinates
            vector_points = [
                (
                    vector_points[0][0] / WaferMap.MAP_CONVERSION,
                    vector_points[0][1] / WaferMap.MAP_CONVERSION,
                ),
                (
                    (
                        vector_points[0][0]
                        + vector_length_scale
                        * (vector_points[1][0] - vector_points[0][0])
                    )
                    / WaferMap.MAP_CONVERSION,
                    (
                        vector_points[0][1]
                        + vector_length_scale
                        * (vector_points[1][1] - vector_points[0][1])
                    )
                    / WaferMap.MAP_CONVERSION,
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
        folium.plugins.PolyLineTextPath(vector_line, "", repeat=False, offset=5).add_to(
            self._vectors_layer
        )

    def add_point(
        self,
        cell: Union[Tuple[int, int], None] = (0, 0),
        offset: Tuple[float, float] = (0.0, 0.0),
        point_style=None,
    ):
        """
        :param point_style: Draw a point with the given style
        :param offset: (y, x)
        :param cell: Tuple of cell index. If blank, the central cell is taken as default. If None is passed, the
        offset is interpreted as wafer coordinates.
        """

        if point_style is None:
            point_style = WaferMap.DEFAULT_POINT_STYLE
        if point_style != WaferMap.DEFAULT_POINT_STYLE:
            point_style = {**WaferMap.DEFAULT_POINT_STYLE, **point_style}

        if cell:
            if cell in self.cell_map:
                # offset is cell coordinates
                origin = self.cell_map[cell][0]  # already converted to MAP coordinates
                point_origin = (
                    offset[0] / WaferMap.MAP_CONVERSION + origin[0],
                    offset[1] / WaferMap.MAP_CONVERSION + origin[1],
                )
            else:
                raise ValueError(f"{str(cell)} does not exist in wafermap.")
        else:
            # offset is wafer coordinates
            point_origin = (
                offset[0] / WaferMap.MAP_CONVERSION,
                offset[1] / WaferMap.MAP_CONVERSION,
            )

        folium.CircleMarker(location=point_origin, **point_style).add_to(
            self._markers_layer
        )
