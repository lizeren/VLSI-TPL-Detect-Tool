#include <iostream>
#include <cstring>
#include "include/curl/curl.h"
#include <cstdio>
#include "include/draw/draw.h"

extern "C" {
#include "pwgen/pwgen.h"

// Define the global variable that's declared in pwgen.h
int (*pw_number)(int max_num);
}


// Define the flags we want to use (from pwgen.h)
#define PW_DIGITS   0x0001  // At least one digit
#define PW_UPPERS   0x0002  // At least one uppercase letter
#define PW_SYMBOLS  0x0004  // Include symbols
#define PW_AMBIGUOUS 0x0008 // Don't use ambiguous characters
#define PW_NO_VOWELS 0x0010 // Don't use vowels


void download_map() {
    CURL* curl;
    FILE* fp;
    CURLcode res;

    const char* url = "https://kz-rush.ru/download/map/cs16/JIG_happy_fogday_ez";
    const char* outFileName = "JIG_happy_fogday_ez.zip";  // Specify the desired output filename

    // Initialize curl
    curl = curl_easy_init();
    if (curl) {
        // Open the file for writing
        fp = fopen(outFileName, "wb");
        if (!fp) {
            perror("Failed to open file");
            return;
        }

        // Set curl options
        curl_easy_setopt(curl, CURLOPT_URL, url);             // Set the URL
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);        // Set the output file pointer
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);   // Follow redirects automatically

        // Perform the file download
        res = curl_easy_perform(curl);

        // Check for errors
        if (res == CURLE_OK) {
            std::cout << "File downloaded successfully as: " << outFileName << std::endl;
        } else {
            std::cerr << "Download failed: " << curl_easy_strerror(res) << std::endl;
        }

        // Cleanup
        fclose(fp);
        curl_easy_cleanup(curl);
    } else {
        std::cerr << "Failed to initialize curl." << std::endl;
        return;
    }

    return;
}


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
    download_map();

    delete[] buf;
    return 0;
}
