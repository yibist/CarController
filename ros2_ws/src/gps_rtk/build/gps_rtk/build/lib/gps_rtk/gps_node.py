import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
import serial
from pynmeagps import NMEAReader

class NtripRosNode(Node):
    def __init__(self):
        super().__init__('ntrip_ros_node')

        # Parameters
        self.declare_parameter("serial_port", "/dev/ttyAMA0")
        self.declare_parameter("baudrate", 115200)
        self.declare_parameter("publish_rate", 1.0)  # Hz

        port = self.get_parameter("serial_port").get_parameter_value().string_value
        baud = self.get_parameter("baudrate").get_parameter_value().integer_value
        self.publish_rate = self.get_parameter("publish_rate").get_parameter_value().double_value

        # ROS publisher
        self.gps_pub = self.create_publisher(NavSatFix, 'gps/fix', 10)

        # Serial and NMEA
        self.stream = serial.Serial(port, baud, timeout=3)
        self.nmr = NMEAReader(self.stream)

        # Timer to read and publish GPS data
        self.timer = self.create_timer(1.0/self.publish_rate, self.publish_gps)

    def publish_gps(self):
        try:
            raw_data, parsed_data = self.nmr.read()
            if bytes("GNGGA",'ascii') in raw_data:
                # Example: parsed_data.lat, parsed_data.lon, parsed_data.alt
                msg = NavSatFix()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = "gps"

                # NMEAReader lat/lon are in degrees
                msg.latitude = parsed_data.lat
                msg.longitude = parsed_data.lon
                msg.altitude = parsed_data.h_msl  # height above mean sea level

                # Fix status
                msg.status.status = 1  # 1=GPS_FIX
                msg.status.service = 1  # GPS

                self.gps_pub.publish(msg)
        except Exception as e:
            self.get_logger().error(f"Error reading GPS: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = NtripRosNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
