from conans import ConanFile, CMake, tools
import os
import shutil


class SdlmixerConan(ConanFile):
    name = "SDL2_mixer"
    version = "2.0.1_2"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = "SDL2/2.0.5_1@hi3c/experimental"
    exports = "CMakeLists.txt"

    def source(self):
        url = "https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-{version}.zip"
        if self.settings.os == "Windows":
            url = "https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-devel-{version}-VC.zip"

        url = url.format(version=self.version.split("_")[0])

        tools.download(url, "SDLmix.zip")
        tools.unzip("SDLmix.zip")
        os.remove("SDLmix.zip")

        shutil.copy("CMakeLists.txt", "SDL2_mixer-2.0.1")
        sdlpath = os.path.join(self.deps_cpp_info["SDL2"].rootpath, self.deps_cpp_info["SDL2"].includedirs[0])
        tools.replace_in_file("SDL2_mixer-2.0.1/Xcode-iOS/SDL_mixer.xcodeproj/project.pbxproj",
                              "$(SRCROOT)/../../SDL/include", sdlpath)

    def build(self):
        if self.settings.os == "Windows":
            return

        if self.settings.os == "iOS" and self.settings.arch == "universal":
            # using xcodebuild for this
            projectfile = os.path.join(self.conanfile_directory, "SDL2_mixer-2.0.1", "Xcode-iOS", "SDL_mixer.xcodeproj")
            with tools.environment_append({"CC": "", "CXX": "", "CFLAGS": "", "CXXFLAGS": "", "LDFLAGS": ""}):
              # start with iOS sdk
              self.run("xcodebuild -sdk iphoneos -configuration Release -project {} CONFIGURATION_BUILD_DIR={}".format(projectfile,
                  os.path.join(self.conanfile_directory, "build-iOS")))
              
              # now iphonesimulator
              self.run("xcodebuild -sdk iphonesimulator -configuration Release -project {} CONFIGURATION_BUILD_DIR={}".format(projectfile,
                  os.path.join(self.conanfile_directory, "build-iOSSimulator")))
            
            os.makedirs(os.path.join(self.conanfile_directory, "build-universal"))
            self.run("lipo -output {}/libSDL2_mixer.a -create {} {}".format(
                os.path.join(self.conanfile_directory, "build-universal"),
                os.path.join(self.conanfile_directory, "build-iOS", "libSDL2_mixer.a"),
                os.path.join(self.conanfile_directory, "build-iOSSimulator", "libSDL2_mixer.a")))

    def package(self):
        self.copy("SDL_mixer.h", dst="include", src="SDL2_mixer-2.0.1", keep_path=False)
        self.copy("SDL_config.h", dst="include", src="include")

        if self.settings.os == "Windows":
            archdir = "SDL2_mixer-2.0.1/lib/{}".format("x64" if self.settings.arch == "x86_64" else "x86")
            self.copy("*.lib", src=archdir, dst="lib")
            self.copy("*.dll", src=archdir, dst="bin")

        self.copy("*.a", dst="lib", src="build-universal", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["SDL2_mixer"]
