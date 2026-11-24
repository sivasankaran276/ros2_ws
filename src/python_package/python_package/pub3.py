import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
class pubnode(Node):
    def __init__(self):
        super().__init__("print_number_series")
        self.pub3=self.create_publisher(String,"num",10)
        self.create_timer(1.0,self.pub_pullback)
        self.n = int(input("enter the number:"))
        self.end=int(input("enter the end num:"))
        self.x=self.n

    def pub_pullback(self):
        
        msg = String()
        for i in range (self.n,self.end+1):
            msg.data = str(self.x)
            self.pub3.publish(msg)
            self.x+=1

        if i == self.end:
            rclpy.shutdown()
            Node.destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node=pubnode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =="__main__":
    main()

