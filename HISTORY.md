# History

## 0.1.0 (2021-10-23)

* First release on PyPI.

## 0.2.7

* Separated logic of grid construction to a `WaferMapGrid` base class
* Python support: 3.9 - 3.13
* Updated dependency versions

## 0.2.8

* Implemented input validation
* Fixed module definition to include `WaferMapGrid`
* Fixed some issues with `conversion_factor`
* Layer visibility when exporting to html or png is now not set by the corresponding function
* made `WaferMapGrid` iterable and addressable: 
    ```python
    for cell in wm:
    ...
    wm[x]
    ```

## 0.2.9

* Added heatmap functionality:

    ```python
    data = (np.random.normal(size=(100, 3)) * np.array([[30, 30, 1]])).tolist()
    wm.add_heatmap(data)
    ```

* Bug fixes (edge exclusion now properly excludes cells, margin is respecting wafer boundaries etc.)
* Small performance improvements

## 0.3.0

* Option to define cells manually with `cells=[(wafer_x, wafer_y, cell_x, cell_y), ...]`

## 0.3.1

* Fixed image placement (x/y swap) in `add_image`

## 0.3.2

* Dropped support for Python 3.9
* `save_png` falls back to Microsoft Edge when Chrome is not available

## 0.4.0

* Dependencies: `numpy` and `branca` are no longer direct dependencies. `html2image` is now
  optional; install it with `pip install wafermap[png]` to use `save_png`
* Fixed `add_image` applying the offset twice when a cell is given
* Fixed `add_vector` modifying the passed `vector_points` list
* Fixed `style_cell` failing when called without `cell_style`
* `coverage='full'` now includes every cell that overlaps the usable wafer area, also
  cells that cross the edge without any corner inside it
* `add_image` raises `ValueError` for unreadable images and supports non-RGB images in popups
* Exports no longer change the map's zoom control setting
* Faster cell iteration, smaller HTML output for vectors
* Realistic notch: a 1 mm deep, 90 degree V-notch with a rounded bottom (0.9 mm
  radius) cut out of the wafer edge, after SEMI M1, instead of a triangle drawn over the
  edge circle. `WaferMap.NOTCH_HEIGHT`/`NOTCH_WIDTH` are replaced by `NOTCH_DEPTH`,
  `NOTCH_ANGLE` and `NOTCH_BOTTOM_RADIUS`. New helper `utils.wafer_outline`
* Development tooling: ruff (lint, format, import sorting) and ty (type checking) replace
  black, isort and flake8. Type annotations for style arguments; `add_vector` accepts any
  sequence of points
