import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
class formula (Node):
    def __init__(self):
        super().__init__("pose_node")
        self.x=None
        self.y=None
        self.theta=None
        self.goalpoints=int(input("enter the number of goals:"))
        self.tur_point=[]
        for i in range (self.goalpoints):
            x = float(input("enter x value = "))
            y = float(input("enter y value = "))
            self.tur_point.append((x,y))
        self.publisher=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.subscriber=self.create_subscription(Pose,"/turtle1/pose",self.callback,10)
        self.timer=self.create_timer(0.1,self.callback1)
        self.get_logger().info("publisher is running")
        self.currentgoal=0
 

    def callback (self,ps):
        self.x = ps.x
        self.y = ps.y
        self.theta= ps.theta

    def callback1 (self):
        msg=Twist()
        if self.currentgoal<self.goalpoints:
            x,y=self.tur_point[self.currentgoal]
            self.dx = ((x)-(self.x))
            self.dy = ((y)-(self.y))
            self.EDl=math.sqrt((self.dx)**2+(self.dy)**2)
            self.ang=math.atan2(self.dy,self.dx)
            atog = self.ang-self.theta
            atog = math.atan2(math.sin(atog),math.cos(atog))
        if self.EDl >=0.1:
            msg.linear.x = self.EDl
            msg.angular.z =atog
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.currentgoal+=1
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node =formula()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ =="__main__":
    main()
