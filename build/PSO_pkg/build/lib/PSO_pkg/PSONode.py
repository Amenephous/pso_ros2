import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Point
import random
import numpy as np
import matplotlib.pyplot as plt



x1,y1 = 0,0
tx1,ty1 = 0,0

x2,y2 = 0,0
tx2,ty2 = 0,0

x3,y3 = 0,0
tx3,ty3 = 0,0

x4,y4 = 0,0
tx4,ty4 = 0,0

x5,y5 = 0,0
tx5,ty5 = 0,0

flag = 0





class PSONode(Node):

    def __init__(self):
        super().__init__('PSO_Node')
        self.subs_point_1 = self.create_subscription(
            Point, f'bot_1_point', self.point_callback_1, 10)
        self.subs_twist_1 = self.create_subscription(
            Twist, f'bot_1_twist', self.twist_callback_1, 10)
            
        self.subs_point_2 = self.create_subscription(
            Point, f'bot_2_point', self.point_callback_2, 10)
        self.subs_twist_2 = self.create_subscription(
            Twist, f'bot_2_twist', self.twist_callback_2, 10)
            
        self.subs_point_3 = self.create_subscription(
            Point, f'bot_3_point', self.point_callback_3, 10)
        self.subs_twist_3 = self.create_subscription(
            Twist, f'bot_3_twist', self.twist_callback_3, 10)        
            
        self.subs_point_4 = self.create_subscription(
            Point, f'bot_4_point', self.point_callback_4, 10)
        self.subs_twist_4 = self.create_subscription(
            Twist, f'bot_4_twist', self.twist_callback_4, 10)
            
        self.subs_point_5 = self.create_subscription(
            Point, f'bot_5_point', self.point_callback_5, 10)
        self.subs_twist_5 = self.create_subscription(
            Twist, f'bot_5_twist', self.twist_callback_5, 10)
            
        self.pubs_point_1 = self.create_publisher(
            Point, f'bot_1_point_update', 10)
        self.pubs_twist_1 = self.create_publisher(
            Twist, f'bot_1_twist_update', 10)
            
        self.pubs_point_2 = self.create_publisher(
            Point, f'bot_2_point_update', 10)
        self.pubs_twist_2 = self.create_publisher(
            Twist, f'bot_2_twist_update', 10)
        
        self.pubs_point_3 = self.create_publisher(
            Point, f'bot_3_point_update', 10)
        self.pubs_twist_3 = self.create_publisher(
            Twist, f'bot_3_twist_update', 10)
        
        self.pubs_point_4 = self.create_publisher(
            Point, f'bot_4_point_update', 10)
        self.pubs_twist_4 = self.create_publisher(
            Twist, f'bot_4_twist_update', 10)
            
        self.pubs_point_5 = self.create_publisher(
            Point, f'bot_5_point_update', 10)
        self.pubs_twist_5 = self.create_publisher(
            Twist, f'bot_5_twist_update', 10)
        
        '''
        self.subscribers = []
        for i in range(1, 6):
            subscriber_point = self.create_subscription(Point, f'bot_{i}_point', self.point_callback, 10)
            subscriber_twist = self.create_subscription(Twist, f'bot_{i}_twist', self.twist_callback, 10)
            self.subscribers.append(subscriber_point)
            self.subscribers.append(subscriber_twist)
        '''
    #1    
    def point_callback_1(self, msg):
    	global x1,y1
    	x1 = msg.x
    	y1 = msg.y
        #self.get_logger().info(f'Received Point: x={msg.x}, y={msg.y}')
        
    def twist_callback_1(self, msg):
    	global tx1 , ty1
    	tx1 = msg.linear.x
    	ty1 = msg.linear.y
        #self.get_logger().info(f'Received Twist: x={msg.linear.x}, y={msg.linear.y}')
        
    #2    
    def point_callback_2(self, msg):
    	global x2,y2
    	x2 = msg.x
    	y2 = msg.y
        #self.get_logger().info(f'Received Point: x={msg.x}, y={msg.y}')
        
    def twist_callback_2(self, msg):
    	global tx2 , ty2
    	tx2 = msg.linear.x
    	ty2 = msg.linear.y
        #self.get_logger().info(f'Received Twist: x={msg.linear.x}, y={msg.linear.y}')
        
    #3    
    def point_callback_3(self, msg):
    	global x3,y3
    	x3 = msg.x
    	y3 = msg.y
        #self.get_logger().info(f'Received Point: x={msg.x}, y={msg.y}')
        
    def twist_callback_3(self, msg):
    	global tx3 , ty3
    	tx3 = msg.linear.x
    	ty3 = msg.linear.y
        #self.get_logger().info(f'Received Twist: x={msg.linear.x}, y={msg.linear.y}')
        
    #4    
    def point_callback_4(self, msg):
    	global x4,y4
    	x4 = msg.x
    	y4 = msg.y
        #self.get_logger().info(f'Received Point: x={msg.x}, y={msg.y}')
        
    def twist_callback_4(self, msg):
    	global tx4 , ty4
    	tx4 = msg.linear.x
    	ty4 = msg.linear.y
        #self.get_logger().info(f'Received Twist: x={msg.linear.x}, y={msg.linear.y}')
        
    #5    
    def point_callback_5(self, msg):
    	global x5,y5
    	x5 = msg.x
    	y5 = msg.y
        #self.get_logger().info(f'Received Point: x={msg.x}, y={msg.y}')
        
    def twist_callback_5(self, msg):
    	global tx5 , ty5
    	tx5 = msg.linear.x
    	ty5 = msg.linear.y
        #self.get_logger().info(f'Received Twist: x={msg.linear.x}, y={msg.linear.y}')
        




