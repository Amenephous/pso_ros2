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
import random
import numpy as np
from geometry_msgs.msg import Twist,Point
from std_msgs.msg import String
import matplotlib.pyplot as plt

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('Drone')
        self.subscription = self.create_subscription(
            Twist,
            'g_best_comparator',
            self.listener_callback,
            10)
        self.subscription = self.create_subscription(
            Twist,
            'goal_position',
            self.listener_callback,
            10)
        #self.publisher = self.create_publisher(Twist, 'g_best', 10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('From Bot_1: "%s"' %msg )
        #self.get_logger().info('From Bot_1: "%f", "%f"' % (msg.linear.x, msg.linear.y))
        
        #new_msg = Twist()
        #new_msg.data = "Message from Bot_1"
        #self.publisher.publish(new_msg)
        
        
        
    







# Define the fitness function to be optimized
def fitness_function(x, y):
    f1 = x+2*-y+3
    f2 = 2*x+y-8
    z = -(f1 ** 2 + f2 ** 2)
    return z
    #term1 = -0.2 * np.sqrt(0.5 * (x**2 + y**2))
    #term2 = 0.5 * (np.cos(2*np.pi*x) + np.cos(2*np.pi*y))
    #return -20*np.exp(term1) - np.exp(term2) + 20 + np.e
    #return -(x**0.2 + y**0.2)


# Define the PSO function
def pso(num_particles, num_iterations):
    # Define the search space
    position_min, position_max = -5.0, 5.0
    velocity_min, velocity_max = -0.05*(position_max-position_min), 0.05*(position_max-position_min)

    # Initialize the particles
    particles = []
    for i in range(num_particles):
        
        position = np.array([random.uniform(position_min, position_max), random.uniform(position_min, position_max)])
        velocity = np.array([random.uniform(velocity_min, velocity_max), random.uniform(velocity_min, velocity_max)])
        particles.append({'position': position, 'velocity': velocity, 'best_position': position})

    # Initialize the global best position
    global_best_position = np.array([random.uniform(position_min, position_max), random.uniform(position_min, position_max)])

    # Create the figure and axes object for the plot
    fig, ax = plt.subplots()

    # Set the x and y limits of the plot
    ax.set_xlim(position_min, position_max)
    ax.set_ylim(position_min, position_max)

    # Iterate over each iteration
    for i in range(num_iterations):
        j = i
        # Update the velocity and position of each particle
        for particle in particles:
            # Update the velocity of the particle
            r1, r2 = random.uniform(0, 1), random.uniform(0, 1)
            cognitive_velocity = 2*r1*(particle['best_position'] - particle['position'])
            social_velocity = 2*r2*(global_best_position - particle['position'])
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
        plot_range = 10
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
        plt.pause(0.05)

    # Return the global best position
    return global_best_position

'''
# Test the PSO function
num_particles = 5
num_iterations = 25
global_best_position = pso(num_particles, num_iterations)
print(f"Global best position: {global_best_position}")



'''


def main(args=None):
    rclpy.init(args=args)

    Drone = MinimalPublisher()

    #rclpy.spin(Drone)
    # Test the PSO function
    num_particles = 5
    num_iterations = 250
    global_best_position = pso(num_particles, num_iterations)
    print(f"Global best position: {global_best_position}")
    rclpy.spin(Drone)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    Drone.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
