# Wafermap


<p align="center">
<a href="https://pypi.python.org/pypi/wafermap">
    <img src="https://img.shields.io/pypi/v/wafermap.svg"
        alt = "Release Status">
</a>

<a href="https://github.com/cap1tan/wafermap/actions">
    <img src="https://github.com/cap1tan/wafermap/actions/workflows/release.yml/badge.svg?branch=release" alt="CI Status">
</a>

<!-- <a href="https://wafermap.readthedocs.io/en/latest/?badge=latest">
    <img src="https://readthedocs.org/projects/wafermap/badge/?version=latest" alt="Documentation Status">
</a> -->

</p>


A python package to plot maps of semiconductor wafers.


* Free software: MIT
* Documentation: <https://cap1tan.github.io/wafermap/>


## Features

* Circular wafers with arbitrary notch orientations.
* Edge-exclusion and grids with optional margin.
* Hover-able points, vectors and images.
* Tooltips with embeddable images.
* Export zoom-able maps to HTML.
* Toggle layers on/off individually.
* Export to png with selenium, geckodriver and Mozilla


## Examples

[HTML](examples/test_wafermap_example.html)

![Example_wafermap](examples/test_wafermap_example.png)



## Usage

```python
import wafermap
import random as rnd

# define the wafermap
wm = wafermap.WaferMap(wafer_radius=100e-3,             # all length dimensions in meters
                       cell_size=(10e-3, 20e-3),        # (sizeX, sizeY)
                       cell_margin=(8e-3, 15e-3),       # distance between cell borders (x, y)
                       grid_offset=(-2.05e-3, -4.1e-3), # grid offset in (x, y)
                       edge_exclusion=2.2e-3,           # margin from the wafer edge where a red edge exclusion ring is drawn
                       coverage='full',                 # 'full': will cover wafer with cells, partial cells allowed
                                                        # 'inner': only full cells allowed
                       notch_orientation=270)           # angle of notch in degrees. 270 corresponds to a notch at the bottom

# add an image
wm.add_image(image_source_file="inspection1.jpg",
             cell=(1, 0),                               # (cell_index_x, cell_index_y)
             offset=(2.0e-3, 2.0e-3))                   # relative coordinate of the image within the cell

# add vectors
vectors = [
            ((3, 0), [(0, 0), (1e-3, 1e-3)]),
            ((3, 0), [(1e-3, 0), (-5e-3, 5e-3)]),
            ((3, 0), [(0, 1e-3), (10e-3, -10e-3)]),
            ((3, 0), [(1e-3, 1e-3), (-20e-3, -20e-3)]),
            ]
colors = ['green', 'red', 'blue', 'black']
for color, (cell, vector) in zip(colors, vectors):
    wm.add_vector(vector_points=vector, cell=cell, vector_style={'color': color}, root_style={'radius': 1, 'color': color})

# add 50 points per cell, in a random distribution
cell_size = (10e-3, 20e-3)
cell_points = [(cell, [(rnd.gauss(cell_size[1]/2, cell_size[1]/6), rnd.gauss(cell_size[0]/2, cell_size[0]/6)) for _ in range(50)]) for cell in wm.cell_map.keys()]
for cell, cell_points_ in cell_points:
    for cell_point in cell_points_:
        wm.add_point(cell=cell, offset=cell_point)

# save to html
wm.save_html(f"wafermap.html")

# save to png (Mozilla must be installed)
wm.save_png(f"wafermap.png")
```

## Dependencies

- Folium
- branca
- Pillow
- Optional for exporting to .png images: selenium, geckodriver and Mozilla browser installed.
