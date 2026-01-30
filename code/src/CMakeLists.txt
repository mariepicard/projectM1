add_executable(posc
    main.cpp
)

target_include_directories(posc
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/headers
)

# Link SDSL
target_link_libraries(posc
    PRIVATE
        sdsl
)
