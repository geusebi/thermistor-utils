
#ifndef _THERMISTOR_UTILS_H
#define _THERMISTOR_UTILS_H

struct sh_s {
    double A;
    double B;
    double C;
    int Tl;
    int Th;
};

double
sh_temperature(struct sh_s SH, double R);

double
sh_resistance(struct sh_s SH, double T);

struct beta_s {
    int beta;
    int R0;
    int T0;
    int T1;
};

double
beta_temperature(struct beta_s B, double R);

double
beta_resistance(struct beta_s B, double T);

#endif
