import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from smbus2 import SMBus

I2C_BUS = 1
I2C_ADDR = 0x58  # adjust if needed

class ADCOutNode(Node):

    def __init__(self):
        super().__init__('adcout1_node')

        self.bus = SMBus(I2C_BUS)
        self.target_voltage = 0.0

        self.subscription = self.create_subscription(
            Float32,
            '/voltage_cmd',
            self.callback,
            10
        )

        # 100 Hz update loop
        self.timer = self.create_timer(0.01, self.update_dac)

    def callback(self, msg):
        self.target_voltage = msg.data

    def update_dac(self):
        voltage = max(0.0, min(10.0, self.target_voltage))
        dac_value = int((voltage / 10.0) * 4095)

        high_byte = (dac_value >> 8) & 0x0F
        low_byte = dac_value & 0xFF

        try:
            self.bus.write_i2c_block_data(I2C_ADDR, 0x00, [high_byte, low_byte])
        except Exception as e:
            self.get_logger().error(f"I2C write failed: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = ADCOutNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
