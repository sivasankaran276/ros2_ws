import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
class posesub(Node):
    def __init__(self):
        super().__init__("pose_subsrciber")
        self.pose_subscriber = self.create_subscription(Pose,"turtle1/pose",self.sub_callback,10)


    def sub_callback(self,msg : Pose):
        self.get_logger().info("(" + str(msg.x) + ", " + str(msg.y) + ")")

def main(args=None):
    rclpy.init(args=args)
    node = posesub()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =="__main__":
    main()