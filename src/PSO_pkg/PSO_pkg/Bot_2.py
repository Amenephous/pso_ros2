import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Point
import random
import numpy as np



class Bot2Node(Node):

    def __init__(self):
        super().__init__('bot_2')
        
        self.publisher_ = self.create_publisher(Point, 'bot_2_point', 10)
        self.publisher_twist = self.create_publisher(Twist, 'bot_2_twist', 10)
        
        self.publisher_ = self.create_publisher(Point, 'bot_5_point', 10)
        self.publisher_twist = self.create_publisher(Twist, 'bot_5_twist', 10)
        
        
        self.subs_point_2 = self.create_subscription(
            Point, f'bot_2_point_update', self.point_callback, 10)
        self.subs_twist_2 = self.create_subscription(
            Twist, f'bot_2_twist_update', self.twist_callback, 10)
        
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        
    def point_callback(self, msg):
        self.get_logger().info(f'Received Point: x={msg.x}, y={msg.y}')
        
    def twist_callback(self, msg):
        self.get_logger().info(f'Received Twist: x={msg.linear.x}, y={msg.linear.y}')
        
    
    def timer_callback(self):
        random.seed(2)
        point_msg = Point()
        point_msg.x = random.uniform(-10, 10)
        point_msg.y = random.uniform(-10, 10)
        self.publisher_.publish(point_msg)
        
        twist_msg = Twist()
        twist_msg.linear.x = random.uniform(-5, 5)
        twist_msg.linear.y = random.uniform(-5, 5)
        self.publisher_twist.publish(twist_msg)
        
        self.get_logger().info('Publishing Point: x=%f, y=%f' % (point_msg.x, point_msg.y))
        self.get_logger().info('Publishing Twist: x=%f, y=%f' % (twist_msg.linear.x, twist_msg.linear.y))
        
        #self.timer.cancel()  # stop the timer
        #self.destroy_node()
        
def main(args=None):
    rclpy.init(args=args)
    bot_2 = Bot2Node()
    rclpy.spin(bot_2)
    bot_2.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

