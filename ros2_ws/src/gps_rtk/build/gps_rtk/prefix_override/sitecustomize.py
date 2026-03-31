import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/ros2_ws/src/gps_rtk/install/gps_rtk'
