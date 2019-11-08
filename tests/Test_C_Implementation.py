import unittest
from thermistor_utils import *
from .reference_data import THERMISTORS

from os import getcwd
from pathlib import Path
from subprocess import run, PIPE

__ALL__ = ("CImplementation", )


VALUES = THERMISTORS[0]["VALUES"]
ABC_0_50 = THERMISTORS[0]["COEFFICIENTS"]
BETA_25_50 = THERMISTORS[0]["BETA"]

cwd = Path(getcwd())
th_conv_path = cwd.joinpath("bin").joinpath("thermistor_convert")
print(th_conv_path)
missing_th_conv = not th_conv_path.is_file()


def th_conv(*args):
    str_args = map(str, (th_conv_path, ) + args)
    result = run(str_args, stdout=PIPE, encoding="utf-8")
    return result.stdout.strip()


class CImplementation(unittest.TestCase):
    @unittest.skipIf(missing_th_conv, "missing thermistor_convert binary")
    def test_sh_full_range(self):
        ABC = ABC_0_50[:3]
        conv = SH_converter(*ABC_0_50)
        
        for T_d, R_d in VALUES.items():
            R_c = th_conv("SH", *ABC, "T", T_d)
            T_c = th_conv("SH", *ABC, "R", R_d)

            self.assertEqual(T_c, "%.6f" % conv.temperature(R_d))
            self.assertEqual(R_c, "%.6f" % conv.resistance(T_d))

    @unittest.skipIf(missing_th_conv, "missing thermistor_convert binary")
    def test_beta_full_range(self):
        beta_values = BETA_25_50[:3]
        conv = Beta_converter(*BETA_25_50)
        
        for T_d, R_d in VALUES.items():
            R_c = th_conv("BETA", *beta_values, "T", T_d)
            T_c = th_conv("BETA", *beta_values, "R", R_d)

            self.assertEqual(T_c, "%.6f" % conv.temperature(R_d))
            self.assertEqual(R_c, "%.6f" % conv.resistance(T_d))
