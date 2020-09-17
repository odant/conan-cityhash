# cityhash Conan package
# Dmitriy Vetutnev, Odant 2020


from conans import ConanFile, CMake, tools


class CityHashConan(ConanFile):
    name = "cityhash"
    version = "1.1.1+1"
    license = "https://raw.githubusercontent.com/google/cityhash/master/COPYING"
    description = "CityHash, a family of hash functions for strings."
    url = "https://github.com/odant/conan-cityhash"
    settings = {
        "os": ["Windows", "Linux"],
        "compiler": ["Visual Studio", "gcc"],
        "build_type": ["Debug", "Release"],
        "arch": ["x86", "x86_64", "mips", "armv7"]
    }
    options = {
        "fPIC": [True, False],
        "with_unit_tests": [True, False],
        "ninja": [True, False]
    }
    default_options = {
        "fPIC": True,
        "with_unit_tests": False,
        "ninja": True
    }
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "FindCityHash.cmake"
    no_copy_source = True
    build_policy = "missing"

    def configure(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build_requiments(self):
        if self.options.ninja:
            self.build_requires("ninja/1.9.0")

    def build(self):
        build_type = "RelWithDebInfo" if self.settings.build_type == "Release" else "Debug"
        gen = "Ninja" if self.options.ninja == True else None
        cmake = CMake(self, build_type=build_type, generator=gen, msbuild_verbosity='normal')
        cmake.verbose = True
        if self.options.with_unit_tests:
            cmake.definitions["WITH_UNIT_TESTS"] = "ON"
        if self.settings.get_safe("compiler.runtime") in ("MT", "MTd"):
            cmake.definitions["MSVC_STATIC_RUNTIME"] = "ON"
        cmake.configure()
        cmake.build()
        if self.options.with_unit_tests:
            if cmake.is_multi_configuration:
                self.run("ctest --output-on-failure --build-config %s" % build_type)
            else:
                self.run("ctest --output-on-failure")
        cmake.install()

    def package(self):
        self.copy("FindCityHash.cmake", dst=".", keep_path=False)
        self.copy("*/cityhash.pdb", dst="bin", keep_path=False)

    def package_id(self):
        self.info.options.with_unit_tests = "any"
        self.info.options.ninja = "any"

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