# Define the fitness function to be optimized
def fitness_function(x, y):
    f1 = x+2*-y+3
    f2 = 2*x+y-8
    z = -(f1 ** 2 + f2 ** 2)
    return z


# Define the PSO function
def pso(num_particles, num_iterations):
    # Define the search space
   
    position_min, position_max = -5.0, 5.0
    velocity_min, velocity_max = -1*(position_max-position_min), 1*(position_max-position_min)
    random.seed(3)

  

    particles = []  
    for i in range(num_particles):
        position = np.array([(25-10*i),(25-10*i)])
        velocity = np.array([random.uniform(velocity_min, velocity_max), random.uniform(velocity_min, velocity_max)])
        particles.append({'position': position, 'velocity': velocity, 'best_position': position})
    
    

    # Initialize the global best position
    global_best_position = np.array([random.uniform(position_min, position_max), random.uniform(position_min, position_max)])

    # Create the figure and axes object for the plot
    fig, ax = plt.subplots()

    # Set the x and y limits of the plot
    #ax.set_xlim(position_min, position_max)
    #ax.set_ylim(position_min, position_max)

    # Iterate over each iteration
    for i in range(num_iterations):
        j = i
        # Update the velocity and position of each particle
        for particle in particles:
            # Update the velocity of the particle
            r1, r2 = random.uniform(0, 1), random.uniform(0, 1)
            cognitive_velocity = 2*r1*(np.array(particle['best_position']) - np.array(particle['position']))
            social_velocity = 2*r2*(np.array(global_best_position) - particle['position'])
            particle['velocity'] = 0.5*particle['velocity'] + cognitive_velocity + social_velocity

            # Update the position of the particle
            particle['position'] = particle['position'] + particle['velocity']

            # Update the best position of the particle
            if fitness_function(particle['position'][0], particle['position'][1]) > fitness_function(particle['best_position'][0], particle['best_position'][1]):
                particle['best_position'] = particle['position']

            # Update the global best position
            if fitness_function(particle['position'][0], particle['position'][1]) > fitness_function(global_best_position[0], global_best_position[1]):
                global_best_position = particle['position']
                
                
                
                
                
        # Clear the previous plot and update the new positions of the particles
        ax.clear()
        # Set the x and y limits of the plot and adjust scaling
        plot_range = 20.0
        ax.set_xlim(-plot_range, plot_range)
        ax.set_ylim(-plot_range, plot_range)
        ax.set_aspect('equal', adjustable='box')



        # Before the loop, create a list of colors
        colors = ['r', 'b', 'g', 'm', 'c']

        # Inside the loop, use the color of the corresponding index for each particle
        for i, particle in enumerate(particles):
            ax.plot(particle['position'][0], particle['position'][1], marker='o', color=colors[i % len(colors)])

        # Output the position of each particle after each iteration
        
        print(f"Iteration {j+1}:")
        for particle in particles:
            print(f"Particle position: {particle['position']}")

        # Pause the program for a short period to visualize the plot
        
        plt.pause(0.1)

    # Return the global best position
    return global_best_position


  
        
        
def main(args=None):
    rclpy.init(args=args)
    PSO_Node = PSONode()
    # Test the PSO function
    num_particles = 5
    num_iterations = 100
    global_best_position = pso(num_particles, num_iterations)
    print(f"Global best position: {global_best_position}")
    rclpy.spin(PSO_Node)
    PSO_Node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

