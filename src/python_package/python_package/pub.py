import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
class pubnode(Node):
    def __init__(self):
        super().__init__("ros_viewing_node")
        self.pub=self.create_publisher(Int64,"num",10)
        self.create_timer(1.0,self.pub_callback)
    def pub_callback(self):
        msg=Int64()
        msg.data=1
        self.pub.publish(msg)
        

def main(args=None):
    rclpy.init(args=args)
    node=pubnode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__=="__main__":
    main()
