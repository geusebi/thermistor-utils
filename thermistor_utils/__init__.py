from math import sqrt, log, exp


__ALL__ = ("SH_converter", "Beta_converter", )

# todo: check all the docstrings

class SH_converter(object):
    """
    Convert between temperature and resistance given the
    Steinhart and Hart coefficients of a termistor.
    """
    __slots__ = ("A", "B", "C", "Tl", "Th", )

    def __init__(self, A, B, C, Tl=None, Th=None):
        """
        Create converter with `A`, `B` and `C` coefficients.
        `Tl` and `Th` are respectively the lower temperature and
        higher temperature from which the coefficients have been
        computed.
        
        To create a converter starting from pairs of temperatures
        and resistances use `SH_converter.from_points`.
        """
        self.Tl, self.Th = Tl, Th
        self.A, self.B, self.C = A, B, C

    @staticmethod
    def from_points(TR_points):
        """
        Create a converter by computing coefficients from three
        evenly spaced temperature-resistance pairs.
        `TR_points` is a sequence of three temp/res pairs.

        See `SH_converter`.
        """
        (T1, R1), (T2, R2), (T3, R3) = TR_points

        Tk1, Tk2, Tk3 = map(
            lambda x: x + 273.15, (T1, T2, T3))

        L1, L2, L3 = log(R1), log(R2), log(R3)
        Y1, Y2, Y3 = 1 / Tk1, 1 / Tk2, 1 / Tk3

        G2 = (Y2 - Y1) / (L2 - L1)
        G3 = (Y3 - Y1) / (L3 - L1)

        C = ((G3 - G2) / (L3 - L2)) * (L1 + L2 + L3)**-1
        B = G2 - C * (L1**2 + L1 * L2 + L2**2)
        A = Y1 - (B + L1**2 * C) * L1

        return SH_converter(A, B, C, T1, T3, )


    def temperature(self, R):
        """
        Calculate the temperature (Celsius) given the resistance.
        """
        A, B, C = self.A, self.B, self.C
        lnR = log(R)
        T = 1 / (A + B * lnR + C * lnR**3) - 273.15

        return T

    def resistance(self, T):
        """
        Calculate the resistance given the temperature (Celsius).
        """
        Tk = T + 273.15

        A, B, C = self.A, self.B, self.C
        x = 1 / (2 * C) * (A - 1 / Tk)
        y = sqrt((B / (3 * C))**3 + x**2)            
        R = exp((y - x)**(1/3) - (y + x)**(1/3))
        
        return R

    def to_cstr(self, short=False, with_temp=True):
        A, B, C, Tl, Th = self.A, self.B, self.C, self.Tl, self.Th

        if short:
            ABC = f"1./{round(1/A)}, 1./{round(1/B)}, 1./{round(1/C)}"
        else:
            ABC = f"{A}, {B}, {C}"

        if with_temp and Tl is not None and Th is not None:
            return f"{{{ABC}, {Tl}, {Th}}}"

        return f"{{{ABC}}}"

    def __repr__(self):
        return (
            f"SH_converter("
            f"A={self.A}, B={self.B}, C={self.C}, "
            f"Tl={self.Tl}, Th={self.Th})"
        )

    def __str__(self):
        Tm = int((self.Tl + self.Th) / 2)
        return f"SH_converter[{self.Tl:g} : {Tm:g} : {self.Th:g}]"


class Beta_converter(object):
    """
    Convert between temperature and resistance given the beta
    value and R0 temperature of a termistor.
    """
    __slots__ = ("beta", "R0", "Tl", "Th", )

    def __init__(self, beta, R0, Tl, Th):
        """
        Create a converter where `beta` is the beta value in
        Kelvin and `R0` is the resistance at 25 degrees Celsius.
        `Tl` and `Th` are respectively the lower and
        higher temperature references used to calculate the
        beta value.
        """
        self.Tl, self.Th = Tl, Th
        self.beta, self.R0 = beta, R0

    @staticmethod
    def from_beta(beta, R0, T0=25, T1=50):
        """
        Create a converter based on the Beta model providing
        some predefined values.
        See `Beta_converter`.
        """
        return Beta_converter(beta, R0, T0, T1)

    
    def temperature(self, R):
        """
        Calculate the temperature (Celsius) given the resistance.
        """
        T0 = 25 + 273.15
        beta, R0 = self.beta, self.R0
        T = 1 / (1 / T0 + 1 / beta * log(R / R0)) - 273.15

        return T

    def resistance(self, T):
        """
        Calculate the resistance given the temperature (Celsius).
        """
        T0 = 25 + 273.15
        beta, R0 = self.beta, self.R0
        R = R0 * exp(beta * ( 1 / (T + 273.15) - 1 / T0))

        return R

    def __repr__(self):
        return (
            f"Beta_converter("
            f"beta={self.beta:g}, R0={self.R0:g}, "
            f"Tl={self.Tl:g}, Th={self.Th:g})"
        )

    def __str__(self):
        Tm = int((self.Tl + self.Th) / 2)
        return f"Beta_converter[B={self.beta}K {self.Tl}/{self.Th}]"
