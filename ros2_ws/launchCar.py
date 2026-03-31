import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Include the RPLidar Launch (the C1 version you mentioned)
    rplidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('rplidar_ros'),
                'launch',
                'rplidar_c1_launch.py'
            )
        )
    )

    # 2. Servo Control Node (Python)
    servo_node = Node(
        package='servo_control',
        executable='servo_node',
        name='servo_manager'
    )

    # 3. Car Controller Node (C++ - the one we just named 'car_node')
    car_node = Node(
        package='car_controller',
        executable='car_node',
        name='car_logic'
    )

    return LaunchDescription([
        rplidar_launch,
        servo_node,
        car_node
    ])
