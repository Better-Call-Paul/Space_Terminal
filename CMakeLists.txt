cmake_minimum_required(VERSION 3.14)
project(SatelliteTerminal)  


set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


find_package(Boost 1.70 REQUIRED COMPONENTS system)

if (Boost_FOUND)
    message(STATUS "Boost version: ${Boost_VERSION}")
    message(STATUS "Boost include directory: ${Boost_INCLUDE_DIRS}")
    message(STATUS "Boost libraries: ${Boost_LIBRARIES}")
else()
    message(FATAL_ERROR "Boost not found!")
endif()


find_package(CURL REQUIRED)

if (CURL_FOUND)
    message(STATUS "CURL version: ${CURL_VERSION}")
    message(STATUS "CURL include directory: ${CURL_INCLUDE_DIRS}")
    message(STATUS "CURL libraries: ${CURL_LIBRARIES}")
else()
    message(FATAL_ERROR "libcurl not found!")
endif()


add_executable(SatelliteTerminal src/main.cpp)  

target_include_directories(SatelliteTerminal PRIVATE ${Boost_INCLUDE_DIRS})


target_link_libraries(SatelliteTerminal PRIVATE Boost::system)


target_link_libraries(SatelliteTerminal PRIVATE CURL::libcurl)
