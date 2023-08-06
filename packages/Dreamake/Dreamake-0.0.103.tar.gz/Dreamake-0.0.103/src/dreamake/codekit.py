from pygame import image, Vector2, Rect
from pygame.color import THECOLORS as COLORS
from pygame import draw as pgdraw


def ints(values):
    intvals = []
    ltype = type(values)
    if ltype == list or ltype == tuple:
        for value in values:
            if type(value) == float or type(value) == int:
                intvals.append(int(value))
            else:
                return values
        intvals = ltype(intvals)
        return intvals
    else:
        return values


def clamp(value, minval, maxval):
    return max(minval, min(value, maxval))


def pad_rect(rect, x_padding=1, y_padding=1):
    rect = Rect(rect)
    rect.w += x_padding*2
    rect.h += y_padding*2
    return rect


def load_image(fpath):
    return image.load(fpath)


def draw_grid(dest, width, height, unit_size=16, offset=(0, 0), color=COLORS["gray"]):
    for x in range(width):
        pgdraw.line(dest, color, Vector2(offset) + (x*unit_size, 0), Vector2(offset) + (x*unit_size, height*unit_size))

    for y in range(height):
        pgdraw.line(dest, color, Vector2(offset) + (0, y*unit_size), Vector2(offset) + (width*unit_size, y*unit_size))


def find_nearest_point_on_line(point, start, end):
    end = Vector2(end)
    start = Vector2(start)
    line_direction = Vector2(end - start)
    line_length = line_direction.magnitude()
    if line_direction != [0, 0]:
        line_direction = line_direction.normalize()

    project_length = clamp(Vector2(point - start).dot(line_direction), 0, line_length)
    return start + line_direction * project_length