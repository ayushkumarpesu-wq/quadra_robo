# Quadruped Robot ROS2 Project

This project provides a ROS 2 (Humble) and Gazebo Classic simulation for a quadruped robot, including control, teleoperation, and simulation packages.

## Features
- Modular ROS 2 packages for robot control, simulation, and teleoperation
- Inverse kinematics and gait generation for walking
- Keyboard teleoperation (W/A/S/D/X keys)
- Gazebo Classic simulation integration

## Packages Overview
- **hyperdog_msgs**: Custom message definitions for robot control
- **hyperdog_ctrl**: Main control logic, including body motion and gait planning
- **hyperdog_teleop**: Teleoperation nodes (gamepad and keyboard)
- **hyperdog_gazebo_sim**: Gazebo Classic simulation files and launch scripts
- **hyperdog_launch**: Launch files to start the full robot stack

## Quick Start

### 1. Build the Workspace
```bash
mkdir -p ~/hyperdog_ws/src
cd ~/hyperdog_ws/src
# Copy or clone this repository here
cd ~/hyperdog_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
```

### 2. Launch the Robot in Gazebo
```bash
ros2 launch hyperdog_gazebo_sim hyperdog_gazebo_sim.launch.py
```

### 3. Launch the Robot Control Stack
```bash
ros2 launch hyperdog_launch hyperdog.launch.py
```

### 4. Teleoperate the Robot
#### Keyboard (W/A/S/D/X):
```bash
ros2 run hyperdog_teleop keyboard_teleop.py
```
- **W**: Forward
- **S**: Backward
- **A**: Left
- **D**: Right
- **X**: Stop

#### Gamepad:
- Connect a supported gamepad and use the default teleop node.

## Robot Behavior
- On startup, the robot spawns in Gazebo and stands at a safe height.
- Use teleop (keyboard or gamepad) to make the robot walk in any direction.
- Press 'X' to stop and make the robot return to a rest pose.

## Troubleshooting
- Ensure all dependencies are installed with `rosdep`.
- If the robot does not move, check that all nodes are running and topics are being published.
- For simulation issues, verify Gazebo Classic is installed and sourced.

## Customization
- Adjust standing/rest heights in cmd_manager_node.py and body_motion_planner.py as needed.
- Modify gait parameters in `hyperdog_ctrl` for different walking styles.

## License
This project is for educational use. Replace or update this section as needed.

---
