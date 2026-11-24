import rclpy
from rclpy.node import Node
class templatenode(Node):
    def __init__(self):
        super().__init__("node_viewing_name")
        print("hello")
        self.get_logger().info("ros2")


def main(args=None):
    rclpy.init(args=args)
    node=templatenode()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ =="__main__":
    main()