cmake_minimum_required(VERSION 3.5)

set(CMAKE_CXX_STANDARD 17)

set(EXTRA_COMPONENT_DIRS App BSP HAL)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(Illumination_FW)