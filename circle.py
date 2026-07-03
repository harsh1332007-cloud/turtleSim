import rclpy
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions
from geometry_msgs.msg import Twist

class CircleMover(Node):
    def __init__(self):
        super().__init__('circle_mover')

        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.move_circle)

    def move_circle(self):
        msg = Twist()
        msg.linear.x = 2.0      # Forward speed
        msg.angular.z = 1.0     # Turning speed
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)
    node = CircleMover()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        stop_msg = Twist()
        node.publisher.publish(stop_msg)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
