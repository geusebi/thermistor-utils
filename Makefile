CC = gcc

BINDIR = bin
SOURCEDIR = src
INCLUDEDIR = $(SOURCEDIR)/include

CFLAGS = -O3 -I$(INCLUDEDIR)
CLIBS = -lm

BIN = $(BINDIR)/thermistor_convert
HEADER = $(INCLUDEDIR)/thermistor_utils.h
SOURCE = $(SOURCEDIR)/thermistor_convert.c

OBJS = \
	obj/sh_converter.o \
	obj/beta_converter.o

.PHONY: all clean tests python-tests

all: $(BIN)
	

$(BIN): $(SOURCE) $(HEADER) $(OBJS)
	@mkdir -p bin
	$(CC) -o $@ $(OBJS) $(CLIBS) $(CFLAGS) $<

obj/%.o: $(SOURCEDIR)/thermistor_utils/%.c $(HEADER)
	@mkdir -p obj
	$(CC) -c -o $@ $(CFLAGS) $<

tests: python-tests
	

python-tests:
	python3 -m unittest tests -v

clean:
	rm -f bin/* && rm -df bin/
	
	rm -f obj/* && rm -df obj/
