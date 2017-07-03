cmake_minimum_required(VERSION 3.6 FATAL_ERROR)
project(SDL2_mixer C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

option(BUILD_SHARED_LIBS "" ON)

add_library(SDL2_mixer
  dynamic_mp3.c
  dynamic_ogg.c
  effect_position.c
  effects_internal.c
  effect_stereoreverse.c
  fluidsynth.c
  load_mp3.c
  load_ogg.c
  load_aiff.c
  load_voc.c
  mixer.c
  music.c
  music_mod.c
  music_modplug.c
  music_ogg.c
  wavestream.c
)

target_link_libraries(SDL2_mixer PUBLIC CONAN_PKG::SDL2 CONAN_PKG::smpeg CONAN_PKG::libvorbis $<$<PLATFORM_ID:Linux>:m>)
target_compile_definitions(SDL2_mixer PUBLIC OGG_MUSIC MP3_MUSIC)

add_executable(playmus playmus.c)
target_link_libraries(playmus PUBLIC SDL2_mixer CONAN_PKG::libvorbis)
