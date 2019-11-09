#include <stdio.h>
#include <thermistor_utils.h>

int main(void)
{
    struct beta_s bpar = {3380, 10000, 25, 50};
    
    // 25C to Ohm and 10k Ohm to Celsius
    double  R_at_25   = beta_resistance(bpar, 25),
            T_at_10000 = beta_temperature(bpar, 10000);
    
    printf("25 Celsius -> %.0f Ohms\n", R_at_25);
    printf("10k Ohms   -> %.0f Celsius\n", T_at_10000);
}

/*
To compile and run from the examples directory:

    $ mkdir -p ../bin
    $ gcc -o ../bin/example-2 \
          -I../src/include \
          ../src/beta_converter.c \
          -lm \
          example-2.c

    $ ../bin/example-2
    25 Celsius -> 10000 Ohms
    10k Ohms   -> 25 Celsius

*/
