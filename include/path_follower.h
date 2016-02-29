#ifndef PATH_FOLLOWER_H_
#define PATH_FOLLOWER_H_

class PathFollower {

  void spin();
protected:
  ros::NodeHandle  m_nh;
  ros::Subscriber  m_frontier_sub;
  tf::TransformListener *m_tf_listener;
}


#endif // PATH_FOLLOWER_H_
