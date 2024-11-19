CC = gcc
CXX = g++
CFLAGS = -Wall -O0 -fPIC
CXXFLAGS = -Wall -O0 -fPIC
LIBS = -lsodium -lpwgen -ldraw
LDFLAGS = -L. -L/home/lizeren/Desktop/VLSI-TPL-Detect-Tool/tpl/lib -Wl,-rpath,/home/lizeren/Desktop/VLSI-TPL-Detect-Tool/tpl/lib

PWGEN_SRCS = pwgen/pw_phonemes.c pwgen/pw_rand.c pwgen/randnum.c pwgen/sha1.c pwgen/sha1num.c pwgen/pwgen.c
PWGEN_OBJS = $(PWGEN_SRCS:.c=.o)

DRAW_SRCS = draw/draw.cpp
DRAW_OBJS = $(DRAW_SRCS:.cpp=.o)

all: libpwgen.so libdraw.so password_generator

libpwgen.so: $(PWGEN_OBJS)
	$(CC) $(CFLAGS) -shared -o $@ $^ -L/home/lizeren/Desktop/VLSI-TPL-Detect-Tool/tpl/lib -lsodium

libdraw.so: $(DRAW_OBJS)
	$(CXX) $(CXXFLAGS) -shared -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

password_generator: test.cpp libpwgen.so libdraw.so
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDFLAGS) $(LIBS)

run_password_generator: password_generator
	LD_LIBRARY_PATH=/home/lizeren/Desktop/VLSI-TPL-Detect-Tool/tpl/lib:$$LD_LIBRARY_PATH ./password_generator

clean:
	rm -f $(PWGEN_OBJS) $(DRAW_OBJS) libpwgen.so libdraw.so password_generator
