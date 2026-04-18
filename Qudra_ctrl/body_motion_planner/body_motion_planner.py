import numpy as np
import time

class BodyMotionPlanner():

    def __init__(self, cmd, leg, body, gait_planner):
        self.cmd = cmd
        self.body = body
        self.leg = leg
        self.gait = gait_planner

        self.is_standing = False
        self.prev_slant = self.cmd.body.slant

        # Link lengths
        self.__L1 = self.leg.physical._L1
        self.__L2 = self.leg.physical._L2
        self.__L3 = self.leg.physical._L3

        # Initialize foot Y offset
        self.cmd.leg.foot_zero_pnt[:, 1] = self.__L1

    # -------------------------------
    # Lying Pose (SAFE STATE)
    # -------------------------------
    def set_lying_pose(self):
        self.body.roll = 0
        self.body.pitch = 0
        self.body.yaw = 0

        self.cmd.body.height = 80  # rest height

        # Set Z for all legs
        self.cmd.leg.foot_zero_pnt[:, 2] = self.cmd.body.height

        # Apply to all legs
        self.leg.FR.pose.cur_coord[:] = self.cmd.leg.foot_zero_pnt[0, :]
        self.leg.FL.pose.cur_coord[:] = self.cmd.leg.foot_zero_pnt[1, :]
        self.leg.BR.pose.cur_coord[:] = self.cmd.leg.foot_zero_pnt[2, :]
        self.leg.BL.pose.cur_coord[:] = self.cmd.leg.foot_zero_pnt[3, :]

        self.is_standing = False
        return True

    # -------------------------------
    # Initial Standing Pose
    # -------------------------------
    def set_init_pose(self):
        self.body.roll = 0
        self.body.pitch = 0
        self.body.yaw = 0

        self.cmd.leg.foot_zero_pnt[:, 2] = self.cmd.body.height

        self.leg.FR.pose.cur_coord[:] = self.cmd.leg.foot_zero_pnt[0, :]
        self.leg.FL.pose.cur_coord[:] = self.cmd.leg.foot_zero_pnt[1, :]
        self.leg.BR.pose.cur_coord[:] = self.cmd.leg.foot_zero_pnt[2, :]
        self.leg.BL.pose.cur_coord[:] = self.cmd.leg.foot_zero_pnt[3, :]

        return True

    # -------------------------------
    # Change Height
    # -------------------------------
    def change_height(self):
        z = self.cmd.body.height

        self.leg.FR.pose.cur_coord[2] = z
        self.leg.FL.pose.cur_coord[2] = z
        self.leg.BR.pose.cur_coord[2] = z
        self.leg.BL.pose.cur_coord[2] = z

        return True

    # -------------------------------
    # MAIN LOOP
    # -------------------------------
    def run(self):
        while True:
            if self.cmd.mode.start:
                if not self.is_standing:
                    self.set_init_pose()
                    self.is_standing = True

                # Update body orientation
                self.body.roll = self.cmd.body.roll
                self.body.pitch = self.cmd.body.pitch
                self.body.yaw = self.cmd.body.yaw

                # Update foot positions
                self.cmd.leg.foot_zero_pnt[:, 2] = self.cmd.body.height
                self.cmd.leg.foot_zero_pnt[:, 1] = self.__L1

                self.leg.FR.pose.cur_coord[:] = (
                    self.cmd.leg.foot_zero_pnt[0, :] +
                    self.gait.FR_traj +
                    self.body.ZMP_handler[0, :] * np.array([0, 1, 0])
                )

                self.leg.FL.pose.cur_coord[:] = (
                    self.cmd.leg.foot_zero_pnt[1, :] +
                    self.gait.FL_traj +
                    self.body.ZMP_handler[1, :] * np.array([0, 1, 0])
                )

                self.leg.BR.pose.cur_coord[:] = (
                    self.cmd.leg.foot_zero_pnt[2, :] +
                    self.gait.BR_traj +
                    self.body.ZMP_handler[2, :] * np.array([0, 1, 0])
                )

                self.leg.BL.pose.cur_coord[:] = (
                    self.cmd.leg.foot_zero_pnt[3, :] +
                    self.gait.BL_traj +
                    self.body.ZMP_handler[3, :] * np.array([0, 1, 0])
                )

            else:
                self.set_lying_pose()

            time.sleep(0.002)  # stable loop (500 Hz)