"""The existing collar bores must clear and locate both unchanged carrier pins."""

from machinome.test import TestCase
from simulation.collar_pin_seat import CollarPinSeat


class CollarPinSeatTest(TestCase):
    node = CollarPinSeat

    def test_source_clocking_reproduces_both_pin_contacts(self):
        from simulation.collar_pin_seat import SourceCollarPinSeat
        source = SourceCollarPinSeat()
        source.assemble()
        source.build_stls()
        for pin in (source.pin_left, source.pin_right):
            self.assertIntersecting(source.collar, pin)

    def test_both_pins_clear_their_existing_collar_bores(self):
        for pin in (self.node.pin_left, self.node.pin_right):
            with self.subTest(pin=pin.name):
                self.assertNotIntersecting(self.node.collar, pin)
                self.assertFreeWithin(self.node.collar, 1, against=pin)

    def test_both_pins_prevent_collar_rotation_beyond_bore_play(self):
        for pin in (self.node.pin_left, self.node.pin_right):
            with self.subTest(pin=pin.name):
                self.assertBlockedBeyond(self.node.collar, 2, against=pin)

    def test_collar_captures_the_pin_tips_below_the_blind_bore_roofs(self):
        for pin in (self.node.pin_left, self.node.pin_right):
            with self.subTest(pin=pin.name):
                self.assertFreeWithin(self.node.collar, .1, against=pin,
                                     along=(0, 0, 1))
                self.assertBlockedBeyond(self.node.collar, .6, against=pin,
                                         along=(0, 0, -1), directions='forward')

    def test_threaded_nut_clears_at_its_existing_installed_height(self):
        self.assertNotIntersecting(self.node.collar, self.node.nut)
        self.assertFreeWithin(self.node.nut, .1, against=self.node.collar,
                             along=(0, 0, 1))

    def test_thread_still_captures_the_nut_axially(self):
        self.assertBlockedBeyond(self.node.nut, .4, against=self.node.collar,
                                 along=(0, 0, 1))
