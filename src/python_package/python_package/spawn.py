import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
import random
import time

class spawn(Node):
    def __init__(self):
        super().__init__("spawn")
        self.clnt = self.create_client(Spawn,"/spawn")
        self.counter = 0
    def callback(self):
        while rclpy.ok:
            while not self.clnt.wait_for_service(1.0):
                self.get_logger().warn("waiting for server")
            self.cln=Spawn.Request()
            self.cln.x=random.uniform(0.0,10.0)
            self.cln.y=random.uniform(0.0,10.0)
            self.cln.theta=random.uniform(0.0,6.27)
            self.cln.name = "turtle"+str(self.counter)
            self.counter = self.counter+1
            future = self.clnt.call_async(self.cln)
            rclpy.spin_until_future_complete(self,future)
            response = future.result()
            self.get_logger().warn(str(response.name))
            time.sleep(1.0)
            
            
        

def main(args=None):
    rclpy.init(args=args)
    node = spawn()
    node.callback()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()