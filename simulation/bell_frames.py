"""Rigid mounting for the whole retaining spring; its hooks still deform."""

from machinome.node import Frame
from simulation.mechanism import TensBellAssembly
from simulation.retaining_spring import RetainingSpring, MOUNT_Z


class FramedRetainingSpring(RetainingSpring):
    datum = Frame()


class FramedTensBellAssembly(TensBellAssembly):
    spring_seat = Frame(at=(0, 0, MOUNT_Z))
    tens_bell_spring = FramedRetainingSpring()
    spring_mount = tens_bell_spring.datum.on(spring_seat)

    def render(self):
        self.tens_bell_c_clip.translate((0, 0, 63.6))
        self.retaining_ring_for_tens_bell.translate((0, 0, 61.8))
        self.m4x10_419159_1.rotate(180, (1, 0, 0)).translate((-10.5, 0, -2.7))
        self.m4x10_419159_2.rotate(180, (1, 0, 0)).translate((10.5, 0, -2.7))
