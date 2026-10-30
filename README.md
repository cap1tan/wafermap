# Wafermap

[
![pypi](https://img.shields.io/pypi/v/wafermap.svg)
![pypi](https://img.shields.io/pypi/pyversions/wafermap.svg)
![pypi](https://img.shields.io/github/license/cap1tan/wafermap.svg)
](https://pypi.org/project/wafermap/)
[
![GitHub](https://img.shields.io/github/v/release/cap1tan/wafermap?include_prereleases)
![GitHub](https://img.shields.io/github/languages/code-size/cap1tan/wafermap)
](https://github.com/cap1tan/wafermap)



A python package to plot maps of semiconductor wafers.

Free software: MIT license


## Features

* Circular wafers with arbitrary notch orientations and full or inner layouts.
* Grid with adjustable offset and origin, cells with adjustable size and margin.
* Edge-exclusion.
* Hover-able points, vectors and images.
* Tooltips with embeddable images.
* Individual labels and colors for each die.
* Toggle layers on/off individually.
* Export zoom-able maps to HTML.
* Heatmaps of measurement data.
* Export PNG images (needs the `png` extra and Chrome or Edge)


## Examples

- See the full dynamic maps [here](https://cap1tan.github.io/wafermap/)!

- Static png image, just to get a taste:

![Example_wafermap](docs/test_wafermap_example.png)


## Installation

To install Wafermap, run this command in your
terminal:

``` console
$ pip install wafermap
```

This is the preferred method to install Wafermap, as it will always install the most recent stable release.

To also export PNG images, install the `png` extra (Chrome or Edge must be installed too):

``` console
$ pip install wafermap[png]
```

If you don't have [pip][] installed, this [Python installation guide][]
can guide you through the process.

### From source

The source for Wafermap can be downloaded from
the [Github repo][].

You can clone the public repository:

``` console
$ git clone git://github.com/cap1tan/wafermap
```


  [pip]: https://pip.pypa.io
  [Python installation guide]: http://docs.python-guide.org/en/latest/starting/installation/
  [Github repo]: https://github.com/cap1tan/wafermap


## Usage

To use Wafermap in a project

```python
    import wafermap
```

First let's define a Wafermap:
```python
wm = wafermap.WaferMap(wafer_radius=100,                # all length dimensions in mm
                       cell_size=(10, 20),              # (sizeX, sizeY)
                       cell_margin=(8, 15),             # distance between cell borders (x, y)
                       cell_origin=(0, 0),              # which cell to select as origin (0, 0), in (x, y)
                       grid_offset=(-2.05, -4.1),       # grid offset in (x, y)
                       edge_exclusion=2.2,              # margin from the wafer edge where a red edge exclusion ring is drawn
                       coverage='full',                 # 'full': will cover wafer with cells, partial cells allowed
                                                        # 'inner': only full cells allowed
                       notch_orientation=270)           # angle of notch in degrees. 270 corresponds to a notch at the bottom
```

To add an image at a specific cell/relative cell coordinates simply:
```python
wm.add_image(image_source_file="inspection1.jpg",
             cell=(1, 0),                               # (cell_index_x, cell_index_y)
             offset=(2.0, 2.0))                         # relative coordinate of the image within the cell
```

Adding vectors is just as easy. Just define cell and \[(start_rel_coordinates), (end_rel_coordinates)\]:
```python
vectors = [
            ((3, 0), [(0, 0), (1, 1)]),
            ((3, 0), [(1, 0), (-5, 5)]),
            ((3, 0), [(0, 1), (10, -10)]),
            ((3, 0), [(1, 1), (-20, -20)]),
            ]
colors = ['green', 'red', 'blue', 'black']
for color, (cell, vector) in zip(colors, vectors):
    wm.add_vector(vector_points=vector, cell=cell, vector_style={'color': color}, root_style={'radius': 1, 'color': color})
```

Let's throw in some points in a normal distribution for good measure too:

```python
# add 50 points per cell, in a random distribution
import random as rnd

cell_size = (10, 20)
cell_points = [(cell, [(rnd.gauss(cell_size[0] / 2, cell_size[0] / 6),
                        rnd.gauss(cell_size[1] / 2, cell_size[1] / 6)) for _ in
                       range(50)]) for cell in wm]
for cell, cell_points_ in cell_points:
    for cell_point in cell_points_:
        wm.add_point(cell=cell, offset=cell_point)
```

Labels, cell colors and heatmaps work the same way:

```python
wm.add_label(cell=(2, 0), offset=(5, 10), label_text="PASS")
wm.style_cell(cell=(2, 0), cell_style={"fill": True, "fillColor": "green", "fillOpacity": 0.5})

# list of (wafer_x, wafer_y, value), or a dict {(cell_x, cell_y, offset_x, offset_y): value}
wm.add_heatmap([(rnd.gauss(0, 25), rnd.gauss(0, 25), 1.0) for _ in range(500)])
```

Instead of a regular grid, the cells can also be given explicitly, as
`(wafer_x, wafer_y, cell_x, cell_y)` with `(wafer_x, wafer_y)` the lower left corner of each cell:

```python
wm = wafermap.WaferMap(wafer_radius=150, cell_size=(5, 10),
                       cells=[(-5, -10, 0, 0), (0, -10, 1, 0), (-5, 0, 0, 1)])
```

Finally, nothing would matter if we couldn't see the result:
```python
# save to html
wm.save_html(f"wafermap.html")

# save to png (needs `pip install wafermap[png]` and Chrome or Edge)
wm.save_png(f"wafermap.png")
```


## Dependencies

- __Folium__ -> to make dynamic, zoom-able and pan-able HTML based maps
- __Pillow__ -> to support embedded images and format the optional image output
- __html2image__ (optional, `png` extra) & __Chrome__ or __Edge__ -> exporting to .png images


## Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

### Types of Contributions

#### Report Bugs

Report bugs at https://github.com/cap1tan/wafermap/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

#### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

#### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

#### Write Documentation

Wafermap could always use more documentation, whether as part of the
official Wafermap docs, in docstrings, or even on the web in blog posts,
articles, and such.

#### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/cap1tan/wafermap/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

### Get Started!

Ready to contribute? Here's how to set up `wafermap` for local development.

1. Fork the `wafermap` repo on GitHub.
2. Clone your fork locally

```
    $ git clone git@github.com:your_name_here/wafermap.git
```

3. Ensure [poetry](https://python-poetry.org/docs/) is installed.
4. Install dependencies and start your virtualenv:

```
    $ poetry install -E test
```

5. Create a branch for local development:

```
    $ git checkout -b name-of-your-bugfix-or-feature
```

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass the
   tests, including testing other Python versions, with tox:

```
    $ tox
```

7. Commit your changes and push your branch to GitHub:

```
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
```

8. Submit a pull request through the GitHub website.

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.
3. The pull request should work for Python 3.10 - 3.14. Check
   https://github.com/cap1tan/wafermap/actions
   and make sure that the tests pass for all supported Python versions.

### Tips
```
    $ python -m unittest tests.test_wafermap
```
To run a subset of tests.


### Deploying

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.md).
Then run:

```
$ poetry patch # possible: major / minor / patch
$ git push
$ git push --tags
```

Github Actions will then deploy to PyPI if tests pass.
