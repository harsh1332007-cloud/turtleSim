#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class TwoTurtles(Node):

    def __init__(self):
        super().__init__("two_turtles")

        self.pose1 = None
        self.pose2 = None

        self.cmd1 = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.cmd2 = self.create_publisher(Twist, "/turtle2/cmd_vel", 10)

        self.create_subscription(Pose, "/turtle1/pose", self.pose1_callback, 10)
        self.create_subscription(Pose, "/turtle2/pose", self.pose2_callback, 10)

        self.timer = self.create_timer(0.05, self.control)

    def pose1_callback(self, msg):
        self.pose1 = msg

    def pose2_callback(self, msg):
        self.pose2 = msg

    def control(self):

        if self.pose1 is None or self.pose2 is None:
            return

        # Move turtle1 forward
        t1 = Twist()
        t1.linear.x = 2.0
        t1.angular.z = 0.5
        self.cmd1.publish(t1)

        # Distance between turtles
        dx = self.pose1.x - self.pose2.x
        dy = self.pose1.y - self.pose2.y

        distance = math.sqrt(dx*dx + dy*dy)

        desired_distance = 0.5   # about 5 cm

        angle_to_target = math.atan2(dy, dx)
        angle_error = angle_to_target - self.pose2.theta

        while angle_error > math.pi:
            angle_error -= 2*math.pi

        while angle_error < -math.pi:
            angle_error += 2*math.pi

        t2 = Twist()

        if distance > desired_distance:
            t2.linear.x = 2.0
        else:
            t2.linear.x = 0.0

        t2.angular.z = 4.0 * angle_error

        self.cmd2.publish(t2)


def main(args=None):
    rclpy.init(args=args)
    node = TwoTurtles()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()