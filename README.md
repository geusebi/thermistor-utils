# Thermistor utilities

A python based library implementing models to convert thermistor values 
from temperature to resistance and vice versa.

# How to use

```python
# import the Steinhart--Hart and or the Beta converter
from thermistor_utils import SH_converter, Beta_converter
```

## Steinhart--Hart model

Create a converter from A, B, and C coefficients

```python
A, B, C = (values...)
conv.SH_converter(A, B, C)
```

If they're not available the converter could compute the values from 
three evenly spaced readings of temperature and resistance.

Create the converter from temp/res readings

```python
readings = (
    (0, 27445),
    (25, 10000),
    (50, 4160),
)
conv = SH_converter.from_points(readings)
```

Printing the coefficients in a form suitable for subsequent use in 
python and C

```python
print(repr(conv))

# SH_converter(A=0.0008402250578523375, B=0.00025963477647737156, C=1.5674403473853433e-07, Tl=0, Th=50)

print(conv.to_cstr())

# {0.0008402250578523375, 0.00025963477647737156, 1.5674403473853433e-07, 0, 50}

# compact but less precise representation
# (inverse of coefficients and no temperature range)
print(conv.to_cstr(short=True, with_temp=False))

# {1./1190, 1./3852, 1./6379828}
```

Use the reference implementation in C (example-1.c)

```c
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
```

## Beta model

todo: documentation in readme file
