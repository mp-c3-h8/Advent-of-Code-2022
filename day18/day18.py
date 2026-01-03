import os.path
from collections import deque
from typing import Iterator
from timeit import default_timer as timer


type Coord = tuple[int, int, int]  # (x,y,z)
type Component = set[Coord]  # connected, not scattered


class Droplet:
    def __init__(self, data: str) -> None:
        self.coords: Component = self.create_droplet(data)
        self.surface: int = self.calc_surface(self.coords)
        bounds_min, bounds_max = self.calc_bounds(self.coords)
        self.bounds_min: Coord = bounds_min
        self.bounds_max: Coord = bounds_max
        self.exterior: Component = self.calc_exterior()
        self.holes: list[Component] = self.calc_holes()
        self.surface_interior: int = self.calc_surface_interior()

    def create_droplet(self, data: str) -> Component:
        coords: Component = set()
        for line in data.splitlines():
            x, y, z = tuple(map(int, line.split(",")))
            coords.add((x, y, z))
        return coords

    def calc_surface(self, comp: Component) -> int:
        return sum((6 - sum(n in comp for n in self.neighbors(coord))) for coord in comp)

    def calc_surface_interior(self) -> int:
        return sum(self.calc_surface(comp) for comp in self.holes)

    def calc_bounds(self, comp: Component) -> tuple[Coord, Coord]:
        # bounding box lies outside of droplet
        x_max, y_max, z_max = map(max, ((c[i] for c in comp) for i in range(3)))
        x_min, y_min, z_min = map(min, ((c[i] for c in comp) for i in range(3)))
        return (x_min-1, y_min-1, z_min-1), (x_max+1, y_max+1, z_max+1)

    def flood_fill(self, start: Coord) -> Component:
        component: Component = set()
        q: deque[Coord] = deque([start])

        while q:
            coord = q.pop()
            component.add(coord)
            for n in self.neighbors(coord):
                if self.inbound(n) and n not in component and n not in self.coords:
                    q.append(n)
        return component

    def calc_exterior(self) -> Component:
        return self.flood_fill(self.bounds_max)

    def calc_holes(self) -> list[Component]:
        components: list[Component] = []

        for coord in self.interior_iterator():
            if coord in self.coords or coord in self.exterior:
                continue
            if any(coord in comp for comp in components):
                continue
            component = self.flood_fill(coord)
            components.append(component)

        return components

    def neighbors(self, coord: Coord) -> Iterator:
        return (coord[:i] + (x+d,) + coord[i+1:] for i, x in enumerate(coord) for d in (1, -1))

    def interior_iterator(self) -> Iterator[Coord]:
        x_min, y_min, z_min = self.bounds_min
        x_max, y_max, z_max = self.bounds_max
        for x in range(x_min+1, x_max):
            for y in range(y_min+1, y_max):
                for z in range(z_min+1, z_max):
                    yield (x, y, z)

    def inbound(self, coord: Coord) -> bool:
        in_min = all(coord[i] >= self.bounds_min[i] for i in range(3))
        in_max = all(coord[i] <= self.bounds_max[i] for i in range(3))
        return in_min and in_max

start = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

droplet = Droplet(data)
print("Part 1:", droplet.surface)
print("Part 2:", droplet.surface - droplet.surface_interior)

end = timer()
print(end - start)
