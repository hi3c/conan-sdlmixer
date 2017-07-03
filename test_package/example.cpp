#include <iostream>

#define SDL_MAIN_HANDLED
#include <SDL.h>
#include <SDL_mixer.h>

int main() {
    SDL_Init(0);
    Mix_Init(0);
    return 0;
}
