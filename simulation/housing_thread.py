"""Isolate the two installed source-print covers and their threaded seat."""

from simulation.mechanism import CarriageCovers
from simulation.cover_fits import FittedUpperHousing
from simulation.colors import ALUMINUM


class HousingThreadBench(CarriageCovers):
    pass


class HousingThreadInspection(FittedUpperHousing):
    """Unchanged fitted geometry, light inspection colour only."""
    color = ALUMINUM
