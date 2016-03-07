cmake_minimum_required(VERSION 2.8)

project(turtlebot_nav_gazebo)

find_package(catkin REQUIRED COMPONENTS
             roscpp
            )

include_directories(include
                   )

catkin_package(
  CATKIN_DEPENDS message_runtime
)

add_executable(path_follower src/path_follower.cpp
                             src/path_follower_demo.cpp)

target_link_libraries(path_follower ${catkin_LIBRARIES}
                     )
