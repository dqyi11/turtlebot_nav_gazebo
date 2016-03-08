#include "tf/message_filter.h"
#include "message_filters/subscriber.h"
#include "tf/transform_datatypes.h"

//#include "geometry_msgs/Twist.h"
//#include "sensor_msgs/LaserScan.h"
//#include "nav_msgs/OccupancyGrid.h"
#include "move_base_msgs/MoveBaseAction.h"
#include "actionlib/client/simple_action_client.h"

#include "turtlebot_navigation_mgr.h"

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

using namespace std;

TurtlebotNavigationMgr::TurtlebotNavigationMgr() {
  m_odom_sub = m_n.subscribe("odom", 1000, &TurtlebotNavigationMgr::odometryCallback, this);

  m_x = -1.0;
  m_y = -1.0;
}

TurtlebotNavigationMgr::~TurtlebotNavigationMgr() {

}

bool TurtlebotNavigationMgr::go_to( double x, double y ) {
  
  move_base_msgs::MoveBaseGoal goal;
  goal.target_pose.header.frame_id = "map";
  goal.target_pose.header.stamp = ros::Time::now();
   
  bool at_target = false;
  int attempts = 0;
  while( false==at_target && attempts < 10 ) {
    attempts ++;
 
    goal.target_pose.pose.position.x = x;
    goal.target_pose.pose.position.y = y;
  
    geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(0);
    goal.target_pose.pose.orientation = odom_quat;

    ROS_INFO("move to x=%f , y=%f", x , y ); 

    MoveBaseClient ac("move_base", true);
  
    while( !ac.waitForServer( ros::Duration(10.0) )) {
      ROS_INFO("waiting for the move_base action"); 
    }
  
    ac.sendGoal(goal);
    ac.waitForResult(ros::Duration(30));
    if( ac.getState() != actionlib::SimpleClientGoalState::SUCCEEDED ) {
      update_state();
    }
    else {
      at_target = true;
      ROS_INFO("arrived");
    }
    std::cout << "Attemps " << attempts << std::endl;
  }
  if( at_target ) {
    return true;
  }
  return false;
}

void TurtlebotNavigationMgr::update_state() {
  tf::StampedTransform transform;
  m_listener.waitForTransform("/map", "/odom", ros::Time(0), ros::Duration(3.0));
  m_listener.lookupTransform("/map", "/odom", ros::Time(0), transform);
  ROS_INFO("At x= %f , y= %f", transform.getOrigin().x(), transform.getOrigin().y() );
 
}
 
void TurtlebotNavigationMgr::odometryCallback(const nav_msgs::Odometry::ConstPtr& msg) {
  double m_x = msg->pose.pose.position.x;
  double m_y = msg->pose.pose.position.y; 
}
