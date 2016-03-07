#ifndef PATH_FOLLOWER_H_
#define PATH_FOLLOWER_H_

#include <string>

#include "tf/transform_broadcaster.h"
#include "tf/transform_listener.h"
#include "tf/message_filter.h"
#include "message_filters/subscriber.h"
#include "tf/transform_datatypes.h"

class PathFollower {
public:
  PathFollower();
  virtual ~PathFollower();
  
  void load_file( std::string filename );
  void spin();
protected:
  ros::NodeHandle  m_nh;
  ros::Subscriber  m_frontier_sub;
  tf::TransformListener *m_tf_listener;
};


#endif // PATH_FOLLOWER_H_
