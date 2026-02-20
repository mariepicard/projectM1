add_executable(posc
    main.cpp
    tools.cpp
    sketch_matrix.cpp
    union_hashes.cpp
)

target_include_directories(posc
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/headers
)

find_package(nlohmann_json)


# Link SDSL
target_link_libraries(posc
    PRIVATE
        sdsl
        nlohmann_json::nlohmann_json
)

