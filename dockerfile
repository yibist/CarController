# =====================================
# General
# =====================================
# OS generated files
.DS_Store
Thumbs.db
*.log

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
*.pdb
*.egg-info/

# Editor/IDE files
*.swp
*.swo
*.vscode/
.idea/

# =====================================
# ROS2 specific
# =====================================
# ROS2 build directories
ros2_ws/build/
ros2_ws/install/
ros2_ws/log/
ros2_ws/devel/

# Colcon cache
ros2_ws/.colcon/

# Catkin (if any)
*.catkin
*.catkin_tools/

# =====================================
# C++ build artifacts
# =====================================
*.o
*.so
*.a
*.out
*.exe
CMakeFiles/
CMakeCache.txt
cmake_install.cmake
Makefile

# =====================================
# Docker
# =====================================
# Do not ignore Dockerfile itself
# Ignore Docker build cache
docker-compose.override.yml
*.env

# =====================================
# Misc
# =====================================
*.tmp
*.bak
*.swp