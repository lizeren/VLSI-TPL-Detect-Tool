CC = gcc
CXX = g++
CFLAGS = -Wall -O0 -fPIC
CXXFLAGS = -Wall -O0 -fPIC
# LIBS for curl
LIBS = -lz -lssl -lcrypto -ldl -pthread -lpsl
SODIUM_STATIC_LIB = /home/lizeren/Desktop/VLSI-TPL-Detect-Tool/tpl/Static/lib/libsodium/libsodium.a
CURL_LIB_PATH = /home/lizeren/Desktop/VLSI-TPL-Detect-Tool/tpl/Static/lib/libcurl
# PSL_LIB_PATH = /home/lizeren/Desktop/VLSI-TPL-Detect-Tool/tpl/Static/lib/libpsl
DRAW_STATIC_LIB = draw/libdraw.a
CURL_STATIC_LIB = $(CURL_LIB_PATH)/libcurl.a
PWGEN_STATIC_LIB = pwgen/libpwgen.a
LDFLAGS = -L. -L$(CURL_LIB_PATH) 

PWGEN_SRCS = pwgen/pw_phonemes.c pwgen/pw_rand.c pwgen/randnum.c pwgen/sha1.c pwgen/sha1num.c pwgen/pwgen.c
PWGEN_OBJS = $(PWGEN_SRCS:.c=.o)

DRAW_SRCS = draw/draw.cpp
DRAW_OBJS = $(DRAW_SRCS:.cpp=.o)

all: $(PWGEN_STATIC_LIB) $(DRAW_STATIC_LIB) password_generator

$(PWGEN_STATIC_LIB): $(PWGEN_OBJS)
	ar rcs $@ $^

$(DRAW_STATIC_LIB): $(DRAW_OBJS)
	ar rcs $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

password_generator: test.cpp $(PWGEN_STATIC_LIB) $(DRAW_STATIC_LIB)
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDFLAGS) $(PWGEN_STATIC_LIB) $(DRAW_STATIC_LIB) $(CURL_STATIC_LIB) $(SODIUM_STATIC_LIB) $(LIBS)

run: password_generator
	LD_LIBRARY_PATH=$(CURL_LIB_PATH):$$LD_LIBRARY_PATH ./password_generator
	
clean:
	rm -f $(PWGEN_OBJS) $(DRAW_OBJS) $(PWGEN_STATIC_LIB) $(DRAW_STATIC_LIB) password_generator *.zip
