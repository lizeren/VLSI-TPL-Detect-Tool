CC = gcc
CXX = g++
CFLAGS = -Wall -O0 -fPIC
CXXFLAGS = -Wall -O0 -fPIC
LIBS = -lsodium -lpwgen 
SODIUM_LIB_PATH = /home/lizeren/Desktop/VLSI-TPL-Detect-Tool/tpl/Static/lib/libsodium
CURL_LIB_PATH = /home/lizeren/Desktop/VLSI-TPL-Detect-Tool/tpl/Static/lib/libcurl
PSL_LIB_PATH = /home/lizeren/Desktop/VLSI-TPL-Detect-Tool/tpl/Static/lib/libpsl
DRAW_STATIC_LIB = draw/libdraw.a
CURL_STATIC_LIB = $(CURL_LIB_PATH)/libcurl.a
LDFLAGS = -L. -L$(SODIUM_LIB_PATH) -L$(CURL_LIB_PATH) -L$(PSL_LIB_PATH)

PWGEN_SRCS = pwgen/pw_phonemes.c pwgen/pw_rand.c pwgen/randnum.c pwgen/sha1.c pwgen/sha1num.c pwgen/pwgen.c
PWGEN_OBJS = $(PWGEN_SRCS:.c=.o)

DRAW_SRCS = draw/draw.cpp
DRAW_OBJS = $(DRAW_SRCS:.cpp=.o)

all: libpwgen.so $(DRAW_STATIC_LIB) password_generator

libpwgen.so: $(PWGEN_OBJS)
	$(CC) $(CFLAGS) -shared -o $@ $^ -L$(SODIUM_LIB_PATH) -lsodium

$(DRAW_STATIC_LIB): $(DRAW_OBJS)
	ar rcs $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

password_generator: test.cpp libpwgen.so $(DRAW_STATIC_LIB)
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDFLAGS) $(LIBS) $(DRAW_STATIC_LIB) $(CURL_STATIC_LIB) -lz -lssl -lcrypto -ldl -pthread -lpsl

run: password_generator
	LD_LIBRARY_PATH=$(SODIUM_LIB_PATH):$(CURL_LIB_PATH):$(PSL_LIB_PATH):$$LD_LIBRARY_PATH ./password_generator
	
clean:
	rm -f $(PWGEN_OBJS) $(DRAW_OBJS) libpwgen.so $(DRAW_STATIC_LIB) password_generator *.zip
