from pygame import Vector2, draw
from pygame.color import THECOLORS as COLORS
from pickle import loads, dumps, load, dump
from math import cos, sin, atan2, degrees, radians, inf


def load_geomodel(fpath):
    with open(fpath, mode="rb") as f:
        return load(f)


def save_geomodel(model, fpath):
    with open(fpath, mode="wb+") as f:
        dump(model, f)
        print("Saved model:", fpath)


class GeoModel:
    def __init__(self, center):
        self.points = []
        self.edges = []
        self.faces = []
        self.face_colors = []
        self.radials = []
        self.center = center
        self.center = Vector2(center)
        self.angle = 0

        self.face_points = []

    def dumps(self):
        return dumps(self)

    def loads(self, data_str):
        return loads(data_str)

    def add_point(self, point, index=None):
        if index:
            self.points.insert(index, point)
        else:
            self.points.append(Vector2(point))

        delta_x = point[0] - self.center.x
        delta_y = point[1] - self.center.y
        theta_radians = atan2(delta_y, delta_x)
        r = Vector2(point).distance_to(self.center)
        a = theta_radians
        self.add_point_radial(degrees(a), r)

    def add_points(self, points):
        for point in points:
            self.add_point(point)

    def set_point(self, index, point):
        # This method will set the location of a point identified by the index given. It will also update the radial.
        self.points[index] = Vector2(point)
        delta_x = point[0] - self.center.x
        delta_y = point[1] - self.center.y
        theta_radians = atan2(delta_y, delta_x)
        r = Vector2(point).distance_to(self.center)
        a = theta_radians
        self.radials[index] = [r, degrees(a)]

    def delete_point(self, index):
        if len(self.points) > 0:
            print("Attempting to delete point", index, f"({self.points[index]})")
            self.points.pop(index)
            self.radials.pop(index)

            bad_edges = []
            # Remove edges associated with the point we are deleting
            for i, edge in enumerate(self.edges):
                # If either point index in the edge contains the index for the deleted point
                # remove that edge as it is no longer valid
                if index in edge:
                    bad_edges.append(edge)

            for e in bad_edges:
                self.edges.remove(e)

            for edge in self.edges:
                if edge[0] > index:
                    edge[0] -= 1
                if edge[1] > index:
                    edge[1] -= 1

            # Remove faces associated with the point we are deleting
            bad_faces = []
            for face in self.faces:
                for point in face:
                    if point == index:
                        bad_faces.append(face)

            for f in bad_faces:
                self.face_colors.pop(self.faces.index(f))
                self.faces.remove(f)

            for face in self.faces:
                for i, p in enumerate(face):
                    if p > index:
                        face[i] -= 1

    def add_edge(self, p1_index, p2_index):
        if not [p1_index, p2_index] in self.edges and not [p2_index, p1_index] in self.edges:

            self.edges.append([p1_index, p2_index])

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge[0], edge[1])

    def add_face(self, indices, color=COLORS["gray"]):
        if len(indices) > 1:
            for face in self.faces:
                # If there is a face that exists which already contains all of the same points, return avoiding duplicates.
                if all(elem in face for elem in indices):
                    if not color == self.face_colors[self.faces.index(face)]:
                        self.add_edge(indices[-1], indices[0])
                        self.face_colors[self.faces.index(face)] = color
                    return

            for i, index in enumerate(indices):
                if i < len(indices) - 1:
                    self.add_edge(index, indices[i + 1])

            self.add_edge(indices[-1], indices[0])

            if len(indices) > 2:
                self.faces.append(indices)
                self.face_colors.append(color)

    def add_point_radial(self, angle, radius):
        self.radials.append([radius, angle])

    def scale(self, scale):
        for r in self.radials:
            r[0] *= scale

    def update_radials(self):
        for i, point in enumerate(self.points):
            delta_x = point[0] - self.center.x
            delta_y = point[1] - self.center.y
            theta_radians = atan2(delta_y, delta_x)
            r = Vector2(point).distance_to(self.center)
            a = degrees(theta_radians)
            self.radials[i] = [r, a]

    def get_xrange(self):
        minx = inf
        miny = inf
        for point in self.points:
            if point.x < minx:
                minx = point.x
            if point.y < miny:
                miny = point.y
        return minx, miny

    def update(self, dt):
        for i, point in enumerate(self.points):
            px = self.center[0] + self.radials[i][0] * cos(radians(self.angle + self.radials[i][1]))
            py = self.center[1] + self.radials[i][0] * sin(radians(self.angle + self.radials[i][1]))
            self.points[i] = Vector2(px, py)

    def draw(self, dest, offset=(0, 0), point_radius=0, draw_edges=False, draw_center=False):
        # Draw faces as polygons filled with the color defined for each face
        for face in self.faces:
            self.face_points = []
            for point_id in face:
                self.face_points.append(self.points[point_id] + offset)

            draw.polygon(dest, self.face_colors[self.faces.index(face)], self.face_points)

        if draw_edges:
            # Draw lines connecting each edge
            for i, edge in enumerate(self.edges):
                l = len(self.points)
                if edge[0] < l and edge[1] < l:
                    draw.aaline(dest, COLORS["blue"], self.points[edge[0]] + offset, self.points[edge[1]] + offset)

        if point_radius > 0:
            # Draw a circle on each point
            for point in self.points:
                draw.circle(dest, COLORS["red"], Vector2(point + offset), point_radius, 1)

        if draw_center:
            # Draw the center point
            draw.circle(dest, COLORS["black"], self.center + offset, 3)


class Polygon:
    def __init__(self, center):
        self.center = Vector2(center)
        self.points = []
        self.angle = 0
        self.radials = []

    def add_point_radial(self, angle, radius):
        px = self.center.x + radius * cos(radians(angle))
        py = self.center.y + radius * sin(radians(angle))
        self.points.append(Vector2(px, py))
        self.radials.append([radius, angle])

    def add_points(self, points):
        for point in points:
            delta_x = point[0] - self.center.x
            delta_y = point[1] - self.center.y
            theta_radians = atan2(delta_y, delta_x)
            r = Vector2(point).distance_to(self.center)
            a = theta_radians
            self.add_point_radial(degrees(a), r)

    def update(self, dt):
        for i, point in enumerate(self.points):
            px = self.center.x + self.radials[i][0] * cos(radians(self.angle + self.radials[i][1]))
            py = self.center.y + self.radials[i][0] * sin(radians(self.angle + self.radials[i][1]))
            self.points[i] = Vector2(px, py)

    def scale(self, scale):
        for r in self.radials:
            r[0] *= scale

    def draw(self, dest, color=COLORS["black"], offset=(0, 0), fill=0):
        if len(self.points) > 2:
            points = []
            for point in self.points:
                points.append(point + offset)
            draw.polygon(dest, color, points, fill)

        for point in self.points:
            pass#draw.circle(dest, COLORS["red"], point + offset, 2)

        #draw.circle(dest, COLORS["blue"], self.center + offset, 2)

