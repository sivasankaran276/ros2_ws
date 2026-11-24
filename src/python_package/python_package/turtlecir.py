import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
class circle(Node):
    def __init__(self):
        super().__init__("turtle_spawned")
        self.turtle = self.create_publisher(Twist,"turtle1/cmd_vel",10)
        self.create_timer(2.0,self.pub_callback)
        self.get_logger().info("turtle_circle")
    def pub_callback(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.linear.y = 2.0
        msg.angular.z = 2.0
        self.turtle.publish(msg)
        self.get_logger().info("turtle_spawned")

def main(args=None):
    rclpy.init(args=args)
    node = circle()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =="__main__":
    main()