#ifndef TURTLEBOT_NAVIGATION_MGR_H_
#define TURTLEBOT_NAVIGATION_MGR_H_

#include "ros/ros.h"
#include "tf/transform_broadcaster.h"
#include "tf/transform_listener.h"
#include "nav_msgs/Odometry.h"

class TurtlebotNavigationMgr {
public:
  TurtlebotNavigationMgr();
  virtual ~TurtlebotNavigationMgr();

  bool go_to( double x, double y );
  void update_state();

  void odometryCallback(const nav_msgs::Odometry::ConstPtr& msg);
 
  ros::NodeHandle m_n;
  tf::TransformListener m_listener;
  ros::Subscriber m_odom_sub;
  
  double m_x;
  double m_y;

};

#endif // TURTLEBOT_NAVIGATION_MGR_H_
