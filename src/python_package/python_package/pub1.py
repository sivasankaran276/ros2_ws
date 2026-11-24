import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int16
class pubnode(Node):
    def __init__(self):
        super().__init__("ros_viewing_node")
        self.pub1=self.create_publisher(Int16,"number",10)
        self.create_timer(2.0,self.pub_callback)
    def pub_callback(self):
        msg=Int16()
        msg.data=10
        self.pub1.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node=pubnode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

        