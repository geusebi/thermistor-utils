#include <math.h>
#include "thermistor_utils.h"


double
beta_temperature(struct beta_s B, double R)
{
    double invT = 1. / (B.T0 + 273.15) + 1. / B.beta * log(R / B.R0);
    return 1. / invT - 273.15;
}

double
beta_resistance(struct beta_s B, double T)
{
    return 
        B.R0 * 
        exp(B.beta * ( 1 / (T + 273.15) - 1 / (B.T0 + 273.15)));
}
