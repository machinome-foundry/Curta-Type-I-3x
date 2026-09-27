"""Attach the clearing pin and coil; leave the carrier's fixed hardware alone."""

from machinome.node import Frame
from machinome.motion.joints import Prismatic
from simulation.cover_fits import FittedAxleCarrier
from simulation.clearing_seat_fit import FittedClearingPin
from simulation.clearing_stop_spring import MountedClearingSpring, WIRE_RADIUS, SEAT_GAP
from simulation.source_frames import source_frame


class FramedClearingPin(FittedClearingPin):
    datum = Frame()


class FramedClearingSpring(MountedClearingSpring):
    datum = Frame()


class FrameAttachedAxleCarrier(FittedAxleCarrier):
    pin_seat = source_frame(at=(29.439639004, 8.004156813, 21.6),
                            angle=-179.450083095, axis=(0, 0, 1))
    spring_seat = source_frame(
        at=(29.439639004, 8.004156813, 44.4 - WIRE_RADIUS - SEAT_GAP),
        angle=-180, axis=(-.004798912, .999988485, 0))
    clearing_pin = FramedClearingPin(slide=Prismatic(axis=(0, 0, -1)))
    clearing_pin_spring = FramedClearingSpring(slide=Prismatic(axis=(0, 0, -1)))
    pin_mount = clearing_pin.datum.on(pin_seat, clearing_pin.slide)
    spring_mount = clearing_pin_spring.datum.on(spring_seat, clearing_pin_spring.slide)

    def render(self):
        # Unchanged fixed-child source placements, extracted mechanically from
        # standard.assembly.UpperCarriageBody1. No runtime source inspection.
        self.digits_axle_1.rotate(100.075449365, (0.385870743, 0.837978245, -0.385870743))
        self.digits_axle_1.translate((-47.293529942, 55.866324875, 33.9))
        self.digits_axle_2.rotate(-152.385861218, (0.685421323, -0.24575439, -0.685421323))
        self.digits_axle_2.translate((57.350022757, -46.787554869, 33.9))
        self.digits_axle_3.rotate(119.683014833, (0.575494277, 0.581044468, -0.575494277))
        self.digits_axle_3.translate((-0.168421671, 73.532491424, 33.9))
        self.digits_axle_4.rotate(-131.796946865, (-0.632406026, -0.447353592, 0.632406026))
        self.digits_axle_4.translate((25.036814601, 69.337152237, 33.9))
        self.counter_body_pin_1.rotate(-180.0, (-0.004798912, 0.999988485, 0.0))
        self.counter_body_pin_1.translate((-20.461311724, -0.239729261, 49.5))
        self.digits_axle_5.rotate(90.001319496, (-0.004798857, 0.999976971, 0.004798857))
        self.digits_axle_5.translate((-73.032947672, -0.744319989, 33.9))
        self.counter_body_stop_pin.rotate(-180.0, (-0.004798912, 0.999988485, 0.0))
        self.counter_body_stop_pin.translate((-23.260793032, 16.287579306, 35.544410518))
        self.counter_body_pin_2.rotate(-180.0, (-0.004798912, 0.999988485, 0.0))
        self.counter_body_pin_2.translate((21.536753794, 0.163374695, 49.5))
        self.digits_axle_6.rotate(-166.279900138, (0.701970973, -0.120305885, -0.701970973))
        self.digits_axle_6.translate((69.913050555, -24.537270849, 33.9))
        self.digits_axle_7.rotate(91.823266661, (-0.175600548, 0.968673782, 0.175600548))
        self.digits_axle_7.translate((-68.354578426, -25.864385029, 33.9))
        self.digits_axle_8.rotate(96.896723418, (-0.327424313, 0.886333255, 0.327424313))
        self.digits_axle_8.translate((-55.366781123, -47.86942826, 33.9))
        self.digits_axle_9.rotate(144.855498385, (0.670712366, 0.316685717, -0.670712366))
        self.digits_axle_9.translate((47.287098621, 56.774124438, 33.9))
        self.digits_axle_10.rotate(-126.266796884, (0.609655748, -0.506596228, -0.609655748))
        self.digits_axle_10.translate((14.008548397, -72.368521826, 33.9))
        self.digits_axle_11.rotate(104.724258057, (-0.450175858, 0.771157178, 0.450175858))
        self.digits_axle_11.translate((-35.636075797, -64.10531671, 33.9))
        self.digits_axle_12.rotate(91.635101119, (0.166560565, 0.971861696, -0.166560565))
        self.digits_axle_12.translate((-68.837608485, 24.460916283, 33.9))
        self.digits_axle_13.rotate(-138.950666871, (0.655684002, -0.374375453, -0.655684002))
        self.digits_axle_13.translate((37.93459291, -63.399174004, 33.9))
        self.digits_axle_14.rotate(114.702446195, (-0.542894613, 0.640726836, 0.542894613))
        self.digits_axle_14.translate((-11.542276705, -72.613762614, 33.9))
        self.counter_body.rotate(-180.0, (-0.004798912, 0.999988485, 0.0))
        self.counter_body.translate((0.537721035, -0.038177283, 45.0))
        self.digits_axle_15.rotate(158.527493838, (0.69427986, 0.189607366, -0.69427986))
        self.digits_axle_15.translate((63.898717756, 37.358694592, 33.9))
        self.clearing_stop_pin_sleeve.rotate(-179.450083095, (0.0, 0.0, 1.0))
        self.clearing_stop_pin_sleeve.translate((29.439639004, 8.004156813, 25.5))
        self.digits_axle_16.rotate(179.611150774, (0.70710271, 0.003393363, -0.70710271))
        self.digits_axle_16.translate((74.108389818, 0.667965423, 33.9))
        self.digits_axle_17.rotate(108.934580006, (0.494966135, 0.714154781, -0.494966135))
        self.digits_axle_17.translate((-25.288486711, 68.854122178, 33.9))
