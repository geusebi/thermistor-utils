import unittest
from thermistor_utils import *


__ALL__ = ("Test_SH_converter", )


values = dict(zip(
    range(-40, 151, 5),
    (197_390, 149_390, 114_340, 88_381, 68_915, 54_166, 
    42_889, 34_196, 27_445, 22_165, 18_010, 14_720, 
    12_099, 10_000, 8_309, 6_939, 5_824, 4_911, 4_160, 
    3_539, 3_024, 2_593, 2_233, 1_929, 1_673, 1_455, 
    1_270, 1_112, 976, 860, 759, 673, 598, 
    532, 476, 426, 383, 344, 311, )
))

ABC_0_25_50 = (
    0.0008402250578523375,
    0.00025963477647737156,
    1.5674403473853433e-07,
)

precision = 3

class Test_SH_converter(unittest.TestCase):
    def testCreationFromABC(self):
        conv = SH_converter(*ABC_0_25_50)
        T_10k = round(conv.temperature(10000), precision)
        R_25c = round(conv.resistance(25), precision)
        
        self.assertEqual(T_10k, 25.000)
        self.assertEqual(R_25c, 10000.000)
    
    def testCreationFromPoints(self):
        A, B, C = ABC_0_25_50
        points = (
            (0, values[0]),
            (25, values[25]),
            (50, values[50]),
        )
        
        conv = SH_converter.from_points(points)
        
        self.assertEqual(conv.A, A)
        self.assertEqual(conv.B, B)
        self.assertEqual(conv.C, C)
        self.assertEqual(conv.Tl, points[0][0])
        self.assertEqual(conv.Th, points[2][0])
    
    def testFullRangeConversion(self):
        conv = SH_converter(*ABC_0_25_50)
        
        for temp, res in values.items():
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

