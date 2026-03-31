FROM ros:humble

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-lgpio \
    python3-colcon-common-extensions \
    i2c-tools \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python libs
RUN pip3 install --no-cache-dir \
    Adafruit-Blinka \
    adafruit-circuitpython-pca9685 \
    adafruit-circuitpython-motor

# Create workspace
WORKDIR /ros2_ws/src

# Clone RPLidar ROS2 driver (specifying the ros2 branch)
RUN git clone -b ros2 https://github.com/Slamtec/rplidar_ros.git

# Build workspace
WORKDIR /ros2_ws
# Using /bin/bash -c to ensure the source command works correctly during build
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build"

# Source ROS + workspace automatically for interactive shells
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source /ros2_ws/install/setup.bash" >> ~/.bashrc