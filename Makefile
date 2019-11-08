CC = gcc

CFLAGS = -O3 -Isrc/include
CLIBS = -lm

HEADERS = src/include/thermistor_utils.h

SOURCES = $(wildcard src/*.c)
OBJS = $(patsubst src/%.c,obj/%.o,$(SOURCES))

SRCEXAMPLES = $(wildcard examples/*.c)
EXAMPLES = $(patsubst examples/%.c,bin/%,$(SRCEXAMPLES))


.PHONY: all clean tests python-tests

all: $(EXAMPLES)
	

bin/%: examples/%.c $(HEADERS) $(OBJS)
	@mkdir -p bin
	$(CC) -o $@ $(OBJS) $(CLIBS) $(CFLAGS) $<

.PRECIOUS: obj/%.o
obj/%.o: src/%.c $(HEADERS)
	@mkdir -p obj
	$(CC) -c -o $@ $(CFLAGS) $<

tests: bin/thermistor_convert
	python3 -m unittest tests -v

python-tests:
	python3 -m unittest tests -v

clean:
	rm -f bin/* && rm -df bin/
	rm -f obj/* && rm -df obj/
