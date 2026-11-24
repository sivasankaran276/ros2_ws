
#!/usr/bin/env python3

import math
import random
from functools import partial

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from turtlesim.srv import Kill, Spawn

from turtle_catcher_interfaces.msg import Turtle, TurtleArray
from turtle_catcher_interfaces.srv import CatchTurtle


class TurtleSpawnerNode(Node):

    def __init__(self):
        super().__init__('turtle_spawner')

        # 1. Declare parameters
        self.declare_parameter('spawn_frequency', 0.5)
        self.declare_parameter('turtle_name_prefix', 'target_turtle')

        # 2. Get parameter values
        self.spawn_frequency_ = self.get_parameter(
            'spawn_frequency').value

        self.turtle_prefix_ = self.get_parameter(
            'turtle_name_prefix').value

        # 3. Initialize variables
        self.spawned_count_ = 0
        self.caught_count_ = 0
        self.alive_turtles_ = []

        self.start_time_ = self.get_clock().now()

        # 4. Create publishers
        self.alive_turtles_pub_ = self.create_publisher(
            TurtleArray, 'alive_turtles', 10
        )

        self.status_pub_ = self.create_publisher(
            String, 'challenge_status', 10
        )

        # 5. Create catch service server
        self.catch_turtle_srv_ = self.create_service(
            CatchTurtle,
            'catch_turtle',
            self.callback_catch_turtle
        )

        # 6. Create service clients
        self.spawn_client_ = self.create_client(Spawn, 'spawn')
        self.kill_client_ = self.create_client(Kill, 'kill')

        # 7. Create timer for continuous spawning
        self.spawn_timer_ = self.create_timer(
            1.0 / self.spawn_frequency_,
            self.spawn_new_turtle
        )

        self.get_logger().info(
            'TurtleSpawner started: ENDLESS MODE ENABLED!'
        )

    # Publish all currently alive turtles
    def publish_alive_turtles(self):

        msg = TurtleArray()
        msg.turtles = self.alive_turtles_

        self.alive_turtles_pub_.publish(msg)

    # Continuously spawn new turtles
    def spawn_new_turtle(self):

        self.spawned_count_ += 1

        name = f'{self.turtle_prefix_}_{self.spawned_count_}'

        x = random.uniform(1.0, 10.0)
        y = random.uniform(1.0, 10.0)
        theta = random.uniform(0.0, 2.0 * math.pi)

        self.call_spawn_server(name, x, y, theta)

    # Call turtlesim Spawn service
    def call_spawn_server(self, turtle_name, x, y, theta):

        while not self.spawn_client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Waiting for /spawn service...')

        req = Spawn.Request()

        req.x = x
        req.y = y
        req.theta = theta
        req.name = turtle_name

        future = self.spawn_client_.call_async(req)

        future.add_done_callback(
            partial(
                self.callback_call_spawn,
                turtle_name=turtle_name,
                x=x,
                y=y,
                theta=theta
            )
        )

    # Process Spawn service response
    def callback_call_spawn(self, future, turtle_name, x, y, theta):

        try:
            response = future.result()

            if response.name:

                new_turtle = Turtle()

                new_turtle.name = response.name
                new_turtle.x = x
                new_turtle.y = y
                new_turtle.theta = theta

                self.alive_turtles_.append(new_turtle)

                self.publish_alive_turtles()

                self.get_logger().info(
                    f'Spawned {response.name} | '
                    f'Total spawned: {self.spawned_count_}'
                )

        except Exception as e:
            self.get_logger().error(
                f'Spawn service call failed: {e}'
            )

    # Receive CatchTurtle request
    def callback_catch_turtle(self, request, response):

        self.call_kill_server(request.name)

        response.success = True

        return response

    # Call turtlesim Kill service
    def call_kill_server(self, turtle_name):

        while not self.kill_client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Waiting for /kill service...')

        req = Kill.Request()
        req.name = turtle_name

        future = self.kill_client_.call_async(req)

        future.add_done_callback(
            partial(
                self.callback_call_kill,
                turtle_name=turtle_name
            )
        )

    # Process Kill service response
    def callback_call_kill(self, future, turtle_name):

        try:
            future.result()

            for idx, turtle in enumerate(self.alive_turtles_):

                if turtle.name == turtle_name:

                    del self.alive_turtles_[idx]

                    self.caught_count_ += 1

                    self.publish_alive_turtles()

                    elapsed = (
                        self.get_clock().now() - self.start_time_
                    ).nanoseconds / 1e9

                    status_msg = String()

                    status_msg.data = (
                        f'RUNNING | '
                        f'Spawned: {self.spawned_count_} | '
                        f'Caught: {self.caught_count_} | '
                        f'Alive: {len(self.alive_turtles_)} | '
                        f'Elapsed: {elapsed:.1f}s'
                    )

                    self.status_pub_.publish(status_msg)

                    self.get_logger().info(
                        f'Caught {turtle_name}! '
                        f'Total caught: {self.caught_count_} | '
                        f'Currently alive: {len(self.alive_turtles_)}'
                    )

                    break

        except Exception as e:
            self.get_logger().error(
                f'Kill service call failed: {e}'
            )


def main(args=None):

    rclpy.init(args=args)

    node = TurtleSpawnerNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
