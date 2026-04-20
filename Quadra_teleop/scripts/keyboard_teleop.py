#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from hyperdog_msgs.msg import JoyCtrlCmds
import sys, termios, tty

MOVE_BINDINGS = {
    "w": (1, 0),
    "s": (-1, 0),
    "a": (0, 1),
    "d": (0, -1),
    "x": (0, 0),
}

class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__("keyboard_teleop_node")
        self.publisher_ = self.create_publisher(JoyCtrlCmds, "hyperdog_joy_ctrl_cmd", 10)
        self.cmd = JoyCtrlCmds()
        self.cmd.states = [False, False, False]
        self.cmd.gait_type = 0
        self.cmd.pose.position.z = 120.0
        self.get_logger().info("Keyboard teleop started. W/A/S/D=move, X=stop/rest, Ctrl-C=quit")

    def get_key(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

    def run(self):
        while rclpy.ok():
            key = self.get_key().lower()
            if key in MOVE_BINDINGS:
                move, turn = MOVE_BINDINGS[key]
                if key == "x":
                    self.cmd.states = [False, False, False]
                    self.cmd.gait_step.x = 0.0
                    self.cmd.gait_step.y = 0.0
                    self.cmd.pose.position.z = 0.0
                    self.get_logger().info("STOP - returning to rest pose")
                else:
                    self.cmd.states = [True, True, False]
                    self.cmd.gait_step.x = float(move) * 50.0
                    self.cmd.gait_step.y = float(turn) * 50.0
                    self.cmd.pose.position.z = 120.0
                    self.get_logger().info(f"Key: {key}")
                self.publisher_.publish(self.cmd)
            elif key == "":
                break

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleop()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
