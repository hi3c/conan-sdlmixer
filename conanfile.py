from conans import ConanFile, CMake, tools
import os
import shutil


class SdlmixerConan(ConanFile):
    name = "SDL2_mixer"
    version = "2.0.1_1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = ("SDL2/2.0.5_1@hi3c/experimental",
                "smpeg/2.0.0@hi3c/experimental",
                "libvorbis/1.3.5@hi3c/experimental")
    exports = "CMakeLists.txt"

    def source(self):
        url = "https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-{version}.zip"
        if self.settings.os == "Windows":
            url = "https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-devel-{version}-VC.zip"

        url = url.format(version=self.version)

        tools.download(url, "SDLmix.zip")
        tools.unzip("SDLmix.zip")
        os.remove("SDLmix.zip")

        shutil.copy("CMakeLists.txt", "SDL2_mixer-2.0.1")

    def build(self):
        if self.settings.os == "Windows":
            return

        cmake = CMake(self)
        cmake.configure(source_dir="SDL2_mixer-2.0.1")
        cmake.build()

    def package(self):
        self.copy("SDL_mixer.h", dst="include", src="SDL2_mixer-2.0.1", keep_path=False)
        self.copy("SDL_config.h", dst="include", src="include")

        if self.settings.os == "Windows":
            archdir = "SDL2_mixer-2.0.1/lib/{}".format("x64" if self.settings.arch == "x86_64" else "x86")
            self.copy("*.lib", src=archdir, dst="lib")
            self.copy("*.dll", src=archdir, dst="bin")

        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["SDL2_mixer"]
