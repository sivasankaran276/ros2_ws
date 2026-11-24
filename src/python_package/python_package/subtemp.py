import rclpy
from rclpy.node import Node
from example_interfaces.msg import Float32
class sub_node(Node):
    def __init__(self):
        super().__init__("temp_subscriber")
        self.subtemp=self.create_subscription(Float32,"num",self.sub_callback,10)
        self.get_logger().info("ros2")

    def sub_callback(self,msg=Float32()):
        temp = msg.data
        if temp < 20:
            status ="Temperature is Low"
        elif temp <=30:
            status ="Temperature is Normal"
        else:
            status ="Temperature is High"
        self.get_logger().info(f"Room temperature = {temp} --> {status}")

def main(args=None):
        rclpy.init(args=args)
        node=sub_node()
        rclpy.spin(node)
        rclpy.shutdown()

if __name__ =="__main__":
    main()
