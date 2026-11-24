import rclpy
from rclpy.node import Node
from siva_interface.srv import Paste
class cus_pub(Node):
    def __init__(self):
        super().__init__("cus_sub")
        self.srv=self.create_client(Paste,"num")

    def callback(self):
        while rclpy.ok():
            while not self.srv.wait_for_service(1.0):
                self.get_logger().info("wating for services")

            self.r=Paste.Request()
            self.r.length=float(input("enter the lenght:"))
            self.r.breadth=float(input("enter the breadth:"))
            future=self.srv.call_async(self.r)
            rclpy.spin_until_future_complete(self,future)
            response=future.result()
            self.get_logger().info(str(response.area))

def main(args=None):
    rclpy.init()
    node=cus_pub()
    node.callback()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__=="__main__":
    main()