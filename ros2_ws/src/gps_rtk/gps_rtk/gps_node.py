#!/usr/bin/env python3

import socket
import base64
import serial
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from pynmeagps import NMEAReader


class NTRIPRosNode(Node):

    def __init__(self):
        super().__init__('ntrip_client')

        # ROS2 publisher
        self.fix_pub = self.create_publisher(NavSatFix, '/gnss/fix', 10)

        # Parameters with defaults
        self.declare_parameter("caster", "")
        self.declare_parameter("port", 2101)
        self.declare_parameter("mountpoint", "")
        self.declare_parameter("username", "")
        self.declare_parameter("password", "")
        self.declare_parameter("serial_port", "/dev/ttyAMA0")
        self.declare_parameter("baudrate", 115200)

        self.caster = self.get_parameter("caster").get_parameter_value().string_value
        self.port = self.get_parameter("port").get_parameter_value().integer_value
        self.mountpoint = self.get_parameter("mountpoint").get_parameter_value().string_value
        self.username = self.get_parameter("username").get_parameter_value().string_value
        self.password = self.get_parameter("password").get_parameter_value().string_value
        self.serial_port = self.get_parameter("serial_port").get_parameter_value().string_value
        self.baudrate = self.get_parameter("baudrate").get_parameter_value().integer_value

        # Serial connection to GNSS receiver
        self.ser = serial.Serial(self.serial_port, self.baudrate, timeout=1)
        self.nmea_reader = NMEAReader(self.ser)

        # NTRIP socket
        self.sock = None

        # Connect to caster
        self.connect()

    def connect(self):
        while rclpy.ok():
            try:
                self.get_logger().info("Connecting to NTRIP caster...")
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.caster, self.port))

                auth = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
                request = (
                    f"GET /{self.mountpoint} HTTP/1.1\r\n"
                    f"User-Agent: NTRIP ROS2 Client\r\n"
                    f"Authorization: Basic {auth}\r\n\r\n"
                )
                self.sock.sendall(request.encode())

                response = self.sock.recv(4096).decode()

                if "401" in response:
                    self.get_logger().error("Unauthorized (401)")
                    raise RuntimeError("Bad credentials")

                if "404" in response:
                    self.get_logger().warn("Mountpoint not found (404), retrying...")
                    time.sleep(5)
                    continue  # retry

                if "200" in response:
                    self.get_logger().info("Connected to NTRIP caster")
                    return

            except Exception as e:
                self.get_logger().warn(f"NTRIP connection failed: {e}")
                time.sleep(5)

    def publish_fix(self, parsed):
        msg = NavSatFix()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "gps"
        msg.latitude = parsed.lat
        msg.longitude = parsed.lon
        msg.altitude = parsed.alt
        self.fix_pub.publish(msg)

    def spin(self):
        while rclpy.ok():
            try:
                # Receive RTCM from caster
                data = self.sock.recv(1024)
                if not data:
                    raise RuntimeError("Caster disconnected")

                # Send corrections to receiver
                self.ser.write(data)

                # Read NMEA from receiver
                raw, parsed = self.nmea_reader.read()
                if parsed and parsed.msgID == "GGA":
                    self.publish_fix(parsed)

            except Exception as e:
                self.get_logger().warn(f"NTRIP stream error: {e}")
                self.connect()


def main(args=None):
    rclpy.init(args=args)
    node = NTRIPRosNode()
    try:
        node.spin()
    finally:
        node.ser.close()
        if node.sock:
            node.sock.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
