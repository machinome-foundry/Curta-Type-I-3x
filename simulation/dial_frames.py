"""Attachment datums on the fitted, source-backed register dials.

The fifteen pin-and-dial assemblies retain the source assembly coordinates
inside their children. Their axle frames therefore use those native radial
datums. The two bare type-2 dials have an axle at their own origin. Nothing
here changes a shape, fit, joint or source placement.
"""

from machinome.node import Frame
from simulation import dial_fits as fitted


class Part10203_1(fitted.Part10203_1):
    axle = Frame(at=(72.008486542, 0.647810225, 33.9),
                 z=(-0.9999539409, -0.0095977127, 2e-10), x=(0, 0, 1))


class Part10203_2(fitted.Part10203_2):
    axle = Frame(at=(67.932893459, -23.838001321, 33.9),
                 z=(-0.9429319505, 0.3329854904, 1e-10), x=(0, 0, 1))


class Part10203_3(fitted.Part10203_3):
    axle = Frame(at=(-45.928298358, 54.270661151, 33.9),
                 z=(0.650110279, -0.7598398681, 3e-10), x=(0, 0, 1))


class Part10203_4(fitted.Part10203_4):
    axle = Frame(at=(-24.5513378, 66.887752049, 33.9),
                 z=(0.3510232907, -0.936366728, 0), x=(0, 0, 1))


class Part10204_1(fitted.Part10204_1):
    axle = Frame(at=(13.624055025, -70.304020713, 33.9),
                 z=(-0.183092082, 0.9830957682, 0), x=(0, 0, 1))


class Part10204_2(fitted.Part10204_2):
    axle = Frame(at=(-11.197481322, -70.542261674, 33.9),
                 z=(0.164188277, 0.9864290191, 0), x=(0, 0, 1))


class Part10204_3(fitted.Part10204_3):
    axle = Frame(at=(-34.603579072, -62.276669529, 33.9),
                 z=(0.491665107, 0.870784372, 0), x=(0, 0, 1))


class Part10204_4(fitted.Part10204_4):
    axle = Frame(at=(-53.771117399, -46.504196676, 33.9),
                 z=(0.759839869, 0.650110278, 0), x=(0, 0, 1))


class Part10204_5(fitted.Part10204_5):
    axle = Frame(at=(-66.388208297, -25.127236119, 33.9),
                 z=(0.9363667283, 0.3510232901, 0), x=(0, 0, 1))


class Part10204_6(fitted.Part10204_6):
    axle = Frame(at=(-70.933044396, -0.724164791, 33.9),
                 z=(0.9999539409, 0.009597713, 0), x=(0, 0, 1))


class Part10204_7(fitted.Part10204_7):
    axle = Frame(at=(45.952746591, 55.152549691, 33.9),
                 z=(-0.6354057288, -0.7721784508, 0), x=(0, 0, 1))


class Part10205_1(fitted.Part10205_1):
    axle = Frame(at=(55.72844801, -45.453202839, 33.9),
                 z=(-0.7721784508, 0.6354057288, 0), x=(0, 0, 1))


class Part10205_2(fitted.Part10205_2):
    axle = Frame(at=(36.867186359, -61.590682021, 33.9),
                 z=(-0.5082888339, 0.8611866588, 0), x=(0, 0, 1))


class Part10205_3(fitted.Part10205_3):
    axle = Frame(at=(-0.148266473, 71.432588148, 33.9),
                 z=(0.009597713, -0.9999539409, 0), x=(0, 0, 1))


class Part10205_4(fitted.Part10205_4):
    axle = Frame(at=(24.337545072, 67.35699514, 33.9),
                 z=(-0.3329854899, -0.9429319506, 0), x=(0, 0, 1))


class FittedDialType2(fitted.FittedDialType2):
    axle = Frame()
