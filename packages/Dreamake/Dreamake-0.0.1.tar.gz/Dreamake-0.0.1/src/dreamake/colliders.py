from pygame import Vector2, Vector3, Rect, draw
from pygame.color import THECOLORS as COLORS
from math import atan2, cos, sin

# The syntax for our collision functions follows this convention
# collide_<shape1>_<shape2>_<response>


class Collider:
    def __init__(self, position=(0, 0)):
        self.position = Vector2(position)

    def draw_debug(self, dest):
        pass


class CircleCollider(Collider):
    def __init__(self, position, radius):
        super().__init__(position)
        self.radius = radius

    def draw_debug(self, dest, offset=(0, 0), color=COLORS["black"], bordersize=0):
        offset = Vector2(offset)
        draw.circle(dest, color, self.position + offset, self.radius, 0)
        draw.circle(dest, (255, 255, 255), self.position + offset, self.radius, 4)
        draw.circle(dest, (0, 0, 0), self.position + offset, self.radius, 1)


class AABBCollider(Collider):
    def __init__(self, rect):
        self.rect = Rect(rect)
        super().__init__(self.rect.topleft)

    def draw_debug(self, dest, offset=(0, 0)):
        offset = Vector2(offset)
        draw.rect(dest, COLORS["red"], self.rect, 1)


def collide_circle_circle(c1, c2):
    # Get the distance between the circles
    d = c1.position.distance_to(c2.position)
    rsum = c1.radius + c2.radius

    # If the distance is less than the sum of both radii, there is a collision
    if d < rsum:
        return True
    return False


def collide_circle_circle_dynamic(c1, c2):
    # Get the distance between the circles
    d = c1.position.distance_to(c2.position)
    rsum = c1.radius + c2.radius

    # If the distance is less than the sum of both radii, there is a collision
    if d < rsum:
        # Perform collision response
        o = rsum - d  # The amount of distance by which the circles overlap
        a = atan2(c2.position.y - c1.position.y, c2.position.x - c1.position.x)  # The angle between the circles
        c2.position.x += o*0.5 * cos(a)
        c2.position.y += o*0.5 * sin(a)
        c1.position.x -= o*0.5 * cos(a)
        c1.position.y -= o*0.5 * sin(a)

        collision_data = (o, a)
        return collision_data
    return None


def collide_circle_circle_static(c1, c2):
    # Get the distance between the circles
    d = c1.position.distance_to(c2.position)
    rsum = c1.radius + c2.radius

    # If the distance is less than the sum of both radii, there is a collision
    if d < rsum:
        # Perform collision response
        o = rsum - d  # The amount of distance by which the circles overlap
        a = atan2(c2.position.y - c1.position.y, c2.position.x - c1.position.x)  # The angle between the circles
        c1.position.x -= o * cos(a)
        c1.position.y -= o * sin(a)

        collision_data = (o, a)
        return collision_data
    return None
