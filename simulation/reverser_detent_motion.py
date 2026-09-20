"""Radial follower of the unchanged two conical pockets, not a force solver."""

from math import radians, sin, cos, tan
from machinome.math import abs, min, max, sqrt

BALL_RADIUS = 2.7  # measured CAD sphere; do not silently substitute nominal 5 mm
SHAFT_RADIUS = 3.693
CONE_APEX = .81
CONE_ANGLE = radians(63)
POCKETS = (78.6, 90.6)
SEAT_GAP = .05
SOURCE_BALL_RADIUS = 5.5310689635676225
SOURCE_BALL_Z = 85.4425

WIRE_RADIUS = .255
COIL_RADIUS = 2.295
COIL_TURNS = 6.5
FREE_HEIGHT = 11.1
SPRING_BACK = 16.7  # knob's blind bore end, measured from shaft axis


def ball_radius_at(z):
    distance = min(abs(z - POCKETS[0]), abs(z - POCKETS[1]))
    radius = BALL_RADIUS + SEAT_GAP
    # In the cone, the sphere-to-wall normal distance is its radius. At the
    # shaft surface the cone ends: the follower rolls over that rim, then
    # follows the cylinder. The two formulae share value and slope at tangent.
    rim_height = (SHAFT_RADIUS - CONE_APEX) * tan(CONE_ANGLE)
    tangent_height = rim_height - radius*cos(CONE_ANGLE)
    cone = CONE_APEX + radius/sin(CONE_ANGLE) + min(distance, tangent_height)/tan(CONE_ANGLE)
    rim = sqrt(radius**2 - max(0, rim_height - max(distance, tangent_height))**2)
    return cone + rim - radius*sin(CONE_ANGLE)


def spring_height(ball_radius):
    # Distance from ball centre to the inner coil centre. The helix wire is
    # bounded by a tube of WIRE_RADIUS, giving the named ball/wire separation.
    front = ball_radius + sqrt((BALL_RADIUS + WIRE_RADIUS + SEAT_GAP)**2 - COIL_RADIUS**2)
    return SPRING_BACK - WIRE_RADIUS - SEAT_GAP - front
