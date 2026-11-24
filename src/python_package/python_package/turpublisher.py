import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
class turpublisher(Node):
    def __init__(self):
        super().__init__("turtle_is_spinninig")
        self.x1 = None
        self.y1 = None
        self.theta = None
        self.x2 =float(input("enter the x2 value:"))
        self.y2 =float(input("enter the y2 value:"))
        self.publisher = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.subscriber = self.create_subscription(Pose,"/turtle1/pose",self.callback ,10)
        self.create_timer(0.1,self.pose_value)
        self.get_logger().info("pose_is_running")
    def callback(self,msg = Pose()):
        self.x1 = msg.x
        self.y1 = msg.y
        self.theta = msg.theta
        self.get_logger().info("pose is creating")
    def pose_value(self):
        msg = Twist()
        self.dx = self.x2 - self.x1
        self.dy = self.y2 - self.y1
        ED = math.sqrt((self.dx)**2+(self.dy)**2)
        AG = math.atan2(self.dy,self.dx)
        THETA = AG - self.theta
        THETA1 = math.atan2(math.sin(THETA),math.cos(THETA))
        if abs(ED) >=0.1:
            msg.linear.x=0.5*ED
            msg.angular.z=2.0*THETA 
        else:
            msg.linear.x =0.0
            msg.angular.z= 0.0
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = turpublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()