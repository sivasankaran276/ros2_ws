
#!/usr/bin/env python3

import math
from functools import partial

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from turtle_catcher_interfaces.msg import Turtle, TurtleArray
from turtle_catcher_interfaces.srv import CatchTurtle


class TurtleControllerNode(Node):

    def __init__(self):
        super().__init__('turtle_controller')

        # 1. Declare parameters
        self.declare_parameter('catch_closest_turtle_first', True)
        self.declare_parameter('catch_tolerance', 0.5)
        self.declare_parameter('kp_linear', 2.0)
        self.declare_parameter('kp_angular', 6.0)
        self.declare_parameter('max_linear_vel', 4.0)

        # 2. Get parameter values
        self.catch_closest_ = self.get_parameter(
            'catch_closest_turtle_first').value

        self.catch_tol_ = self.get_parameter(
            'catch_tolerance').value

        self.kp_lin_ = self.get_parameter('kp_linear').value
        self.kp_ang_ = self.get_parameter('kp_angular').value
        self.max_lin_ = self.get_parameter('max_linear_vel').value

        # 3. Initialize variables
        self.pose_ = None
        self.target_turtle_ = None
        self.catching_in_progress_ = False

        # 4. Create publisher
        self.cmd_vel_pub_ = self.create_publisher(
            Twist, 'turtle1/cmd_vel', 10
        )

        # 5. Create subscribers
        self.pose_sub_ = self.create_subscription(
            Pose,
            'turtle1/pose',
            self.callback_pose,
            10
        )

        self.alive_turtles_sub_ = self.create_subscription(
            TurtleArray,
            'alive_turtles',
            self.callback_alive_turtles,
            10
        )

        # 6. Create service client
        self.catch_client_ = self.create_client(
            CatchTurtle, 'catch_turtle'
        )

        # 7. Create control timer
        self.control_timer_ = self.create_timer(
            0.01, self.control_loop
        )

        self.get_logger().info(
            'TurtleController started and waiting for targets.'
        )

    # Receive the main turtle's position
    def callback_pose(self, msg: Pose):
        self.pose_ = msg

    # Receive the list of alive target turtles
    def callback_alive_turtles(self, msg: TurtleArray):

        if not msg.turtles:
            self.target_turtle_ = None
            return

        # Select the closest target
        if self.catch_closest_ and self.pose_ is not None:

            closest = None
            min_dist = float('inf')

            for turtle in msg.turtles:

                dist = math.hypot(
                    turtle.x - self.pose_.x,
                    turtle.y - self.pose_.y
                )

                if dist < min_dist:
                    min_dist = dist
                    closest = turtle

            self.target_turtle_ = closest

        else:
            self.target_turtle_ = msg.turtles[0]

    # Stop the main turtle
    def stop_turtle(self):

        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0

        self.cmd_vel_pub_.publish(cmd)

    # Main movement control loop
    def control_loop(self):

        if (self.pose_ is None or
                self.target_turtle_ is None or
                self.catching_in_progress_):

            self.stop_turtle()
            return

        # Calculate distance to target
        dist_x = self.target_turtle_.x - self.pose_.x
        dist_y = self.target_turtle_.y - self.pose_.y

        distance = math.hypot(dist_x, dist_y)

        # Check whether target is far away
        if distance >= self.catch_tol_:

            # Calculate desired direction
            goal_theta = math.atan2(dist_y, dist_x)

            # Calculate angle error
            angle_error = math.atan2(
                math.sin(goal_theta - self.pose_.theta),
                math.cos(goal_theta - self.pose_.theta)
            )

            # Generate velocity command
            cmd = Twist()

            cmd.linear.x = min(
                self.kp_lin_ * distance,
                self.max_lin_
            )

            cmd.angular.z = self.kp_ang_ * angle_error

            # Publish movement command
            self.cmd_vel_pub_.publish(cmd)

        else:
            # Target reached
            self.stop_turtle()

            self.catching_in_progress_ = True

            self.call_catch_turtle_server(
                self.target_turtle_.name
            )

    # Call the CatchTurtle service
    def call_catch_turtle_server(self, turtle_name: str):

        while not self.catch_client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn(
                'Waiting for /catch_turtle service...'
            )

        req = CatchTurtle.Request()
        req.name = turtle_name

        future = self.catch_client_.call_async(req)

        future.add_done_callback(
            partial(
                self.callback_call_catch_turtle,
                turtle_name=turtle_name
            )
        )

    # Process the CatchTurtle service response
    def callback_call_catch_turtle(self, future, turtle_name: str):

        try:
            response = future.result()

            if not response.success:
                self.get_logger().error(
                    f'Failed to catch {turtle_name}'
                )

            else:
                self.get_logger().info(
                    f'Catch request completed for {turtle_name}'
                )

                # Clear the old target until the updated
                # alive_turtles message arrives
                self.target_turtle_ = None

        except Exception as e:
            self.get_logger().error(
                f'Catch service call failed: {e}'
            )

        finally:
            self.catching_in_progress_ = False


# Main function
def main(args=None):

    rclpy.init(args=args)

    node = TurtleControllerNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.stop_turtle()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
