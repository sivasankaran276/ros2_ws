import rclpy
from rclpy.node import Node
from example_interfaces.msg import Float32
import random
class pub_node(Node):
    def __init__(self):
        super().__init__("temp_publisher")
        self.pubtemp = self.create_publisher(Float32,"num",10)
        self.create_timer(2.0,self.pub_callback)
        self.get_logger().info("ros2")

    def pub_callback(self):
        self.temp=random.uniform(1.5 ,100.6)
        msg = Float32()
        msg.data = self.temp
        self.pubtemp.publish(msg)
        self.get_logger().info("published temperature")

def main(args=None):
    rclpy.init(args=args)
    node=pub_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =="__main__":
    main()


