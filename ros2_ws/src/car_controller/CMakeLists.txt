cmake_minimum_required(VERSION 3.8)
project(car_controller)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 1. Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED) # Adding this because most cars use Lidar/Camera data

# 2. CREATE THE BINARY (Executable)
# This links the .cpp file to a command name 'car_node'
add_executable(car_node src/CarController.cpp)

# 3. LINK LIBRARIES
# This allows your code to use ROS functions
ament_target_dependencies(car_node rclcpp std_msgs sensor_msgs)

# 4. INSTALL THE BINARY
# This makes 'ros2 run' able to find the file after building
install(TARGETS
  car_node
  DESTINATION lib/${PROJECT_NAME}
)

# (Optional) If you have a launch folder, install that too
# install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})

ament_package()
