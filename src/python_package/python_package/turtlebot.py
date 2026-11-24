import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
class Square(Node):
    def __init__(self):
        super().__init__("turtle_spawned")
        self.turtle = self.create_publisher(Twist,"turtle1/cmd_vel",10)
        time.sleep(2.0)
        for i in range (4):
            self.move_forward()
            self.take_right()
            self.stop()
    def move_forward(self):
        msg = Twist()
        msg.linear.x = 2.0
        start = time.time()
        while (time.time() - start) < 2.0:
            self.turtle.publish(msg)
            time.sleep(0.2)
    def take_right(self):
        ang = Twist()
        ang.angular.z= 1.57
        start = time.time()
        while (time.time() - start) <1.0:
            self.turtle.publish(ang)
            time.sleep(0.2)
    def stop(self):
        msg = Twist()
        msg.linear.x=0.0
        self.turtle.publish(msg)
def main(args=None):
    rclpy.init(args=args)
    node = Square()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == "__main__":
    main()