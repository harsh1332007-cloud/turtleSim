import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import tty
import termios

class KeyboardTurtle(Node):
    def __init__(self):
        super().__init__('keyboard_turtle')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.speed = 2.0
        self.turn = 1.5

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
        return key

    def run(self):
        print("W = Forward")
        print("S = Backward")
        print("A = Turn Left")
        print("D = Turn Right")
        print("Q = Quit")

        while True:
            key = self.get_key()
            msg = Twist()

            if key == 'w':
                msg.linear.x = self.speed
                print("Moving Forward")
            elif key == 's':
                msg.linear.x = -self.speed
                print("Moving Backward")
            elif key == 'a':
                msg.angular.z = self.turn
                print("Turning Left")
            elif key == 'd':
                msg.angular.z = -self.turn
                print("Turning Right")
            elif key == 'q':
                print("Quitting...")
                break
            else:
                msg.linear.x = 0.0
                msg.angular.z = 0.0
                print("Stopped")

            self.pub.publish(msg)

def main():
    rclpy.init()
    node = KeyboardTurtle()
    node.run()
    rclpy.shutdown()

main()