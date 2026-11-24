import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from turtlesim.srv import Kill
import time


class turspasub2(Node):

    def __init__(self):
        super().__init__("killer_node")

        self.sub = self.create_subscription(
            String, "add", self.turtle_callback, 10
        )
        self.clnt = self.create_client(Kill, "/kill")
        self.turtle_queue = []

        self.create_timer(0.1, self.killer_callback)

    def turtle_callback(self, msg=String()):
        turtle_name = msg.data
        current_time = time.time()
        kill_time = current_time + 3.0

        self.turtle_queue.append((turtle_name, kill_time))

        self.get_logger().info(
            f"turtle name received: {turtle_name} killed in: {kill_time}"
        )

    def killer_callback(self):
        if len(self.turtle_queue) == 0:
            return

        current_time = time.time()
        rem_turtle = []

        for turtle_name, kill_time in self.turtle_queue:
            if current_time >= kill_time:

                if not self.clnt.service_is_ready():
                    rem_turtle.append((turtle_name, kill_time))
                    continue

                req = Kill.Request()
                req.name = turtle_name
                future = self.clnt.call_async(req)

            else:
                rem_turtle.append((turtle_name, kill_time))

        self.turtle_queue = rem_turtle


def main(args=None):
    rclpy.init(args=args)
    node = turspasub2()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()