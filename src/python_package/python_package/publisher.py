import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int32
import random
class pub_node(Node):
    def __init__(self):
        super().__init__("speed_publisher")
        self.publisher=self.create_publisher(Int32,"num",10)
        self.create_timer(1.0,self.pub_callback)

    def pub_callback(self):
        self.temp=int(input("Enter the speed:"))
        msg =  Int32()
        msg.data = self.temp
        self.publisher.publish(msg)
        self.get_logger().info(f"speed published-->{self.temp}")

def main(args=None):
    rclpy.init(args=args)
    node=pub_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()