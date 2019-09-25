cmake_minimum_required(VERSION 3.8)
project(photo_dens VERSION 1.1.0 LANGUAGES CXX)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release")
endif()

if (CMAKE_BUILD_TYPE EQUAL "Debug")
     message("debug mode")
endif()


add_executable(${PROJECT_NAME}
                src/basis.h
                src/basis.cpp
                src/utils.h
                src/utils.cpp
                src/main.cpp
                )

target_compile_features(${PROJECT_NAME} PUBLIC
                        cxx_std_17)

target_compile_definitions(${PROJECT_NAME} PUBLIC "$<$<CONFIG:DEBUG>:DENSITY_DEBUG>")

target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src )

target_compile_options(${PROJECT_NAME} PRIVATE -Wall -march=native)

find_library(TBB NAMES libtbb.so)

 
target_link_libraries (${PROJECT_NAME} PRIVATE ${TBB})
 