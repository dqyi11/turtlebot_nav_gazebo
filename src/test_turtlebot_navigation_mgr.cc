#include <iostream>
#include "turtlebot_navigation_mgr.h"


int main( int argc, char **argv ) {
  ros::init( argc, argv, "TurtlebotNavigationMgr");
  
  TurtlebotNavigationMgr mgr;
  mgr.go_to(1.5, 0.8);

  return 0;
}
