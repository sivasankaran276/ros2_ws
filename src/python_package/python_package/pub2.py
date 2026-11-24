import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
class pubnode(Node):
    def __init__(self):
        super().__init__("name_publishing_node")
        self.pub2=self.create_publisher(String,"num",10)
        self.create_timer(1.0,self.pub_pullback)
        self.name = input("input your name")
    def pub_pullback(self):
        msg =String()
        msg.data=self.name
        self.pub2.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node=pubnode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =="__main__":
   main()

