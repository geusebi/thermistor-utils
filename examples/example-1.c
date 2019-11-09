#include <stdio.h>
#include <thermistor_utils.h>

int main(void)
{
    struct sh_s coefficients = {
        0.0008402250578523375,
        0.00025963477647737156,
        1.5674403473853433e-07
    };
    
    // 25C to Ohm and 10k Ohm to Celsius
    double  R_at_25   = sh_resistance(coefficients, 25),
            T_at_10000 = sh_temperature(coefficients, 10000);
    
    printf("25 Celsius -> %.0f Ohms\n", R_at_25);
    printf("10k Ohms   -> %.0f Celsius\n", T_at_10000);
}

/*
To compile and run from the examples directory:

    $ mkdir -p ../bin
    $ gcc -o ../bin/example-1 \
          -I../src/include \
          ../src/sh_converter.c \
          -lm \
          example-1.c

    $ ../bin/example-1
    25 Celsius -> 10000 Ohms
    10k Ohms   -> 25 Celsius

*/
