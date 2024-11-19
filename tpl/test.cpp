#include <iostream>
#include <cstring>

extern "C" {
#include "pwgen/pwgen.h"

// Define the global variable that's declared in pwgen.h
int (*pw_number)(int max_num);
}

#include "include/draw/draw.h"

// Define the flags we want to use (from pwgen.h)
#define PW_DIGITS   0x0001  // At least one digit
#define PW_UPPERS   0x0002  // At least one uppercase letter
#define PW_SYMBOLS  0x0004  // Include symbols
#define PW_AMBIGUOUS 0x0008 // Don't use ambiguous characters
#define PW_NO_VOWELS 0x0010 // Don't use vowels

int main() {
    int length, count;
    
    std::cout << "ASCII Cat:" << std::endl;
    Draw::drawCat();
    std::cout << std::endl;
    
    // User input for password length and count
    std::cout << "Enter the length of the password: ";
    std::cin >> length;
    std::cout << "Enter the number of passwords to generate: ";
    std::cin >> count;

    // Allocate buffer for password
    char* buf = new char[length + 1];
    if (!buf) {
        std::cerr << "Failed to allocate memory" << std::endl;
        return 1;
    }

    // Set default flags (similar to pwgen's defaults)
    int pwgen_flags = PW_DIGITS | PW_UPPERS;
    
    // Initialize the random number generator
    pw_number = pw_random_number;

    // Generate and print passwords
    for (int i = 0; i < count; ++i) {
        pw_phonemes(buf, length, pwgen_flags, nullptr);
        std::cout << buf << std::endl;
    }

    std::cout << "\nASCII Dog:" << std::endl;
    Draw::drawDog();

    delete[] buf;
    return 0;
}
