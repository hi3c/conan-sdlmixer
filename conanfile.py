from conans import ConanFile, CMake, tools
import os


class SdlmixerConan(ConanFile):
    name = "SDL2_mixer"
    version = "2.0.1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = "SDL2/2.0.5@hi3c/experimental"

    def source(self):
        tools.download("https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-devel-{version}-VC.zip".format(version=self.version),
                       "SDLmix.zip")
        tools.unzip("SDLmix.zip")
        os.remove("SDLmix.zip")

    def build(self):
        pass

    def package(self):
        self.copy("*.h", dst="include", src="SDL2_mixer-2.0.1/include")
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
