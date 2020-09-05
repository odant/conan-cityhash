project(PackageTest CXX)
cmake_minimum_required(VERSION 3.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

enable_testing()


# CONAN_PKG imported targets

add_executable(test_cityhash_CONAN_PKG test_cityhash.cpp)
target_link_libraries(test_cityhash_CONAN_PKG CONAN_PKG::cityhash)
add_test(
    NAME test_cityhash_CONAN_PKG
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND test_cityhash_CONAN_PKG
)


# cityhash imported targets

find_package(CityHash REQUIRED)

add_executable(test_cityhash test_cityhash.cpp)
target_link_libraries(test_cityhash CityHash::CityHash)
add_test(
    NAME test_cityhash
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND test_cityhash
)

