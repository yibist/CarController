#!/bin/bash

# Exit on error

set -e

PACKAGE_NAME="motor_control"

echo "Creating ROS2 Python package: $PACKAGE_NAME"

# Create base structure

mkdir -p $PACKAGE_NAME/$PACKAGE_NAME
mkdir -p $PACKAGE_NAME/resource

# Create Python module files

touch $PACKAGE_NAME/$PACKAGE_NAME/**init**.py
touch $PACKAGE_NAME/$PACKAGE_NAME/motor_node.py
touch $PACKAGE_NAME/$PACKAGE_NAME/dac_driver.py
touch $PACKAGE_NAME/$PACKAGE_NAME/gpio_driver.py
touch $PACKAGE_NAME/$PACKAGE_NAME/encoder.py

# Create ROS2 package files

touch $PACKAGE_NAME/package.xml
touch $PACKAGE_NAME/setup.py
touch $PACKAGE_NAME/setup.cfg

# Resource index file (required by ROS2)

touch $PACKAGE_NAME/resource/$PACKAGE_NAME

echo "Structure created."

# Optional: add minimal boilerplate content

# setup.cfg

cat <<EOF > $PACKAGE_NAME/setup.cfg
[develop]
script_dir=$base/lib/$PACKAGE_NAME
[install]
install_scripts=$base/lib/$PACKAGE_NAME
EOF

# package.xml

cat <<EOF > $PACKAGE_NAME/package.xml

<?xml version="1.0"?>

<package format="3">
  <name>$PACKAGE_NAME</name>
  <version>0.0.1</version>
  <description>Motor control package</description>
  <maintainer email="you@example.com">you</maintainer>
  <license>MIT</license>
  <depend>rclpy</depend>
</package>
EOF

# setup.py

cat <<EOF > $PACKAGE_NAME/setup.py
from setuptools import setup

package_name = '$PACKAGE_NAME'

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
EOF

echo "ROS2 package $PACKAGE_NAME is ready."
echo "Next steps:"
echo "cd $PACKAGE_NAME/.. && colcon build"
