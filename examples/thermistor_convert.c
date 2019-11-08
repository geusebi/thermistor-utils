#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <thermistor_utils.h>

#define atod(s) strtod(s, NULL)

enum {SH, BETA};
enum {TO_RES, TO_TEMP};

void usage();
int parse_opts(int, char *[], int *, int *);

int main (int argc, char *argv[])
{
    int model, op;
    double value, result;

    if (!parse_opts(argc, argv, &model, &op)) {
        usage(argv[0]);
        return EXIT_FAILURE;
    }

    value = atod(argv[6]);

    if (model == SH) {
        struct sh_s conv;

        conv.A = atod(argv[2]);
        conv.B = atod(argv[3]);
        conv.C = atod(argv[4]);

        if (op == TO_TEMP) {
            result = sh_temperature(conv, value);
        }
        if (op == TO_RES) {
            result = sh_resistance(conv, value);
        }
    }

    if (model == BETA) {
        struct beta_s conv;

        conv.beta = atoi(argv[2]);
        conv.R0 = atoi(argv[3]);
        conv.T0 = atoi(argv[4]);

        if (op == TO_TEMP) {
            result = beta_temperature(conv, value);
        }
        if (op == TO_RES) {
            result = beta_resistance(conv, value);
        }
    }

    printf("%.6f\n", result);

    return EXIT_SUCCESS;
}

int
parse_opts(int argc, char *argv[], int *mod, int *op)
{
    if (argc < 7) {
        return 0;
    }

    if (strcmp("SH", argv[1]) == 0) {
        *mod = SH;
    } else if (strcmp("BETA", argv[1]) == 0) {
        *mod = BETA;
    } else {
        return 0;
    }

    if (strcmp("T", argv[5]) == 0) {
        *op = TO_RES;
    } else if (strcmp("R", argv[5]) == 0) {
        *op = TO_TEMP;
    } else {
        return 0;
    }

    return 1;
}

void usage(char *name) {
    fprintf(stderr,
    "Usage: %s BETA <beta> <R0> <T0> {R|T} <value>\n"
    "       %s SH   <A>    <B>  <C>  {R|T} <value>\n"
    "\n"
    "NOTE: this is an example program, its main purpose is for\n"
    "testing the code.\n\n"
    "Convert a temperature in resistance and vice versa using the\n"
    "BETA or SH (Steinhart--Hart) model.\n"
    "<beta>, <R0> and <T0> are the setup values for a beta model\n"
    "converter.\n"
    "<A>, <B> and <C> are the coefficents for a SH converter.\n"
    "<value> is the value to convert.\n"
    "{R|T} specifies which value is given and therefore which\n"
    "operation to perform.\n\n"
    "E.g.\n"
    "    $ %s BETA 3380 10000 25 R 10000\n"
    "    25.000000\n"
    "    $ %s BETA 3380 10000 25 T 25\n"
    "    10000.000000\n"
    "\n"
    , name, name, name, name);
}
