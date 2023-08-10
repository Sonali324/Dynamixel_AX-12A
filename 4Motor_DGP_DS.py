import os

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

from dynamixel_sdk import *

# Control table address
ADDR_AX_TORQUE_ENABLE = 24
ADDR_AX_GOAL_POSITION = 30
ADDR_AX_PRESENT_POSITION = 36
ADDR_AX_GOAL_SPEED_L = 32

# Protocol version
PROTOCOL_VERSION = 1.0

# Default setting
ID_MAT = [4, 3, 2, 1]
BAUDRATE = 57600
DEVICENAME = '/dev/ttyUSB0'

TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
DXL_MOVING_STATUS_THRESHOLD = 20

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixel Torque
for dxl_id in ID_MAT:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_AX_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("Failed to enable torque for ID:%03d" % dxl_id)
    elif dxl_error != 0:
        print("Error in enabling torque for ID:%03d" % dxl_id)
    else:
        print("Torque enabled for ID:%03d" % dxl_id)

try:
    while True:
        CHECK_MAT = [[0, 30, 60, 360, 390, 420, 570, 595, 620, 940, 970, 1000, 0],
                     [750, 470, 700, 700, 470, 700, 700, 470, 700, 700, 470, 700, 750],
                     [750, 650, 750, 750, 620, 750, 750, 630, 750, 750, 630, 750, 750],
                     [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]]
        SPEED_MAT = [[40, 70, 20, 90, 50, 20, 90, 90, 20, 90, 90, 20, 120],
                     [50, 90, 70, 50, 90, 70, 50, 90, 70, 50, 90, 70, 50],
                     [50, 70, 70, 50, 70, 70, 50, 70, 70, 50, 70, 70, 50],
                     [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]]

        for i in range(len(CHECK_MAT[0])):
            for dxl_index, dxl_id in enumerate(ID_MAT):
                goal_position = CHECK_MAT[dxl_index][i]
                goal_speed = SPEED_MAT[dxl_index][i]

                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_AX_GOAL_SPEED_L, goal_speed)
                if dxl_comm_result != COMM_SUCCESS:
                    print("Failed to set goal speed for ID:%03d" % dxl_id)

                while True:
                    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_AX_PRESENT_POSITION)
                    if dxl_comm_result != COMM_SUCCESS:
                        print("Failed to read present position for ID:%03d" % dxl_id)
                    elif dxl_error != 0:
                        print("Error in reading present position for ID:%03d" % dxl_id)

                    print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (dxl_id, goal_position, dxl_present_position))

                    dxl_comm1_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_AX_GOAL_POSITION, goal_position)
                    if dxl_comm1_result != COMM_SUCCESS:
                        print("Failed to set goal position for ID:%03d" % dxl_id)

                    if not abs(goal_position - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                        break

finally:
    for dxl_id in ID_MAT:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_AX_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to disable torque for ID:%03d" % dxl_id)
        elif dxl_error != 0:
            print("Error in disabling torque for ID:%03d" % dxl_id)

    portHandler.closePort()
