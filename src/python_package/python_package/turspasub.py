import rclpy
from rclpy.node import Node
from turtlesim.srv import Kill
from example_interfaces.msg import String
import time


class KillNode(Node):

    def __init__(self):
        super().__init__("kill_node")

        self.subscriber = self.create_subscription(String,"add",self.turtle_callback,10)
        self.kill_clnt = self.create_client(Kill,"/kill")
    

    def turtle_callback(self, msg):

        turtle_name = msg.data

        self.get_logger().info(
            "Subscriber received: " + turtle_name
        )

        
        time.time =+3

        
        while not self.kill_clnt.wait_for_service(1.0):
            self.get_logger().warn(
                "Waiting for kill server..."
            )

        kill_req = Kill.Request()

        kill_req.name = turtle_name

        
        kill_future = self.kill_clnt.call_async(
            kill_req
        )

        rclpy.spin_until_future_complete(
            self,
            kill_future
        )

        self.get_logger().info(
            "Killed: " + turtle_name
        )


def main(args=None):

    rclpy.init(args=args)

    node = KillNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()