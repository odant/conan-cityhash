# Build CitiHash with CMake
# DmitriyVetutnev, ODANT 2020

cmake_minimum_required(VERSION 3.0)
set(CMAKE_USER_MAKE_RULES_OVERRIDE ${CMAKE_CURRENT_SOURCE_DIR}/c_as_cxx_extensions.cmake)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED)
set(CMAKE_CXX_EXTENSIONS OFF)
project(CityHash VERSION 1.1.1 LANGUAGES CXX)

if(UNIX)
    foreach (flag_var
                 CMAKE_C_FLAGS CMAKE_C_FLAGS_DEBUG CMAKE_C_FLAGS_RELEASE
                 CMAKE_C_FLAGS_MINSIZEREL CMAKE_C_FLAGS_RELWITHDEBINFO
                 CMAKE_CXX_FLAGS CMAKE_CXX_FLAGS_DEBUG CMAKE_CXX_FLAGS_RELEASE
                 CMAKE_CXX_FLAGS_MINSIZEREL CMAKE_CXX_FLAGS_RELWITHDEBINFO)
        string(REPLACE "-O2" "-O3" ${flag_var} "${${flag_var}}")
    endforeach()
endif()

option(MSVC_STATIC_RUNTIME OFF)
if(MSVC AND MSVC_STATIC_RUNTIME)
    foreach (flag_var
                 CMAKE_C_FLAGS CMAKE_C_FLAGS_DEBUG CMAKE_C_FLAGS_RELEASE
                 CMAKE_C_FLAGS_MINSIZEREL CMAKE_C_FLAGS_RELWITHDEBINFO
                 CMAKE_CXX_FLAGS CMAKE_CXX_FLAGS_DEBUG CMAKE_CXX_FLAGS_RELEASE
                 CMAKE_CXX_FLAGS_MINSIZEREL CMAKE_CXX_FLAGS_RELWITHDEBINFO)
        string(REPLACE "/MD" "/MT" ${flag_var} "${${flag_var}}")
    endforeach()
endif()

include(CheckCXXSourceCompiles)
include(CheckIncludeFileCXX)
include(CheckTypeSize)

check_cxx_source_compiles("
int main() {
  return __builtin_expect(0, 1);
}"
HAVE_BUILTIN_EXPECT
)
check_include_file_cxx(dlfcn.h HAVE_DLFCN_H)
check_include_file_cxx(inttypes.h HAVE_INTTYPES_H)
check_include_file_cxx(memory.h HAVE_MEMORY_H)
check_include_file_cxx(stdint.h HAVE_STDINT_H)
check_include_file_cxx(stdlib.h HAVE_STDLIB_H)
check_include_file_cxx(strings.h HAVE_STRINGS_H)
check_include_file_cxx(string.h HAVE_STRING_H)
check_include_file_cxx(sys/stat.h HAVE_SYS_STAT_H)
check_include_file_cxx(sys/types.h HAVE_SYS_TYPES_H)
check_include_file_cxx(unistd.h HAVE_UNISTD_H)
set(STDC_HEADERS)
set(PACKAGE_BUGREPORT "cityhash-discuss@googlegroups.com")
set(PACKAGE_NAME ${PROJECT_NAME})
set(PACKAGE_STRING "${PROJECT_NAME} ${PROJECT_VERSION}")
set(PACKAGE_TARNAME "cityhash")
set(PACKAGE_VERSION ${PROJECT_VERSION})
set(STDC_HEADERS 1)
check_type_size(_UINT32_T _UINT32_T)
if(_UINT32_T)
    unset(_UINT32_T CACHE)
endif()
check_type_size(_UINT64_T _UINT64_T)
if(_UINT64_T)
    unset(_UINT64_T CACHE)
endif()
check_type_size(_UINT8_T _UINT8_T)
if(_UINT8_T)
    unset(_UINT8_T CACHE)
endif()
check_type_size(size_t size_t)
if(size_t)
    unset(size_t CACHE)
endif()
check_type_size(ssize_t ssize_t)
if(ssize_t)
    unset(ssize_t CACHE)
endif()
check_type_size(uint32_t uint32_t)
if(uint32_t)
    unset(uint32_t CACHE)
endif()
check_type_size(uint64_t uint64_t)
if(uint64_t)
    unset(uint64_t CACHE)
endif()
check_type_size(uint8_t uint8_t)
if(uint8_t)
    unset(uint8_t CACHE)
endif()

configure_file(config.h.in.cmake config.h)

include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(src)

add_library(cityhash STATIC src/city.cc)
set_target_properties(cityhash PROPERTIES PUBLIC_HEADER "src/city.h;src/citycrc.h")
install(
    TARGETS cityhash
    LIBRARY DESTINATION lib
    PUBLIC_HEADER DESTINATION include
)

option(WITH_UNIT_TESTS OFF)
if(WITH_UNIT_TESTS)
    enable_testing()
    add_executable(cityhash_unittest src/city-test.cc)
    target_link_libraries(cityhash_unittest cityhash)
    add_test(
        NAME cityhash_unittest
        COMMAND cityhash_unittest
    )
endif()


