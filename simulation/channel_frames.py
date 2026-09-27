"""Native shaft datums on the already fitted transmission channels.

These adapters add no geometry or motion. Each spindle names the channel's
existing source-local turning line; fitted child shapes and translations stay
inside the original channel.
"""

from machinome.node import Frame
from simulation.standard import channels
from simulation.higher_lockout_parts import ContactTens
from simulation.counter_lockout_parts import ContactCounterOnes
from simulation.result_bank_lockout_parts import contact_result_channel
from simulation.counter_bank_lockout_parts import contact_counter_channel


class ResultOnes(channels.ResultOnes):
    spindle = Frame(at=channels.ResultOnes.turn.at)


class ResultTens(ContactTens):
    spindle = Frame(at=channels.ResultTens.turn.at)


class ResultHundreds(contact_result_channel(3)):
    spindle = Frame(at=channels.ResultHundreds.turn.at)


class ResultDigit4(contact_result_channel(4)):
    spindle = Frame(at=channels.ResultDigit4.turn.at)


class ResultDigit5(contact_result_channel(5)):
    spindle = Frame(at=channels.ResultDigit5.turn.at)


class ResultDigit6(contact_result_channel(6)):
    spindle = Frame(at=channels.ResultDigit6.turn.at)


class ResultDigit7(contact_result_channel(7)):
    spindle = Frame(at=channels.ResultDigit7.turn.at)


class ResultDigit8(contact_result_channel(8)):
    spindle = Frame(at=channels.ResultDigit8.turn.at)


class ResultDigit9(contact_result_channel(9)):
    spindle = Frame(at=channels.ResultDigit9.turn.at)


class ResultDigit10(contact_result_channel(10)):
    spindle = Frame(at=channels.ResultDigit10.turn.at)


class ResultDigit11(contact_result_channel(11)):
    spindle = Frame(at=channels.ResultDigit11.turn.at)


class TurnsOnes(ContactCounterOnes):
    spindle = Frame(at=channels.TurnsOnes.turn.at)


class TurnsTens(contact_counter_channel(2)):
    spindle = Frame(at=channels.TurnsTens.turn.at)


class TurnsHundreds(contact_counter_channel(3)):
    spindle = Frame(at=channels.TurnsHundreds.turn.at)


class TurnsDigit4(contact_counter_channel(4)):
    spindle = Frame(at=channels.TurnsDigit4.turn.at)


class TurnsDigit5(contact_counter_channel(5)):
    spindle = Frame(at=channels.TurnsDigit5.turn.at)


class TurnsDigit6(contact_counter_channel(6)):
    spindle = Frame(at=channels.TurnsDigit6.turn.at)
