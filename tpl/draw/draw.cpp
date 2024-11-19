#include <iostream>
#include "../include/draw/draw.h"

namespace Draw {
    void drawCat() {
        std::cout << "  /\\___/\\" << std::endl;
        std::cout << " (  o o  )" << std::endl;
        std::cout << " (  =^=  )" << std::endl;
        std::cout << "  (---)  " << std::endl;
        std::cout << " /     \\" << std::endl;
        std::cout << "/       \\" << std::endl;
    }

    void drawDog() {
        std::cout << "   / \\__" << std::endl;
        std::cout << "  (    @\\___" << std::endl;
        std::cout << "  /         O" << std::endl;
        std::cout << " /   (_____/" << std::endl;
        std::cout << "/_____/   U" << std::endl;  
    }
}

#ifdef DRAW_MAIN
int main() {
    std::cout << "ASCII Cat:" << std::endl;
    Draw::drawCat();
    std::cout << "\nASCII Dog:" << std::endl;
    Draw::drawDog();
    return 0;
}
#endif
