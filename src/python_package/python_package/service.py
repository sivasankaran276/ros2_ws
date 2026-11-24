import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class server(Node):
    def __init__(self):
        super().__init__("server is running")
        self.srv = self.create_service(AddTwoInts,"add",self.srv_callback)

    def srv_callback(self,rqt=AddTwoInts.Request,rsp=AddTwoInts.Response):
        rsp=rqt.a+rqt.b
        self.get_logger().info(str(rsp.sum))
        return rsp

def main(args=None):
    rclpy.init(args=args)
    node = server()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
