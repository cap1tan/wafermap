# Usage

To use Wafermap in a project

```python
    import wafermap
```

First let's define a Wafermap:
```python
wm = wafermap.WaferMap(wafer_radius=100e-3,             # all length dimensions in meters
                       cell_size=(10e-3, 20e-3),        # (sizeX, sizeY)
                       cell_margin=(8e-3, 15e-3),       # distance between cell borders (x, y)
                       grid_offset=(-2.05e-3, -4.1e-3), # grid offset in (x, y)
                       edge_exclusion=2.2e-3,           # margin from the wafer edge where a red edge exclusion ring is drawn
                       coverage='full',                 # 'full': will cover wafer with cells, partial cells allowed
                                                        # 'inner': only full cells allowed
                       notch_orientation=270)           # angle of notch in degrees. 270 corresponds to a notch at the bottom
```

To add an image at a specific cell/relative cell coordinates simply:
```python
wm.add_image(image_source_file="inspection1.jpg",
             cell=(1, 0),                               # (cell_index_x, cell_index_y)
             offset=(2.0e-3, 2.0e-3))                   # relative coordinate of the image within the cell
```

Adding vectors is just as easy. Just define cell and \[(start_rel_coordinates), (end_rel_coordinates)\]:
```python
vectors = [
            ((3, 0), [(0, 0), (1e-3, 1e-3)]),
            ((3, 0), [(1e-3, 0), (-5e-3, 5e-3)]),
            ((3, 0), [(0, 1e-3), (10e-3, -10e-3)]),
            ((3, 0), [(1e-3, 1e-3), (-20e-3, -20e-3)]),
            ]
colors = ['green', 'red', 'blue', 'black']
for color, (cell, vector) in zip(colors, vectors):
    wm.add_vector(vector_points=vector, cell=cell, vector_style={'color': color}, root_style={'radius': 1, 'color': color})
```

Let's throw in some points in a normal distribution for good measure too:
```python
# add 50 points per cell, in a random distribution
import random as rnd
cell_size = (10e-3, 20e-3)
cell_points = [(cell, [(rnd.gauss(cell_size[1]/2, cell_size[1]/6), rnd.gauss(cell_size[0]/2, cell_size[0]/6)) for _ in range(50)]) for cell in wm.cell_map.keys()]
for cell, cell_points_ in cell_points:
    for cell_point in cell_points_:
        wm.add_point(cell=cell, offset=cell_point)
```

Finally, nothing would matter if we couldn't see the result:
```python
# save to html
wm.save_html(f"wafermap.html")

# save to png (Mozilla must be installed)
wm.save_png(f"wafermap.png")
```
