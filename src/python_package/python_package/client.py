import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class client(Node):
    def __init__(self):
        super().__init__("client is running")
        self.client = self.create_client(AddTwoInts,"add")

    def client_callback(self):
        while rclpy.ok:
            while not self.client.wait_for_service(1,0):
                self.get_logger().warn("waiting for server")
        clt = AddTwoInts.Request()
        clt.a = int(input("enter the number:"))
        clt.b = int(input("enter the number:"))
        future = self.client.call_async(clt)
        rclpy.spin_until_future_complete(self,future)
        response = future.result()
        self.get_logger().info(str(response.sum))

def main(args=None):
    rclpy.init(args=args)
    node = client()
    node.client_callback()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =="__main__":
    main()
