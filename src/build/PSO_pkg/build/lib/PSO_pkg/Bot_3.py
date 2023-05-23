import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalNode(Node):

    def __init__(self):
        super().__init__('Bot_3')
        self.subscription = self.create_subscription(
            String,
            'g_best_comparator',
            self.listener_callback,
            10)
        self.subscription = self.create_subscription(
            String,
            'goal_position',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(String, 'g_best', 10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Message from Drone: "%s"' % msg.data)
        new_msg = String()
        new_msg.data = "Message from Bot_3"
        self.publisher.publish(new_msg)

def main(args=None):
    rclpy.init(args=args)
    Bot_3 = MinimalNode()
    rclpy.spin(Bot_3)
    Bot_3.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
