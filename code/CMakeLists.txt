cmake_minimum_required(VERSION 3.16)

project(POSC
    VERSION 1.0
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# --------------------------------
# Get SDSL as an external library
# --------------------------------
include(FetchContent)

FetchContent_Declare(
    sdsl
    GIT_REPOSITORY https://github.com/simongog/sdsl-lite.git
)

# Makes the library available via add_subdirectory()
FetchContent_MakeAvailable(sdsl)



# move all the binaries and libraries into dedicated directories
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# --------------------------------
# Project sources
# --------------------------------
add_subdirectory(src)
