from setuptools import setup

package_name = 'motor_control'

setup(
name=package_name,
version='0.0.1',
packages=[package_name],
install_requires=['setuptools'],
zip_safe=True,
maintainer='you',
description='Motor control ROS2 package',
entry_points={
'console_scripts': [
'motor_node = motor_control.motor_node:main',
],
},
)
