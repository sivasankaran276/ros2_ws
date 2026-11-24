import rclpy
from rclpy.node import Node
from siva_interface.srv import Paste
class service(Node):
    def __init__(self):
        super().__init__("service")
        self.srv=self.create_service(Paste,"num",self.srv_callback)
    def srv_callback(self,rqt=Paste.Request,rsp=Paste.Response):
        rsp.area=int(rqt.length*rqt.breadth)
        self.get_logger().info(str(rsp.area))
        return rsp







def main(args=None):
    rclpy.init(args=args)
    node=service()
    rclpy.spin(node)
    rclpy.shutdown()




if __name__=="__main__":
    main()