#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from hyperdog_msgs.msg import JoyCtrlCmds
import sys
import termios
import tty

# Key mapping for WASDX
MOVE_BINDINGS = {
    'w': (1, 0),   # Forward
    's': (-1, 0),  # Backward
    'a': (0, 1),   # Left
    'd': (0, -1),  # Right
    'x': (0, 0),   # Stop
}

class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__('keyboard_teleop_node')
        self.publisher_ = self.create_publisher(JoyCtrlCmds, 'hyperdog_joy_ctrl_cmd', 10)
        self.cmd = JoyCtrlCmds()
        self.cmd.states = [False, False, False]
        self.cmd.gait_type = 0
        self.cmd.pose.position.z = 120
        self.get_logger().info('Keyboard teleop started. Use W/A/S/D/X keys.')
        self.run()

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def run(self):
        while rclpy.ok():
            key = self.get_key().lower()
            if key in MOVE_BINDINGS:
                move, turn = MOVE_BINDINGS[key]
                if key == 'x':
                    self.cmd.states = [False, False, False]
                else:
                    self.cmd.states = [True, True, False]  # start, walk, no side move
                    self.cmd.gait_step.x = float(move) * 50.0
                    self.cmd.gait_step.y = float(turn) * 50.0
                self.publisher_.publish(self.cmd)
                self.get_logger().info(f'Key: {key} | Move: {move}, Turn: {turn}')
            elif key == '\x03':  # Ctrl-C
                break

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleop()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
