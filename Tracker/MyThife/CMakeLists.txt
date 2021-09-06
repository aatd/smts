cmake_minimum_required(VERSION 3.20)
project(MyThief)

set(CMAKE_CXX_STANDARD 14)

include_directories(../../../../Documents/Arduino/MyThief)

add_executable(MyThief
        config.h
        MyThief.ino)
