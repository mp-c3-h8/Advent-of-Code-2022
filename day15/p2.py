import os.path
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import shapely
from shapely.geometry import Polygon, mapping
from itertools import combinations
from shapely import prepare


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

with open(input_path) as f:
    data = f.read().splitlines()

regex = re.compile(r"-?\d+")
plt.figure(0)
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
    polygons.append(Polygon(polygon))
    # ax.add_patch(mpatches.Polygon(polygon))
    plt.plot((sx+dist, sx, sx-dist, sx, sx+dist), (sy, sy+dist, sy, sy-dist, sy))

intersections = set()
for s1, s2 in combinations(polygons, 2):
    inter = shapely.intersection(s1, s2)
    if inter and inter.geom_type == "Polygon":
        intersections.update(inter.exterior.coords)

inter = list(intersections)

plt.xlim(0, 4000000)
plt.ylim(0, 4000000)

plt.figure(1)
plt.scatter([x for x, y in inter], [y for x, y in inter])
plt.show()
