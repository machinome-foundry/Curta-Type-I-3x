"""Independent maximum underside region, in installed zero-lift coordinates.

This is acceptance geometry only, never a production cutter. Rounded limits
are declared in clear-radial-ball-thrust-ring before constructing its fit.
"""

import cadquery as cq
import manifold3d


def permitted_world():
    return cq.Solid.makeBox(2.3, 4.8, .8, (12, -2.4, 33.05))


def permitted_faceted():
    return manifold3d.Manifold.cube((2.3, 4.8, .8)).translate((12, -2.4, 33.05))


def permitted_local():
    return permitted_world().translate((0, 0, -33.05)).rotate(
        (0, 0, 0), (0, 0, 1), -35.717779468)
