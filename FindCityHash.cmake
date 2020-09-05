# FindCityHash.cmake for Conan cityhash package
# Dmitriy Vetutnev, Odant, 2020


# Find include path
find_path(CityHash_INCLUDE_DIR
    NAMES city.h
    PATHS ${CONAN_INCLUDE_DIRS_CITYHASH}
    NO_DEFAULT_PATH
)

# Find library
find_library(CityHash_LIBRARY
    NAMES cityhash
    PATHS ${CONAN_LIB_DIRS_CITYHASH}
    NO_DEFAULT_PATH
)

# Set version
set(CityHash_VERSION_MAJOR 1)
set(CityHash_VERSION_MINOR 1)
set(CityHash_VERSION_PATCH 1)
set(CityHash_VERSION_STRING "${CityHash_VERSION_MAJOR}.${CityHash_VERSION_MINOR}.${CityHash_VERSION_PATCH}")
set(CityHash_VERSION ${CityHash_VERSION_STRING})

# Check variables
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(CityHash
    REQUIRED_VARS CityHash_INCLUDE_DIR CityHash_LIBRARY
    VERSION_VAR CityHash_VERSION
)

# Add imported target
if(CityHash_FOUND AND NOT TARGET CityHash::CityHash)
    add_library(CityHash::CityHash UNKNOWN IMPORTED)
    set_target_properties(CityHash::CityHash PROPERTIES
        IMPORTED_LOCATION ${CityHash_LIBRARY}
        INTERFACE_INCLUDE_DIRECTORIES ${CityHash_INCLUDE_DIR}
        INTERFACE_COMPILE_DEFINITIONS "${CONAN_COMPILE_DEFINITIONS_CITYHASH}"
    )

    set(CityHash_INCLUDE_DIRS ${CityHash_INCLUDE_DIR})
    set(CityHash_LIBRARIES ${CityHash_LIBRARY})
    mark_as_advanced(CityHash_INCLUDE_DIR CityHash_LIBRARY)
    set(CityHash_DEFINITIONS "${CONAN_COMPILE_DEFINITIONS_CITYHASH}")
endif()
