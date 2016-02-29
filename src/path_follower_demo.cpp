#include <ros/ros.h>
#include "path_follower.h"

int main( int argc, char** argv ) {
  ros::init( argc, argv, "path_follower" );
  for( unsigned int i=0; i < argc; i++ ) {
    std::cout << i << " " << argv[i] << std::endl;
  }
  PathFollower follower;  
  if( argc > 1 ) {
    follower.loadFile( argv[1] );
  }
  ros::spin();
  return 0;
}
