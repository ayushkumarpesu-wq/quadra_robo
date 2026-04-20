import rclpy
from rclpy.node import Node
import numpy as np
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float32MultiArray
from hyperdog_msgs.msg import Geometry
from IK.InverseKinematics import InverseKinematics

class InvKin_Node(Node):
    def __init__(self):
        self.IK = InverseKinematics()
        self.joint_angs = Float32MultiArray()
        self.prev_joint_angs = None
        super().__init__("IK_node")
        self.sub_ = self.create_subscription(Geometry, "hyperdog_geometry", self.sub_callback, 30)
        self.pub2STM = self.create_publisher(Float32MultiArray, "hyperdog_jointController/commands", 30)
        self.timerPub = self.create_timer(0.02, self.pub_callback)

    def sub_callback(self, msg):
        eulerAng = np.array([msg.euler_ang.x, msg.euler_ang.y, msg.euler_ang.z])
        fr_coord = np.array([msg.fr.x, msg.fr.y, msg.fr.z])
        fl_coord = np.array([msg.fl.x, msg.fl.y, msg.fl.z])
        br_coord = np.array([msg.br.x, msg.br.y, msg.br.z])
        bl_coord = np.array([msg.bl.x, msg.bl.y, msg.bl.z])

        ang_FR = self.IK.get_FR_joint_angles(fr_coord, eulerAng)
        ang_FL = self.IK.get_FL_joint_angles(fl_coord, eulerAng)
        ang_BR = self.IK.get_BR_joint_angles(br_coord, eulerAng)
        ang_BL = self.IK.get_BL_joint_angles(bl_coord, eulerAng)

        if (not np.any(self.IK.singularity)
                and ang_FR is not None and ang_FL is not None
                and ang_BR is not None and ang_BL is not None):
            # FIXED: removed rad2deg — ros2_control expects RADIANS
            self.joint_angs.data = [
                float(ang_FR[0]), float(ang_FR[1]), float(ang_FR[1] + ang_FR[2]),
                float(ang_FL[0]), float(ang_FL[1]), float(ang_FL[1] + ang_FL[2]),
                float(ang_BR[0]), float(ang_BR[1]), float(ang_BR[1] + ang_BR[2]),
                float(ang_BL[0]), float(ang_BL[1]), float(ang_BL[1] + ang_BL[2]),
            ]
            self.prev_joint_angs = list(self.joint_angs.data)
        elif self.prev_joint_angs is not None:
            self.joint_angs.data = self.prev_joint_angs

    def pub_callback(self):
        if self.joint_angs.data:
            self.pub2STM.publish(self.joint_angs)

def main(args=None):
    rclpy.init(args=args)
    inv_kin = InvKin_Node()
    rclpy.spin(inv_kin)
    inv_kin.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
