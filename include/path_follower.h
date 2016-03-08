#ifndef PATH_FOLLOWER_H_
#define PATH_FOLLOWER_H_

#include <string>

#include "turtlebot_navigation_mgr.h"

struct Pos2D{
  int x;
  int y;
};

class PathFollower : public TurtlebotNavigationMgr {
public:
  PathFollower();
  virtual ~PathFollower();
  
  void load_file( std::string filename );
  void run();
protected:
  std::vector< std::pair<Pos2D, bool> > m_target_poses;
  int                                   m_target_pos_idx;
};


#endif // PATH_FOLLOWER_H_
