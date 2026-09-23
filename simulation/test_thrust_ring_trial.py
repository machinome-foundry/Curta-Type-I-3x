"""Reuse the original support contracts against the actual fitted collar/ring."""

from simulation.test_thrust_seat_trial import ThrustSeatTest as _SeatContract
from simulation.thrust_ring_trial import FittedThrustBench


class FittedThrustSeatTest(_SeatContract):
    node = FittedThrustBench
