# ROS 2 Workspace

A hands-on **ROS 2 Humble workspace** containing Python-based robotics exercises, communication concepts, Turtlesim simulations, custom interfaces, and autonomous turtle navigation.

This repository documents my learning and development journey with ROS 2, focusing on node development, inter-node communication, services, robot movement, and autonomous control.

---

## Tech Stack

- **Operating System:** Ubuntu 22.04
- **Middleware:** ROS 2 Humble
- **Programming Language:** Python 3
- **Build System:** Colcon
- **Simulation:** Turtlesim
- **Development Environment:** Visual Studio Code
- **Version Control:** Git and GitHub

---

## Repository Structure

```text
ros2_ws/
│
├── src/
│   │
│   ├── python_package/
│   │   ├── python_package/
│   │   │   ├── publisher.py
│   │   │   ├── subscriber.py
│   │   │   ├── service.py
│   │   │   ├── client.py
│   │   │   ├── turtle.py
│   │   │   ├── turtlebot.py
│   │   │   ├── turtle_spawner.py
│   │   │   └── turtle_controller.py
│   │   │
│   │   ├── package.xml
│   │   ├── setup.py
│   │   └── setup.cfg
│   │
│   ├── turtle_catcher_interfaces/
│   │   ├── msg/
│   │   │   ├── Turtle.msg
│   │   │   └── TurtleArray.msg
│   │   │
│   │   ├── srv/
│   │   │   └── CatchTurtle.srv
│   │   │
│   │   ├── CMakeLists.txt
│   │   └── package.xml
│   │
│   └── my_bringup/
│       ├── launch/
│       │   ├── catch_them_all.launch.xml
│       │   └── my_turtle.launch.xml
│       │
│       ├── CMakeLists.txt
│       └── package.xml
│
└── .gitignore
```

---

## ROS 2 Concepts Practiced

This workspace contains practical implementations of several ROS 2 concepts:

- **Nodes:** Creating independent ROS 2 Python nodes.
- **Topics:** Publisher and subscriber communication.
- **Services:** Service servers and clients.
- **Custom Interfaces:** Creating and using custom message and service definitions.
- **Turtlesim:** Robot movement, spawning, and simulation.
- **Launch Files:** Running multiple ROS 2 nodes together.
- **Robot Control:** Position tracking, distance calculation, and velocity control.

---

## Featured Project: Autonomous Turtle Catch-Them-All

An autonomous Turtlesim project where a main turtle continuously identifies, approaches, and catches randomly spawned target turtles.

### Features

- Automatic target turtle spawning.
- Random target positions and orientations.
- Continuous target tracking.
- Closest-target selection.
- Autonomous movement using linear and angular velocity.
- Distance-based target catching.
- Custom ROS 2 messages and services.
- Live tracking of spawned and caught turtles.
- Endless spawning and catching mode.

### System Architecture

The project consists of three main components:

| Component | Responsibility |
|---|---|
| Turtlesim Node | Provides the simulation environment |
| Turtle Spawner Node | Generates targets and manages their lifecycle |
| Turtle Controller Node | Identifies and autonomously catches targets |

### Custom ROS 2 Interfaces

**1. Turtle.msg**

Stores information about an individual target turtle.

```text
string name
float64 x
float64 y
float64 theta
```

**2. TurtleArray.msg**

Stores an array of target turtles.

```text
Turtle[] turtles
```

**3. CatchTurtle.srv**

Request:

```text
string name
---
bool success
```

The controller sends a target name to the spawner through this service.

### Communication

| Topic / Service | Type | Purpose |
|---|---|---|
| `/turtle1/pose` | Pose | Main turtle position |
| `/turtle1/cmd_vel` | Twist | Main turtle movement |
| `/alive_turtles` | TurtleArray | Active target information |
| `/challenge_status` | String | Catching progress |
| `/spawn` | Spawn service | Spawn target turtles |
| `/kill` | Kill service | Remove target turtles |
| `/catch_turtle` | Custom service | Request target catching |

### Autonomous Control

The controller uses Euclidean distance to identify the nearest target:

\[
d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}
\]

It calculates the target direction and generates linear and angular velocity commands using proportional control.

### Endless Mode Configuration

| Parameter | Value |
|---|---:|
| Spawn frequency | 0.5 Hz |
| Spawn interval | 2 seconds |
| Target selection | Closest first |
| Catch tolerance | 0.5 units |
| Linear gain | 2.0 |
| Angular gain | 6.0 |
| Maximum linear velocity | 4.0 |

The spawning process has no fixed target limit. New turtles continue spawning while the controller attempts to catch existing targets.

---

## Installation and Setup

### Prerequisites

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- Colcon
- Turtlesim

Install the required tools:

```bash
sudo apt update

sudo apt install -y \
python3-colcon-common-extensions \
python3-rosdep \
ros-humble-turtlesim
```

### 1. Clone the repository

```bash
cd ~

git clone https://github.com/sivasankaran276/ros2_ws.git

cd ros2_ws
```

### 2. Source ROS 2 Humble

```bash
source /opt/ros/humble/setup.bash
```

### 3. Install package dependencies

```bash
rosdep install --from-paths src --ignore-src -r -y
```

### 4. Build the workspace

```bash
colcon build --symlink-install
```

### 5. Source the workspace

```bash
source install/setup.bash
```

---

## Running the Project

### Launch Autonomous Catch-Them-All

```bash
ros2 launch my_bringup catch_them_all.launch.xml
```

This starts:

1. Turtlesim simulation.
2. Turtle spawner node.
3. Turtle controller node.

The main turtle automatically starts chasing the spawned targets.

Press `Ctrl + C` in the launch terminal to stop the simulation.

### Launch the Basic Turtlesim Exercise

```bash
ros2 launch my_bringup my_turtle.launch.xml
```

### View Available Python Executables

```bash
ros2 pkg executables python_package
```

### Inspect Custom Interfaces

```bash
ros2 interface show turtle_catcher_interfaces/msg/Turtle
```

```bash
ros2 interface show turtle_catcher_interfaces/msg/TurtleArray
```

```bash
ros2 interface show turtle_catcher_interfaces/srv/CatchTurtle
```

---

## Building Individual Packages

To build the custom interface package:

```bash
colcon build --packages-select turtle_catcher_interfaces
```

To build the Python and bringup packages:

```bash
colcon build --packages-select python_package my_bringup
```

After building, source the workspace:

```bash
source install/setup.bash
```

---

## Learning Objectives

Through this workspace, I aim to strengthen my practical understanding of:

- ROS 2 architecture and communication.
- Python-based robotic software development.
- Custom message and service creation.
- Turtlesim-based robot navigation.
- Autonomous robot movement and control.
- Multi-node system integration.
- Workspace management and Git version control.

---

## Future Improvements

- Improve autonomous navigation and turning behaviour.
- Add better target-spawning and catch-service reliability.
- Prevent uncontrolled growth of active targets.
- Add real-time performance statistics.
- Explore SLAM, Nav2, and multi-robot coordination.

---

## Author

**Sivasankaran G**

GitHub: [@sivasankaran276](https://github.com/sivasankaran276)

LinkedIn: [Sivasankaran G](https://www.linkedin.com/in/sivasankaran-g-/)

---

*This repository is an evolving collection of ROS 2 learning exercises and robotics development projects.*
