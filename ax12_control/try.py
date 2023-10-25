from Ax12 import *  # Uses Ax12 library
from dynamixel_sdk import *  # Uses Dynamixel SDK library
from dxl_control.ax12_control_table import *  # Uses ax12 Control Table

class Ax12:
    """ Class for Dynamixel AX12A motors."""
    PROTOCOL_VERSION = 1.0
    BAUDRATE = 57600             # Dynamixel default baudrate
    DEVICENAME = '/dev/ttyUSB0'           # Default COM Port
    portHandler = PortHandler(DEVICENAME)   # Initialize Ax12.PortHandler instance
    packetHandler = PacketHandler(PROTOCOL_VERSION)  # Initialize Ax12.PacketHandler instance
    # Dynamixel will rotate between this value
    MIN_POS_VAL = 0
    MAX_POS_VAL = 1023
    
    



