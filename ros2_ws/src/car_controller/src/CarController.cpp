#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "std_msgs/msg/float32.hpp"

class CarController : public rclcpp::Node
{
public:
    CarController() : Node("carcontroller")
    {
        // Subscribe to LiDAR scans
        scan_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/scan",
            10,
            std::bind(&CarController::scan_callback, this, std::placeholders::_1)
        );

        // Publish servo angle
        servo_pub_ = this->create_publisher<std_msgs::msg::Float32>(
            "/servo_angle",
            10
        );

        RCLCPP_INFO(this->get_logger(), "CarController started");
    }

private:

    void scan_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg)
    {
        if (msg->ranges.empty()) return;

        float min_distance = std::numeric_limits<float>::infinity();
        int min_index = 0;
        for (size_t i = 0; i < msg->ranges.size(); ++i)
        {
            if (!std::isfinite(msg->ranges[i])) continue;
            if (msg->ranges[i] < min_distance)
            {
                min_distance = msg->ranges[i];
                min_index = i;
            }
        }

        float angle = msg->angle_min + min_index * msg->angle_increment;
        float angle_deg = angle * 180.0 / M_PI;

        float servo_angle = ((angle_deg - msg->angle_min * 180.0 / M_PI) /
                            ((msg->angle_max - msg->angle_min) * 180.0 / M_PI)) * 180.0;

        servo_angle = std::max(0.0f, std::min(180.0f, servo_angle));

        std_msgs::msg::Float32 servo_msg;
        servo_msg.data = servo_angle;

        servo_pub_->publish(servo_msg);

        RCLCPP_INFO(this->get_logger(),
                    "Nearest object at %.2f m, lidar angle: %.1f°, servo angle: %.1f°",
                    min_distance, angle_deg, servo_angle);
    }

    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr servo_pub_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<CarController>());
    rclcpp::shutdown();
    return 0;
}