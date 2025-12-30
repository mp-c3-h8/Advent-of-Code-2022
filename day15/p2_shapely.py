import os.path
import re
import shapely
from shapely.geometry import Polygon
from shapely import prepare
from shapely.plotting import plot_polygon
import matplotlib.pyplot as plt


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

with open(input_path) as f:
    data = f.read().splitlines()

regex = re.compile(r"-?\d+")
polygons = []
for line in data:
    sx, sy, bx, by = map(int, regex.findall(line))
    dist = abs(sx-bx) + abs(sy-by)  # manhatten
    a = (sx+dist, sy)
    b = (sx, sy+dist)
    c = (sx-dist, sy)
    d = (sx, sy-dist)
    polygon = (a, b, c, d)
    poly = Polygon(polygon)
    prepare(poly)
    polygons.append(poly)


union = shapely.union_all(polygons)
assert (type(union) == Polygon)
inner = union.interiors
assert (len(inner) == 1)
inner = inner[0]
xmin = min(x for x, y in inner.coords)
xmax = max(x for x, y in inner.coords)
ymin = min(y for x, y in inner.coords)
ymax = max(y for x, y in inner.coords)
beacon = (int((xmin+xmax)/2), int((ymin+ymax)/2))

print("Beacon Position:",beacon)
print("Part 2:", 4000000 * beacon[0] + beacon[1])
plot_polygon(union)
plt.show()
