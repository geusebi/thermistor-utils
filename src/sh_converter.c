#include <math.h>
#include "thermistor_utils.h"


double
sh_temperature(struct sh_s SH, double R)
{
    double lnR, invT;
    lnR = log(R);
    invT = SH.A + SH.B * lnR + SH.C * pow(lnR, 3);
    return 1 / invT - 273.15;
}

double
sh_resistance(struct sh_s SH, double T)
{
    double Tk, x, y, R;
    Tk = T + 273.15;
    x  = 1 / (2 * SH.C) * (SH.A - 1 / Tk);
    y  = sqrt(pow(SH.B / (3 * SH.C), 3) + pow(x, 2));
    R  = exp(pow(y - x, 1.0/3) - pow(y + x, 1.0/3));
    return R;
}
