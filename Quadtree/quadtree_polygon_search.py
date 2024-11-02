import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point

class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary 
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point):
        if not self.contains_point(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            return (
                self.northeast.insert(point) or
                self.northwest.insert(point) or
                self.southeast.insert(point) or
                self.southwest.insert(point)
            )

    def contains_point(self, point):
        x, y = point
        return (
            self.boundary[0] <= x < self.boundary[0] + self.boundary[2] and
            self.boundary[1] <= y < self.boundary[1] + self.boundary[3]
        )

    def subdivide(self):
        x, y, w, h = self.boundary
        half_w, half_h = w / 2, h / 2

        self.northeast = Quadtree((x + half_w, y, half_w, half_h), self.capacity)
        self.northwest = Quadtree((x, y, half_w, half_h), self.capacity)
        self.southeast = Quadtree((x + half_w, y + half_h, half_w, half_h), self.capacity)
        self.southwest = Quadtree((x, y + half_h, half_w, half_h), self.capacity)
        
        self.divided = True

def search_quadtree_for_polygon(node, polygon, found_points=None):
    if found_points is None:
        found_points = []

    node_rect = Polygon([
        (node.boundary[0], node.boundary[1]),
        (node.boundary[0] + node.boundary[2], node.boundary[1]),
        (node.boundary[0] + node.boundary[2], node.boundary[1] + node.boundary[3]),
        (node.boundary[0], node.boundary[1] + node.boundary[3])
    ])
    if not polygon.intersects(node_rect):
        return found_points

    for point in node.points:
        if polygon.contains(Point(point)):
            found_points.append(point)

    if node.divided:
        search_quadtree_for_polygon(node.northeast, polygon, found_points)
        search_quadtree_for_polygon(node.northwest, polygon, found_points)
        search_quadtree_for_polygon(node.southeast, polygon, found_points)
        search_quadtree_for_polygon(node.southwest, polygon, found_points)

    return found_points

boundary = (0, 0, 100, 100)
capacity = 4
quadtree = Quadtree(boundary, capacity)

np.random.seed(0)
points = [(np.random.uniform(0, 100), np.random.uniform(0, 100)) for _ in range(20)]
for point in points:
    quadtree.insert(point)

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
plt.scatter(*zip(*points), color="blue", label="All Points")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Click to Define Polygon Vertices. Press Enter to Finish.")
plt.legend()

polygon_points = []

def onclick(event):
    if event.inaxes != ax:
        return
    polygon_points.append((event.xdata, event.ydata))
    plt.plot(*zip(*polygon_points), marker='o', color='green')
    plt.draw()

def onkey(event):
    if event.key == "enter" and len(polygon_points) > 2:
        polygon = Polygon(polygon_points)
        points_in_polygon = search_quadtree_for_polygon(quadtree, polygon)

        poly_x, poly_y = zip(*polygon_points, polygon_points[0])
        plt.plot(poly_x, poly_y, color="green", linestyle="-", linewidth=2, label="Polygon")

        if points_in_polygon:
            plt.scatter(*zip(*points_in_polygon), color="red", label="Points Inside Polygon")
        
        plt.title("Points Inside Polygon")
        plt.legend()
        plt.draw()

        print("Points inside polygon:", points_in_polygon)

cid_click = fig.canvas.mpl_connect('button_press_event', onclick)
cid_key = fig.canvas.mpl_connect('key_press_event', onkey)

plt.show()
