import unittest
from thermistor_utils import *


__ALL__ = ("Test_Beta_converter", )


values = dict(zip(
    range(-40, 151, 5),
    (197_390, 149_390, 114_340, 88_381, 68_915, 54_166, 
    42_889, 34_196, 27_445, 22_165, 18_010, 14_720, 
    12_099, 10_000, 8_309, 6_939, 5_824, 4_911, 4_160, 
    3_539, 3_024, 2_593, 2_233, 1_929, 1_673, 1_455, 
    1_270, 1_112, 976, 860, 759, 673, 598, 
    532, 476, 426, 383, 344, 311, )
))

Beta_values = (
    3380,
    10000,
    25,
    50,
)

precision = 3

class Test_Beta_converter(unittest.TestCase):
    def testCreation(self):
        conv = Beta_converter(*Beta_values)
        T_10k = round(conv.temperature(10000), precision)
        R_25c = round(conv.resistance(25), precision)
        
        self.assertEqual(T_10k, 25.000)
        self.assertEqual(R_25c, 10000.000)
    
    def testCreationFromBeta(self):
        beta, R0, T0, T1 = Beta_values
        
        conv = Beta_converter.from_beta(*Beta_values)
        
        self.assertEqual(conv.beta, beta)
        self.assertEqual(conv.R0, R0)
        self.assertEqual(conv.T0, T0)
        self.assertEqual(conv.T1, T1)
    
    def testFullRangeConversion(self):
        conv = Beta_converter(*Beta_values)
        
        for temp, res in values.items():
            T = conv.temperature(res)
            R = conv.resistance(temp)
            
            Tdiff = abs(T - temp)
            Rdiff = abs(R - res)
            
            if temp < 25:
                Tmaxdiff = 3
                Rmaxdiff = res * .20
            elif temp <= 50:
                Tmaxdiff = .1
                Rmaxdiff = res * .01
            else:
                Tmaxdiff = 7
                Rmaxdiff = res * .20
            
            self.assertTrue(Tdiff <= Tmaxdiff)
            self.assertTrue(Rdiff <= Rmaxdiff)

