import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int32
class sub_node(Node):
    def __init__(self):
        super().__init__("speed_subscribe")
        self.subscribe=self.create_subscription(Int32,"num",self.sub_callback,10)
        self.get_logger().info("speed published")
        

    def sub_callback(self,msg):
        temp = msg .data
        if temp <40:
            status=("normal speed")
        elif temp <=70:
            status=("moderate speed")
        else:
            status=("high speed")
        self.get_logger().info(f"recieved speed = {temp} --> {status}")

def main(args=None):
    rclpy.init(args=args)
    node=sub_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()

        

