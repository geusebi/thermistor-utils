import unittest
from thermistor_utils import SH_converter
from .reference_data import THERMISTORS

__all__ = ("Test_SH_converter", )


VALUES = THERMISTORS[0]["VALUES"]
ABC_0_50 = THERMISTORS[0]["COEFFICIENTS"]

precision = 3


class Test_SH_converter(unittest.TestCase):
    def testCreationFromABC(self):
        conv = SH_converter(*ABC_0_50)
        T_10k = round(conv.temperature(10000), precision)
        R_25c = round(conv.resistance(25), precision)

        self.assertEqual(T_10k, 25.000)
        self.assertEqual(R_25c, 10000.000)

    def testCreationFromPoints(self):
        A, B, C, _, _ = ABC_0_50
        points = (
            (0, VALUES[0]),
            (25, VALUES[25]),
            (50, VALUES[50]),
        )

        conv = SH_converter.from_points(points)

        self.assertEqual(conv.A, A)
        self.assertEqual(conv.B, B)
        self.assertEqual(conv.C, C)
        self.assertEqual(conv.Tl, points[0][0])
        self.assertEqual(conv.Th, points[2][0])

    def testFullRangeConversion(self):
        conv = SH_converter(*ABC_0_50)

        for temp, res in VALUES.items():
            T = conv.temperature(res)
            R = conv.resistance(temp)

            Tdiff = abs(T - temp)
            Rdiff = abs(R - res)

            if temp < 0:
                Tmaxdiff = 1
                Rmaxdiff = res * .015
            elif temp < 50:
                Tmaxdiff = .01
                Rmaxdiff = res * .001
            else:
                Tmaxdiff = 1
                Rmaxdiff = res * .015

            self.assertTrue(Tdiff <= Tmaxdiff)
            self.assertTrue(Rdiff <= Rmaxdiff)
