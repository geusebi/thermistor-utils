# Thermistor utilities

A python based library implementing models to convert thermistor values 
from temperature to resistance and vice versa.

## Steinhart--Hart model

### Implementation precision

![SH resistance to temperature chart](charts/sh-res-temp.png "Steinhart & Hart model (py) resistance to temperature chart")
![SH temperature to resistance chart](charts/sh-temp-res.png "Steinhart & Hart model (py) temperature to resistance chart")

### How to use

```python
# import the Steinhart--Hart and or the Beta converter
from thermistor_utils import SH_converter
```

Create a converter from A, B, and C coefficients:

```python
A, B, C = (0.0008402250578523375, 0.00025963477647737156, 1.5674403473853433e-07, )
conv = SH_converter(A, B, C)
```

If they're not available the converter could compute the values from 
three evenly spaced readings of temperature and resistance.

Create the converter from temp/res readings:

```python
readings = (
    (0, 27445),
    (25, 10000),
    (50, 4160),
)
conv = SH_converter.from_points(readings)
```

Printing the coefficients in a form suitable for subsequent use in 
python and C:

```python
print(repr(conv))

# SH_converter(0.0008402250578523375, 0.00025963477647737156, 1.5674403473853433e-07, 0, 50)

print(conv.to_cstr())

# {0.0008402250578523375, 0.00025963477647737156, 1.5674403473853433e-07, 0, 50}

# compact but less precise representation
# (inverse of coefficients and no temperature range)
print(conv.to_cstr(compact=True, with_temps=False))

# {1./1190, 1./3852, 1./6379828}
```

Use the reference implementation in C (example-1.c):

```c
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
```

To compile and run from the examples directory:

```bash
$ mkdir -p ../bin
$ gcc -o ../bin/example-1 \
    -I../src/include \
    ../src/sh_converter.c \
    -lm \
    example-1.c

$ ../bin/example-1
25 Celsius -> 10000 Ohms
10k Ohms   -> 25 Celsius
```

## Beta model

### Implementation precision

![Beta resistance to temperature chart](charts/beta-res-temp.png "Beta model (py) resistance to temperature chart")
![Beta temperature to resistance chart](charts/beta-temp-res.png "Beta model (py) temperature to resistance chart")

### How to use

```python
# import the Steinhart--Hart and or the Beta converter
from thermistor_utils import Beta_converter
```

Create a converter from beta values:

```python
beta, R0, T0 = (3380, 10000, 25)
conv = Beta_converter(beta, R0, T0)
```

Printing the beta values in a form suitable for subsequent use in 
python and C:

```python
print(repr(conv))

# Beta_converter(3380, 10000, 25)

print(conv.to_cstr())

# {3380, 10000, 25}
```

Use the reference implementation in C (example-2.c):

```c
#include <stdio.h>
#include <thermistor_utils.h>

int main(void)
{
    struct beta_s bpar = {3380, 10000, 25};
    
    // 25C to Ohm and 10k Ohm to Celsius
    double  R_at_25   = beta_resistance(bpar, 25),
            T_at_10000 = beta_temperature(bpar, 10000);
    
    printf("25 Celsius -> %.0f Ohms\n", R_at_25);
    printf("10k Ohms   -> %.0f Celsius\n", T_at_10000);
}
```

To compile and run from the examples directory:

```bash
$ mkdir -p ../bin
$ gcc -o ../bin/example-2 \
      -I../src/include \
      ../src/beta_converter.c \
      -lm \
      example-2.c

$ ../bin/example-2
25 Celsius -> 10000 Ohms
10k Ohms   -> 25 Celsius

```
