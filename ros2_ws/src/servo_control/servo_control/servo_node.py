import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

# These libraries replace smbus2 for better compatibility with Adafruit drivers
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

class ServoNode(Node):
    def __init__(self):
        super().__init__('servo_node')

        try:
            self.i2c = busio.I2C(board.SCL, board.SDA)

            self.pca = PCA9685(self.i2c)
            self.pca.frequency = 50  # 50Hz is standard for MG996R

            self.channel_num = 0
            self.my_servo = servo.Servo(
                self.pca.channels[self.channel_num], 
                min_pulse=500, 
                max_pulse=2400
            )

            self.get_logger().info(f'PCA9685 detected and Servo initialized on channel {self.channel_num}')

        except Exception as e:
            self.get_logger().error(f'Failed to initialize hardware: {str(e)}')
            raise e

        # Create Subscription
        self.subscription = self.create_subscription(
            Float32,
            'servo_angle',
            self.angle_callback,
            10
        )
        self.get_logger().info('Listening for angles on topic: /servo_angle')

    def angle_callback(self, msg):
        try:
            angle = max(0.0, min(180.0, msg.data))
            
            self.my_servo.angle = angle
            self.get_logger().info(f'Moving to {angle:.1f}°', throttle_duration_sec=0.5)
            
        except Exception as e:
            self.get_logger().warn(f'Error moving servo: {str(e)}')

    def cleanup(self):
        """Called on shutdown to stop PWM signals"""
        self.pca.deinit()

def main(args=None):
    rclpy.init(args=args)
    node = ServoNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Servo node stopping...')
    finally:
        node.cleanup()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
