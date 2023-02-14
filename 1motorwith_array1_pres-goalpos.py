import os
import time


if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_AX_GOAL_SPEED_L = 32

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID1                      = 1                 # Dynamixel ID : 1
DXL_ID2                      = 2                 # Dynamixel ID : 2
DXL_ID3                      = 3                 # Dynamixel ID : 3
DXL_ID4                      = 4                 # Dynamixel ID : 4
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
#DXL_MINIMUM_POSITION_VALUE  = 0           # Dynamixel will rotate between this value
#DXL_MAXIMUM_POSITION_VALUE  = 1023            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()
    
#dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, ADDR_MX_PRESENT_POSITION)
#print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, dxl_goal_position[index], dxl_present_position))
#dxl_goal_position = [dxl_present_position + 100]         # Goal position
# for dxl_goal_position in range(dxl_present_position, DXL_MAXIMUM_POSITION_VALUE, 100):

# Enable Dynamixel Torque
dxl1_comm_result, dxl1_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID1, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
dxl2_comm_result, dxl2_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID2, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl1_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl1_comm_result))
elif dxl1_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl1_error))
else:
    print("Dynamixel has been successfully connected")    
    
while 1:
    
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break
    
#print(dxl_goal_position)

check1 = [0, 50, 0, 50, 0, 50, 0]
speed1 = [50, 100, 50, 100, 50, 100, 50]
#x = len(dxl_goal_position)
for x in range(7):
    print(x)
    
    dxl_goal_position = check1[x]
    print("%03d" %(check1[x]))
    
    while 1:
        
        # Read present position
        dxl1_present_position, dxl1_comm_result, dxl1_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID1, ADDR_MX_PRESENT_POSITION)
        dxl2_present_position, dxl2_comm_result, dxl2_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID2, ADDR_MX_PRESENT_POSITION)
        dxl3_present_position, dxl1_comm_result, dxl3_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID3, ADDR_MX_PRESENT_POSITION)
        dxl4_present_position, dxl2_comm_result, dxl4_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID4, ADDR_MX_PRESENT_POSITION)
        if dxl1_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl1_comm_result))
        elif dxl1_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl1_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID1, check1[x], dxl1_present_position))
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID2, check1[x], dxl2_present_position))
        
        dxl1_comm_result, dxl1_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID1, ADDR_AX_GOAL_SPEED_L, speed1[x])
        dxl2_comm_result, dxl2_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID2, ADDR_AX_GOAL_SPEED_L, speed1[x])
  
        # Write goal position
        dxl1_comm_result, dxl1_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID1, ADDR_MX_GOAL_POSITION, check1[x])
        dxl2_comm_result, dxl2_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID2, ADDR_MX_GOAL_POSITION, check1[x])
        if dxl1_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl1_comm_result))
        elif dxl1_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl1_error))

        if not abs(check1[x] - dxl1_present_position) > DXL_MOVING_STATUS_THRESHOLD:
        #if not abs(check1[x] - dxl2_present_position) > DXL_MOVING_STATUS_THRESHOLD:
            break


# Disable Dynamixel Torque
dxl1_comm_result, dxl1_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID1, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
dxl2_comm_result, dxl2_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID2, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl1_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl1_comm_result))
elif dxl1_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl1_error))

#Close port
portHandler.closePort()