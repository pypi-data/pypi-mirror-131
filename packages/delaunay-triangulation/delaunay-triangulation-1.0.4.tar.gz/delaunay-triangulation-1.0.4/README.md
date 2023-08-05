# Installing
### Python 3.6 or higher is required
other than that it's just as simple as
```
pip install delaunay-triangulation
```

# Features
## Geometry Math Classes - typing.py
### StandardLine
A line in a coordinate grid described in standard form (ax + by = c).

### Coordinate
A single x or y coordinate that doesn't have a specific value yet.

### Vertex
A Vertex - a point in 2D space described by an x and y value.

### Edge
An Edge - a line(AB) in 2D space described by 2 vertices

### Triangle
A Triangle represented as 3 vertices a, b, c

### Circle
A Circle described by its center and its radius

## Calculation Methods - triangulation.py
### scatter_vertices
helper method to scatter random vertices on a specified plane.

### get_super_triangle
get super triangle from vertices

### delaunay
the crux of this package. A method to Delaunay Triangulate a list of vertices using the Bowyer-Watson algorithm.

# Basic usage
```python
from delaunay_triangulation.triangulate import scatter_vertices, delaunay

width = 1920
height = 1080
spacing = 250
scatter = 0.75

vertices = scatter_vertices(
    plane_width=width,
    plane_height=height,
    spacing=spacing,
    scatter=scatter
)

# delete_super_shared is True by default but can be turned off if you need to fill a plane completely
triangles = delaunay(
    vertices=vertices,
    delete_super_shared=False
)
```
You are now free to do with those triangles what ever you may desire!