#include <stdio.h>
#include <thermistor_utils.h>

int main(void)
{
    struct sh_s coefficients = {1./1190, 1./3852, 1./6379828};
    
    // 25C to Ohm and 10k Ohm to Celsius
    double  R_at_25   = sh_resistance(coefficients, 25),
            T_at_10000 = sh_temperature(coefficients, 10000);
    
    printf("25 Celsius -> %.0f Ohms\n", R_at_25);
    printf("10k Ohms   -> %.0f Celsius\n", T_at_10000);
}

// gcc -o example-1 -I ../src -lm ../src/sh_converter.c example-1.c
// ./example-1
// 25 Celsius -> 10005 Ohms
// 10k Ohms   -> 25 Celsius
