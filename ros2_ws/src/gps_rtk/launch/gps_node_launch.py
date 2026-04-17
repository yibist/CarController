from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gps_rtk',
            executable='gps_node',
            name='gps_node',
            output='screen',
            parameters=[{
                'caster': 'crtk.net',
                'mountpoint': 'NEAR',
                'username': 'c',
                'password': 'c',
                'serial_port': '/dev/ttyAMA0',
                'baudrate': 115200
            }]
        )
    ])
