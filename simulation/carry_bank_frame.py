"""Independent full-bank stroke fixture; operating parts and source placements."""

from machinome.node import AssemblyNode
from machinome.simulation import Driver
from simulation.mechanism import UpperFrame
from simulation.standard.carry import ResultsCarry, TurnsCarry
from simulation.carry_bank_fits import CarryBankPassageFrame
from simulation.frame_fits import CarryPassageFrame


class CarryBankFrameBench(AssemblyNode):
    drop_mm = Driver(default=0, range=(0, 4.2), unit='mm')
    frame = UpperFrame()
    result_carries = ResultsCarry()
    turns_carries = TurnsCarry()
    drop_mm.drives(result_carries.results_tens_lever_assembly_1.engage, ratio=1/4.2)
    drop_mm.drives(result_carries.results_tens_lever_assembly_2.engage, ratio=1/4.2)
    drop_mm.drives(result_carries.results_tens_lever_assembly_3.engage, ratio=1/4.2)
    drop_mm.drives(result_carries.results_tens_lever_assembly_4.engage, ratio=1/4.2)
    drop_mm.drives(result_carries.results_tens_lever_assembly_5.engage, ratio=1/4.2)
    drop_mm.drives(result_carries.results_tens_lever_assembly_6.engage, ratio=1/4.2)
    drop_mm.drives(result_carries.results_tens_lever_assembly_7.engage, ratio=1/4.2)
    drop_mm.drives(result_carries.results_tens_lever_assembly_8.engage, ratio=1/4.2)
    drop_mm.drives(result_carries.results_tens_lever_assembly_9.engage, ratio=1/4.2)
    drop_mm.drives(result_carries.results_tens_lever_assembly_10.engage, ratio=1/4.2)
    drop_mm.drives(turns_carries.turns_tens_lever_assembly_1.engage, ratio=1/4.2)
    drop_mm.drives(turns_carries.turns_tens_lever_assembly_2.engage, ratio=1/4.2)
    drop_mm.drives(turns_carries.turns_tens_lever_assembly_3.engage, ratio=1/4.2)
    drop_mm.drives(turns_carries.turns_tens_lever_assembly_4.engage, ratio=1/4.2)
    drop_mm.drives(turns_carries.turns_tens_lever_assembly_5.engage, ratio=1/4.2)


def stations(root):
    for group, prefix, count, slider in (
            ('result_carries', 'results_tens_lever_assembly_', 10, 'tens_slider_for_results'),
            ('turns_carries', 'turns_tens_lever_assembly_', 5, 'tens_slider_for_turns_counter')):
        for index in range(1, count+1):
            path = group+'.'+prefix+str(index)
            node = getattr(getattr(root, group), prefix+str(index))
            yield path, node, slider


class FittedUpperFrame(UpperFrame):
    main_body = CarryBankPassageFrame()


class FirstPairUpperFrame(UpperFrame):
    """Preserved two-station baseline, independent of future root adoption."""
    main_body = CarryPassageFrame()


class FirstPairCarryBankFrameBench(CarryBankFrameBench):
    frame = FirstPairUpperFrame()


class FittedCarryBankFrameBench(CarryBankFrameBench):
    """Isolated candidate; the production operating root is not changed."""
    frame = FittedUpperFrame()
