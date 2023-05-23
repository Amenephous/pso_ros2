# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from pyamaze import maze,agent,COLOR,textLabel                  #Download library pyamaze first
from queue import PriorityQueue                                 #Use Priority queue
from math import sqrt    


def h(p1, p2):                                                  #Heuristic
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x1 - x2) + abs(y1 - y2))                        #Manhattan Distance (Comment out Euclidean Distance line for this)
#    return sqrt((x1-x2)**2+(y1-y2)**2)                         #Euclidean Distance (Comment out Manhattan distance line for this)
    
def A_Star(m,start=None):                                       #A Star search algorithm
    if start is None:                                           #When start point is not mentioned, Start from (10,10)
        start=(10,10)

    Track_P = {}
    frontier = PriorityQueue()
    frontier.put((h(start, m._goal), h(start, m._goal), start))
    
    g = {row: float("inf") for row in m.grid}                   #Function of Cost so far 
    g[start] = 0
    f = {row: float("inf") for row in m.grid}                   #Function from cost so far and Heuristics 
    f[start] = h(start, m._goal)
    Path_Finding=[start]
    while not frontier.empty():
        pos = frontier.get()[2]
        Path_Finding.append(pos)
        if pos == m._goal:
            break        
        for d in 'ESNW':                                        #ESNW are East, South, North and West. Directions defined in Pyamaze
            if m.maze_map[pos][d]==True:
                if d=='E':
                    current=(pos[0],pos[1]+1)
                elif d=='W':
                    current=(pos[0],pos[1]-1)
                elif d=='N':
                    current=(pos[0]-1,pos[1])
                elif d=='S':
                    current=(pos[0]+1,pos[1])

                g_t = g[pos] + 1                                #Temporary cost so far
                f_t = g_t + h(current, m._goal)                    #Temporary f

                if f_t < f[current]:                               #If temporary f is less than the f current, then update temporary f as f
                    Track_P[current] = pos
                    g[current] = g_t
                    f[current] = g_t + h(current, m._goal)
                    frontier.put((f[current], h(current, m._goal), current))


    Path={}                                                     #Initialize Path taken


    fin=m._goal
    while fin!=start:
        Path[Track_P[fin]]=fin
        fin=Track_P[fin]
    return Path_Finding,Track_P,Path





class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('Drone')
        
        self.publisher_ = self.create_publisher(String, 'goal_position', 10)
        self.publisher_ = self.create_publisher(String, 'g_best_comparator', 10)
        self.subscription = self.create_subscription(
            String,
            'g_best',
            self.sensor_data_callback,
            10
        )
        self.subscription = self.create_subscription(
            String,
            'Desired_g_best',
            self.sensor_data_callback,
            10
        )
        
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        
        
    
    def timer_callback(self):
        msg = String()
        
        msg.data = None
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
        
    def sensor_data_callback(self, msg):
        self.get_logger().info('Received: "%s"' % msg.data)
        
    def update_stuff(self,val):
    	msg = String()
    	msg.data = str(val)
	
	


def main(args=None):
    
    
    m=maze(10,10)                                                   #Initialize "maze", taken from pyamaze library
    #m.CreateMaze(loadMaze='Class_Setup1.csv',theme='light')         #Class_Setup1 replicates our class
    m.CreateMaze(theme='light')         #Class_Setup1 replicates our class
    
    Path_Finding,Track_P,Path=A_Star(m)                             #A star with (10,10) as start point
    Path_Finding2,Track_P2,Path2=A_Star(m,(10,2))                   #A star with (10,2) as start point
    Path_Finding3,Track_P3,Path3=A_Star(m,(8,8))                    #A star with (8,8) as start point
    
    a = agent(m,footprints=True,color=COLOR.red,filled=True,goal=(1,1))             #For Pathfinding of agent "a"
    aT= agent(m,footprints=True,shape='arrow',color=COLOR.black,goal=(1,1))         #For shortest path of agent "a" 
                                                                                    #Also remove/add shape = 'arrow' according to your preference
    b = agent(m,10,2,footprints=True,color=COLOR.yellow,filled=True,goal=(1,1))     #For Pathfinding of agent "b"
    bT= agent(m,10,2,footprints=True,color=COLOR.red,goal=(1,1))                    #For shortest path of agent "b"
    c = agent(m,8,8,footprints=True,color=COLOR.blue,filled=True,goal=(1,1))        #For Pathfinding of agent "c"
    cT= agent(m,8,8,footprints=True,color=COLOR.blue,goal=(1,1))                    #For shortest path of agent "c"
 
    #m.tracePath({a:Path_Finding},delay=200)                         #To run Path finding Algo for a, Comment out other path finding and vice versa
    m.tracePath({aT:Path},delay=100)                                #Shortest path for a
    #m.tracePath({b:Path_Finding2},delay=200)
    m.tracePath({bT:Path2},delay=100)                               #Shortest path for b
    #m.tracePath({c:Path_Finding3},delay=200)
    m.tracePath({cT:Path3},delay=100)                               #Shortest path for c
    
    #l=textLabel(m,'Blocks searched for a',len(Path_Finding))        #To see the number of blocks searched for a
    #l=textLabel(m,'Blocks searched for b',len(Path_Finding2))      #To see the number of blocks searched for b
    #l=textLabel(m,'Blocks searched for c',len(Path_Finding3))      #To see the number of blocks searched for c
    l=textLabel(m,'Shortest Path length for a',len(Path)+1)         #To see the shortest path transversed for a
    #l=textLabel(m,'Shortest Path length for b',len(Path2)+1)        #To see the shortest path transversed for b
    #l=textLabel(m,'Shortest Path length for c',len(Path3)+1)        #To see the shortest path transversed for c
    
    m.run()
    
    
    Data = l
    rclpy.init(args=args)

    Drone = MinimalPublisher()
    #Drone.update_stuff(l)

    rclpy.spin(Drone)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    Drone.destroy_node()
    rclpy.shutdown()






if __name__ == '__main__':
    main()
