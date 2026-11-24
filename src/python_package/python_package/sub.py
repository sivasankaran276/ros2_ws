import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
class sub_node(Node):
    def __init__(self):
        super().__init__("node_viewing_name")
        print("hello")
        self.get_logger().info("ros2")
        self.sub=self.create_subscription(String,"num",self.sub_callback,10)
    def sub_callback(self,msg=String()):
        self.get_logger().info(msg.data)


def main(args=None):
    rclpy.init(args=args)
    node=sub_node()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ =="__main__":
    main()