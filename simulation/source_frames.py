"""Project-local conversion of recorded CAD poses to explicit frame triads."""

from math import cos, sin, radians, sqrt
from machinome.node import Frame


def source_frame(*, at, angle, axis):
    """Express one recorded source rotation/translation as a full frame."""
    length = sqrt(sum(value * value for value in axis))
    unit = tuple(value / length for value in axis)
    cosine, sine = cos(radians(angle)), sin(radians(angle))

    def rotate(vector):
        x, y, z = unit
        a, b, c = vector
        cross = (y * c - z * b, z * a - x * c, x * b - y * a)
        dot = sum(u * v for u, v in zip(unit, vector))
        return tuple(v * cosine + w * sine + u * dot * (1 - cosine)
                     for v, w, u in zip(vector, cross, unit))

    return Frame(at=at, x=rotate((1, 0, 0)), z=rotate((0, 0, 1)))

