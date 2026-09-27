"""Native shaft datums on the already fitted transmission channels.

Each spindle names the channel's existing source-local turning line. Sliding
prints mate to that same shaft line through their original travel joints;
fitted shapes, translations, relations and coordinate names stay unchanged.
"""

from machinome.node import Frame
from machinome.motion.joints import Prismatic
from simulation import channel_slider_frames as sliders
from simulation.standard import channels
from simulation.higher_lockout_parts import ContactTens, ContactTensUpper
from simulation.counter_lockout_parts import ContactCounterOnes
from simulation.result_bank_lockout_parts import contact_result_channel, contact_result_upper
from simulation.counter_bank_lockout_parts import contact_counter_channel, contact_counter_upper
from simulation import reverser_inputs


class ResultOnes(channels.ResultOnes):
    spindle = Frame(at=channels.ResultOnes.turn.at)
    guide_seat = Frame(at=channels.ResultOnes.turn.at, z=(0, 0, -1))
    p_10219_410002_1 = sliders.ResultOnesInput(travel=Prismatic(axis=(0, 0, -1)))
    p_10221_1 = sliders.ResultOnesCarry(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10219_410002_1.guide.on(guide_seat, p_10219_410002_1.travel)
    carry_mount = p_10221_1.guide.on(guide_seat, p_10221_1.travel)


class ResultTens(ContactTens):
    spindle = Frame(at=channels.ResultTens.turn.at)
    guide_seat = Frame(at=channels.ResultTens.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419229 = sliders.ResultTensInput(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419227 = ContactTensUpper(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419229.guide.on(guide_seat, p_10230_410008_1_419229.travel)
    carry_mount = p_10220_410003_1_419227.guide.on(guide_seat, p_10220_410003_1_419227.travel)


class ResultHundreds(contact_result_channel(3)):
    spindle = Frame(at=channels.ResultHundreds.turn.at)
    guide_seat = Frame(at=channels.ResultHundreds.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419088 = sliders.ResultHundredsInput(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419086 = contact_result_upper(3)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419088.guide.on(guide_seat, p_10230_410008_1_419088.travel)
    carry_mount = p_10220_410003_1_419086.guide.on(guide_seat, p_10220_410003_1_419086.travel)


class ResultDigit4(contact_result_channel(4)):
    spindle = Frame(at=channels.ResultDigit4.turn.at)
    guide_seat = Frame(at=channels.ResultDigit4.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419232 = sliders.ResultDigit4Input(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419234 = contact_result_upper(4)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419232.guide.on(guide_seat, p_10230_410008_1_419232.travel)
    carry_mount = p_10220_410003_1_419234.guide.on(guide_seat, p_10220_410003_1_419234.travel)


class ResultDigit5(contact_result_channel(5)):
    spindle = Frame(at=channels.ResultDigit5.turn.at)
    guide_seat = Frame(at=channels.ResultDigit5.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419092 = sliders.ResultDigit5Input(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419093 = contact_result_upper(5)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419092.guide.on(guide_seat, p_10230_410008_1_419092.travel)
    carry_mount = p_10220_410003_1_419093.guide.on(guide_seat, p_10220_410003_1_419093.travel)


class ResultDigit6(contact_result_channel(6)):
    spindle = Frame(at=channels.ResultDigit6.turn.at)
    guide_seat = Frame(at=channels.ResultDigit6.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419066 = sliders.ResultDigit6Input(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419064 = contact_result_upper(6)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419066.guide.on(guide_seat, p_10230_410008_1_419066.travel)
    carry_mount = p_10220_410003_1_419064.guide.on(guide_seat, p_10220_410003_1_419064.travel)


class ResultDigit7(contact_result_channel(7)):
    spindle = Frame(at=channels.ResultDigit7.turn.at)
    guide_seat = Frame(at=channels.ResultDigit7.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419032 = sliders.ResultDigit7Input(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419039 = contact_result_upper(7)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419032.guide.on(guide_seat, p_10230_410008_1_419032.travel)
    carry_mount = p_10220_410003_1_419039.guide.on(guide_seat, p_10220_410003_1_419039.travel)


class ResultDigit8(contact_result_channel(8)):
    spindle = Frame(at=channels.ResultDigit8.turn.at)
    guide_seat = Frame(at=channels.ResultDigit8.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419075 = sliders.ResultDigit8Input(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419074 = contact_result_upper(8)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419075.guide.on(guide_seat, p_10230_410008_1_419075.travel)
    carry_mount = p_10220_410003_1_419074.guide.on(guide_seat, p_10220_410003_1_419074.travel)


class ResultDigit9(contact_result_channel(9)):
    spindle = Frame(at=channels.ResultDigit9.turn.at)
    guide_seat = Frame(at=channels.ResultDigit9.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419137 = sliders.ResultDigit9Input(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419139 = contact_result_upper(9)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419137.guide.on(guide_seat, p_10230_410008_1_419137.travel)
    carry_mount = p_10220_410003_1_419139.guide.on(guide_seat, p_10220_410003_1_419139.travel)


class ResultDigit10(contact_result_channel(10)):
    spindle = Frame(at=channels.ResultDigit10.turn.at)
    guide_seat = Frame(at=channels.ResultDigit10.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419118 = sliders.ResultDigit10Input(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419117 = contact_result_upper(10)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419118.guide.on(guide_seat, p_10230_410008_1_419118.travel)
    carry_mount = p_10220_410003_1_419117.guide.on(guide_seat, p_10220_410003_1_419117.travel)


class ResultDigit11(contact_result_channel(11)):
    spindle = Frame(at=channels.ResultDigit11.turn.at)
    guide_seat = Frame(at=channels.ResultDigit11.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419111 = sliders.ResultDigit11Input(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419114 = contact_result_upper(11)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419111.guide.on(guide_seat, p_10230_410008_1_419111.travel)
    carry_mount = p_10220_410003_1_419114.guide.on(guide_seat, p_10220_410003_1_419114.travel)


class TurnsOnes(ContactCounterOnes):
    spindle = Frame(at=channels.TurnsOnes.turn.at)


class TurnsTens(contact_counter_channel(2)):
    spindle = Frame(at=channels.TurnsTens.turn.at)
    guide_seat = Frame(at=channels.TurnsTens.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419080 = reverser_inputs.TensInput(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419081 = contact_counter_upper(2)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419080.guide.on(guide_seat, p_10230_410008_1_419080.travel)
    carry_mount = p_10220_410003_1_419081.guide.on(guide_seat, p_10220_410003_1_419081.travel)


class TurnsHundreds(contact_counter_channel(3)):
    spindle = Frame(at=channels.TurnsHundreds.turn.at)
    guide_seat = Frame(at=channels.TurnsHundreds.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419068 = reverser_inputs.HundredsInput(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419070 = contact_counter_upper(3)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419068.guide.on(guide_seat, p_10230_410008_1_419068.travel)
    carry_mount = p_10220_410003_1_419070.guide.on(guide_seat, p_10220_410003_1_419070.travel)


class TurnsDigit4(contact_counter_channel(4)):
    spindle = Frame(at=channels.TurnsDigit4.turn.at)
    guide_seat = Frame(at=channels.TurnsDigit4.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419182 = reverser_inputs.FourthInput(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419181 = contact_counter_upper(4)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419182.guide.on(guide_seat, p_10230_410008_1_419182.travel)
    carry_mount = p_10220_410003_1_419181.guide.on(guide_seat, p_10220_410003_1_419181.travel)


class TurnsDigit5(contact_counter_channel(5)):
    spindle = Frame(at=channels.TurnsDigit5.turn.at)
    guide_seat = Frame(at=channels.TurnsDigit5.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419105 = reverser_inputs.FifthInput(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419107 = contact_counter_upper(5)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419105.guide.on(guide_seat, p_10230_410008_1_419105.travel)
    carry_mount = p_10220_410003_1_419107.guide.on(guide_seat, p_10220_410003_1_419107.travel)


class TurnsDigit6(contact_counter_channel(6)):
    spindle = Frame(at=channels.TurnsDigit6.turn.at)
    guide_seat = Frame(at=channels.TurnsDigit6.turn.at, z=(0, 0, -1))
    p_10230_410008_1_419237 = reverser_inputs.SixthInput(travel=Prismatic(axis=(0, 0, -1)))
    p_10220_410003_1_419238 = contact_counter_upper(6)(travel=Prismatic(axis=(0, 0, -1)))
    input_mount = p_10230_410008_1_419237.guide.on(guide_seat, p_10230_410008_1_419237.travel)
    carry_mount = p_10220_410003_1_419238.guide.on(guide_seat, p_10220_410003_1_419238.travel)
