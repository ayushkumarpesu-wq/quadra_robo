#include "rclcpp/rclcpp.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "hyperdog_msgs/msg/joy_ctrl_cmds.hpp"

using std::placeholders::_1;

class FakeOdom : public rclcpp::Node
{
public:
    FakeOdom()
    : Node("fake_odom_node"), odom_x(0.0), odom_y(0.0), odom_rot(0.0)
    {
        auto qos = rclcpp::QoS(rclcpp::KeepLast(10)).reliable();

        sub_ = this->create_subscription<hyperdog_msgs::msg::JoyCtrlCmds>(
            "/hyperdog_joy_ctrl_cmd", qos,
            std::bind(&FakeOdom::topic_callback, this, _1));

        pub_ = this->create_publisher<nav_msgs::msg::Odometry>("/odom", qos);

        RCLCPP_INFO(this->get_logger(), "Fake Odom Node Started");
    }

private:
    double odom_x;
    double odom_y;
    double odom_rot;

    void topic_callback(const hyperdog_msgs::msg::JoyCtrlCmds::SharedPtr msg)
    {
        double x = msg->gait_step.x / 1000.0;
        double y = msg->gait_step.y / 1000.0;
        bool side_walk = msg->states[2];

        // Update position
        if (!side_walk) {
            odom_x += x;
            odom_y += y;
        } else {
            odom_x += x;
            odom_y += y / 2.0;
            odom_rot += y;
        }

        // Normalize rotation
        const double pi = 3.14159265359;
        if (odom_rot > pi) odom_rot -= 2 * pi;
        if (odom_rot < -pi) odom_rot += 2 * pi;

        // Convert yaw → quaternion
        double qz = sin(odom_rot / 2.0);
        double qw = cos(odom_rot / 2.0);

        nav_msgs::msg::Odometry odom;

        odom.header.stamp = this->get_clock()->now();
        odom.header.frame_id = "odom";
        odom.child_frame_id = "base_link";

        odom.pose.pose.position.x = odom_x;
        odom.pose.pose.position.y = odom_y;
        odom.pose.pose.position.z = 0.0;

        odom.pose.pose.orientation.x = 0.0;
        odom.pose.pose.orientation.y = 0.0;
        odom.pose.pose.orientation.z = qz;
        odom.pose.pose.orientation.w = qw;

        pub_->publish(odom);

        RCLCPP_INFO_THROTTLE(this->get_logger(), *this->get_clock(), 2000,
                             "Odom: x=%.2f y=%.2f yaw=%.2f", odom_x, odom_y, odom_rot);
    }

    rclcpp::Subscription<hyperdog_msgs::msg::JoyCtrlCmds>::SharedPtr sub_;
    rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr pub_;
};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<FakeOdom>());
    rclcpp::shutdown();
    return 0;
}