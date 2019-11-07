import unittest
from thermistor_utils import *
from .reference_data import THERMISTORS

__ALL__ = ("Test_Beta_converter", )


VALUES = THERMISTORS[0]["VALUES"]
BETA_25_50 = THERMISTORS[0]["BETA"]

precision = 3

class Test_Beta_converter(unittest.TestCase):
    def testCreation(self):
        conv = Beta_converter(*BETA_25_50)
        T_10k = round(conv.temperature(10000), precision)
        R_25c = round(conv.resistance(25), precision)
        
        self.assertEqual(T_10k, 25.000)
        self.assertEqual(R_25c, 10000.000)
    
    def testCreationFromBeta(self):
        beta, R0, T0, T1 = BETA_25_50
        
        conv = Beta_converter.from_beta(*BETA_25_50)
        
        self.assertEqual(conv.beta, beta)
        self.assertEqual(conv.R0, R0)
        self.assertEqual(conv.T0, T0)
        self.assertEqual(conv.T1, T1)
    
    def testFullRangeConversion(self):
        conv = Beta_converter(*BETA_25_50)
        
        for temp, res in VALUES.items():
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

