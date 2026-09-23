"""Rerun existing spring and working-interface contracts on the trial."""

from simulation import test_carry_contact as contacts
from simulation.counter_shoulder_contacts import CounterShoulderContactBench


class CounterShoulderContactTest(contacts.CarryContactTest):
    node = CounterShoulderContactBench
