"""Focused zero-gap bench, using the already fitted clearing assembly."""

from simulation.clearing_contact import ClearingContactBench


class ClearingGapBench(ClearingContactBench):
    """Same geometry; the companion contract probes the bilateral zero gap."""
