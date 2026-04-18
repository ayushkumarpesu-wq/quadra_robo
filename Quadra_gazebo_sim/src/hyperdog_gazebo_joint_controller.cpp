#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32_multi_array.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"

using std::placeholders::_1;

class HyperDogGazeboJointCtrl : public rclcpp::Node
{
public:
    HyperDogGazeboJointCtrl()
    : Node("hyperdog_gazebo_joint_ctrl_node")
    {
        // QoS (important for simulation)
        auto qos = rclcpp::QoS(rclcpp::KeepLast(10)).reliable();

        subscription_ = this->create_subscription<std_msgs::msg::Float32MultiArray>(
            "/hyperdog_jointController/commands", qos,
            std::bind(&HyperDogGazeboJointCtrl::topic_callback, this, _1));

        publisher_ = this->create_publisher<std_msgs::msg::Float64MultiArray>(
            "/gazebo_joint_controller/commands", qos);

        RCLCPP_INFO(this->get_logger(), "Gazebo Joint Controller Node Started");
    }

private:
    void topic_callback(const std_msgs::msg::Float32MultiArray::SharedPtr msg_rx)
    {
        // 🔥 Check size
        if (msg_rx->data.size() != 12) {
            RCLCPP_WARN(this->get_logger(),
                        "Expected 12 joints, got %ld", msg_rx->data.size());
            return;
        }

        std_msgs::msg::Float64MultiArray joint_angles;

        // Convert degrees → radians
        for (const float &ang : msg_rx->data) {
            joint_angles.data.push_back(ang * M_PI / 180.0);
        }

        publisher_->publish(joint_angles);

        // Debug print
        RCLCPP_INFO_THROTTLE(this->get_logger(), *this->get_clock(), 2000,
                             "Publishing joint angles to Gazebo");
    }

    rclcpp::Subscription<std_msgs::msg::Float32MultiArray>::SharedPtr subscription_;
    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr publisher_;
};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<HyperDogGazeboJointCtrl>());
    rclcpp::shutdown();
    return 0;
}