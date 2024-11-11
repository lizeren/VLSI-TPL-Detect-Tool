CC = gcc
CXX = g++
CFLAGS = -Wall -O0 -fPIC
CXXFLAGS = -Wall -O0
LDFLAGS = -L.

PWGEN_SRCS = pwgen/pw_phonemes.c pwgen/pw_rand.c pwgen/randnum.c pwgen/sha1.c pwgen/sha1num.c pwgen/pwgen.c
PWGEN_OBJS = $(PWGEN_SRCS:.c=.o)

DRAW_SRCS = draw/draw.cpp
DRAW_OBJS = $(DRAW_SRCS:.cpp=.o)

all: password_generator pwgen_exec draw_test

libpwgen.a: $(PWGEN_OBJS)
	ar rcs $@ $^

libdraw.a: $(DRAW_OBJS)
	ar rcs $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

password_generator: test.cpp libpwgen.a libdraw.a
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDFLAGS) -lpwgen -ldraw -I.

pwgen_exec: $(PWGEN_OBJS)
	$(CC) $(CFLAGS) -o $@ $^

draw_test: draw/draw.cpp
	$(CXX) $(CXXFLAGS) -DDRAW_MAIN $< -o $@

clean:
	rm -f $(PWGEN_OBJS) $(DRAW_OBJS) libpwgen.a libdraw.a password_generator pwgen_exec draw_test
