from math import log, exp


__ALL__ = ("Beta_converter", )

# todo: check all the docstrings

class Beta_converter(object):
    """
    Convert between temperature and resistance given the beta
    value and R0 temperature of a termistor.
    """
    __slots__ = ("beta", "R0", "T0", "T1", )

    def __init__(self, beta, R0, T0, T1):
        """ Create a converter where `beta` is the beta value in 
        Kelvin and `R0` is the resistance at 25 degrees Celsius.
        `T0` and `T1` are respectively the temperature references
        used to calculate the beta value. """
        self.beta, self.R0 = beta, R0
        self.T0, self.T1 = T0, T1

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
        beta, R0 = self.beta, self.R0
        T0 = self.T0 + 273.15
        T = 1 / (1 / T0 + 1 / beta * log(R / R0)) - 273.15

        return T

    def resistance(self, T):
        """
        Calculate the resistance given the temperature (Celsius).
        """
        T0 = self.T0 + 273.15
        beta, R0 = self.beta, self.R0
        R = R0 * exp(beta * ( 1 / (T + 273.15) - 1 / T0))

        return R

    def __repr__(self):
        return (
            f"Beta_converter("
            f"beta={self.beta:g}, R0={self.R0:g}, "
            f"T0={self.T0:g}, T1={self.T1:g})"
        )

    def __str__(self):
        return (
            f"Beta_converter["
            f"B={self.beta}K at {self.R0} "
            f"{self.T0}/{self.T1}]"
        )
