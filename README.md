# MAR Quadrupled Robot (Quadra Robot)

A quadruped robot simulation using ROS2 Humble and Gazebo.

## Features
- Full quadruped robot simulation in Gazebo
- Keyboard teleoperation (W/A/S/D/X)
- Gamepad teleoperation support
- Inverse Kinematics based motion control
- ROS2 Control integration with ForwardCommandController

## Requirements
- Ubuntu 22.04
- ROS2 Humble
- Gazebo 11
- ros-humble-gazebo-ros2-control
- ros-humble-ros2-control
- ros-humble-ros2-controllers

## Setup
```bash
mkdir -p ~/hyperdog_ws/src
cd ~/hyperdog_ws/src
git clone https://github.com/ayushkumarpesu-wq/MAR_Quadrupled_Robo.git
cd ~/hyperdog_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
```

## Launch Simulation
Terminal 1 - Launch Gazebo:
```bash
source /opt/ros/humble/setup.bash && source ~/hyperdog_ws/install/setup.bash
ros2 launch hyperdog_gazebo_sim hyperdog_gazebo_sim.launch.py
```

Terminal 2 - Load Controllers (wait 25s after Gazebo loads):
```bash
source /opt/ros/humble/setup.bash && source ~/hyperdog_ws/install/setup.bash
ros2 run controller_manager spawner joint_state_broadcaster
ros2 run controller_manager spawner gazebo_joint_controller
```

Terminal 3 - Stand pose:
```bash
ros2 topic pub /gazebo_joint_controller/commands std_msgs/msg/Float64MultiArray \
"data: [0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0]" --rate 50
```

Terminal 4 - Launch control stack:
```bash
source /opt/ros/humble/setup.bash && source ~/hyperdog_ws/install/setup.bash
ros2 launch hyperdog_launch hyperdog.launch.py
```

Terminal 5 - Keyboard teleop:
```bash
source /opt/ros/humble/setup.bash && source ~/hyperdog_ws/install/setup.bash
ros2 run hyperdog_teleop keyboard_teleop.py
```

## Controls
- W: Forward
- S: Backward  
- A: Left
- D: Right
- X: Stop / Rest pose
- Ctrl+C: Quit

## Package Structure
- Quadra_ctrl - Control nodes (cmd_manager, IK_node)
- Quadra_gazebo_sim - Gazebo simulation
- Quadra_launch - Launch files
- Quadra_msgs - Custom messages
- Quadra_teleop - Teleoperation nodes
EOF
