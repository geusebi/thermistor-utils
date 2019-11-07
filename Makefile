CC = gcc
CFLAGS = -O0

.PHONY: all clean tests python-tests

HEADERS = src/thermistor_utils.h

OBJS = \
	objs/sh_converter.o \
	objs/beta_converter.o

all: $(OBJS)
	

objs/%.o: src/%.c $(HEADERS)
	@mkdir -p objs
	$(CC) -c -o $@ $< $(CFLAGS)

tests: python-tests
	

python-tests:
	python3 -m unittest tests -v

clean:
	rm -f objs/*.o
	rmdir objs
