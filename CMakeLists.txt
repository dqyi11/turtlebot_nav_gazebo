cmake_minimum_required(VERSION 2.8)

project(turtlebot_nav_gazebo)

find_package(catkin REQUIRED COMPONENTS
             roscpp
             tf
             actionlib
             move_base_msgs
            )

include_directories(include
                   )

catkin_package(
  CATKIN_DEPENDS message_runtime
)

include_directories(include
                    ${catkin_INCLUDE_DIRS}
                   )

add_library(turtlebot_nav_mgr_lib src/turtlebot_navigation_mgr.cc)

target_link_libraries(turtlebot_nav_mgr_lib ${catkin_LIBRARIES}
                     )

add_executable(path_follower src/path_follower.cpp
                             src/path_follower_demo.cpp)

add_executable(test_turtlebot_nav_mgr src/test_turtlebot_navigation_mgr.cc)

target_link_libraries(path_follower ${catkin_LIBRARIES}
                                    turtlebot_nav_mgr_lib
                     )

target_link_libraries(test_turtlebot_nav_mgr ${catkin_LIBRARIES}
                                             turtlebot_nav_mgr_lib
                     )
