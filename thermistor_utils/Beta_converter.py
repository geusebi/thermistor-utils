from math import log, exp


__all__ = ("Beta_converter", )

# todo: check all the docstrings


class Beta_converter(object):
    """
    Convert between temperature and resistance given the beta
    value and R0 temperature of a termistor.
    """
    __slots__ = ("beta", "R0", "T0", "T1", )

    def __init__(self, beta, R0, T0, T1=None):
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
        R = R0 * exp(beta * (1 / (T + 273.15) - 1 / T0))

        return R

    def _to_str_impl(self, with_temps=True):
        """
        Stringify (kinda) implementation used by
        `__repr__`, `__str__` and `to_cstr`.
        """
        beta, R0, T0, T1 = self.beta, self.R0, self.T0, self.T1

        if with_temps and T1 is not None:
            return f"{beta}, {R0}, {T0}, {T1}"

        return f"{beta}, {R0}, {T0}"

    def to_cstr(self, with_temps=True):
        """
        Return a string with the beta values and, if available, the
        temperatures provided upon creation.

        Use `with_temp` to control whether the low/high temperature
        should be printed.
        """
        s = self._to_str_impl(with_temps)
        return f"{{{s}}}"

    def __repr__(self):
        """
        Tentatively print the converter to satisfy

            converter = eval(converter)

        Where equality means different objects but same functionality.
        """
        s = self._to_str_impl(with_temps=True)
        return f"Beta_converter({s})"

    def __str__(self):
        """
        Create a string representation of the object.
        """
        s = self._to_str_impl(with_temps=True)
        return f"Beta_converter[{s}]"
