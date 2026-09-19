"""Prove one tapered source finger before repeating it over the registers."""

from machinome.node import AssemblyNode
from machinome.simulation import Driver
from simulation.spider import OneFingerMount, SpiderFinger


class SpiderShapeBench(AssemblyNode):
    rise = Driver(default=0, range=(0, 3), unit='mm')
    mount = OneFingerMount()
    finger = SpiderFinger()
    rise.drives(finger.rise)
