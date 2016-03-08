#include <iostream>
#include <fstream>
#include <sstream>
#include "path_follower.h"
 
using namespace std;
 
PathFollower::PathFollower() {
  m_target_pos_idx = -1;
}

PathFollower::~PathFollower() {

}
  
void PathFollower::load_file( string filename ) {
  ifstream read_file;
  m_target_poses.clear();
  m_target_pos_idx = -1;
  read_file.open( filename );
  if( !read_file.good() ) {
    cout << "FAILED IN OPEN " << filename << endl;
    return;
  }
  std::string line_str;
  while( !read_file.eof() ) {
    getline( read_file , line_str );
    std::cout << line_str << std::endl;
    std::istringstream iss( line_str );
    int x, y;
    if( !( iss >> x >> y ) ){
      break; 
    }
    Pos2D pos;
    pos.x = x;
    pos.y = y;
    std::cout << "READ " << x << " " << y << std::endl;
    m_target_poses.push_back( make_pair( pos, true ) ); 
  }
}

void PathFollower::run() {

  for(unsigned int i=0; i< m_target_poses.size(); i++ ) {
    Pos2D pos = m_target_poses[i]; 
  }

}
