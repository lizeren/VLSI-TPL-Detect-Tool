# Testing TPL 

Currently I have Three TPLs: Pwgen, LibSodium and a c++ program that draws ascii cat and dog. Test.cpp using pwgen to generate passwords and pwgen calls libsodium to generate random bytes. Test.cpp also uses libcurl to download a map file from a website. It also uses draw.h to draw ascii cat and dog.
  
## How to use
```bash
make
```
Move the executable `draw_test` and `pwgen_exec` from this direcotry to `dataset/dataset2/1_binary/candidate` folder of Libam. Move `password_generator`to   `dataset/dataset2/1_binary/target` 

## Function Call Graph
```scss
test.cpp
│
├── pw_phonemes() [from pwgen/pwgen.h]
│   └── randombytes_random() [from libsodium/sodium.h]
│
├── drawcat() [from draw/draw.h]
└── drawdog() [from draw/draw.h]
│
│
└── download_map()
│   └── curl_easy_init() [from libcurl/libcurl.h]
│   └── curl_easy_setopt() [from libcurl/libcurl.h]
│   └── curl_easy_perform() [from libcurl/libcurl.h]
│   └── curl_easy_cleanup() [from libcurl/libcurl.h]
```