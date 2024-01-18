import os
import time
import threading
import numpy as np
import matplotlib.pyplot as plt
from dynamixel_sdk import *

# Control table address
ADDR_AX_TORQUE_ENABLE = 24
ADDR_AX_GOAL_POSITION = 30
ADDR_AX_PRESENT_POSITION = 36
ADDR_AX_GOAL_SPEED_L = 32

# Protocol version
PROTOCOL_VERSION = 1.0

# Default setting
ID_MAT = [3, 4, 5, 6]
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
        CHECK_MAT = [[597, 512, 512, 512, 512, 597, 597, 512],
                     [427, 427, 427, 512, 427, 512, 512, 512],
                     [512, 512, 597, 597, 597, 597, 427, 427],
                     [512, 597, 597, 597, 597, 597, 427, 427]]

        for i in range(len(CHECK_MAT[0])):
            for dxl_index, dxl_id in enumerate(ID_MAT):
                goal_position = CHECK_MAT[dxl_index][i]

                # Read present position
                dxl_present_position, _, _ = packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_AX_PRESENT_POSITION)

                # Create an array of positions for interpolation
                positions = np.linspace(dxl_present_position, goal_position, num=40)

                for pos in positions:
                    # Set the goal position
                    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_AX_GOAL_POSITION, int(pos))
                    if dxl_comm_result != COMM_SUCCESS:
                        print("Failed to set goal position for ID:%03d" % dxl_id)

                    # Read present position to calculate speed
                    dxl_present_position_new, _, _ = packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_AX_PRESENT_POSITION)

                    # Calculate speed (change in position over time)
                    speed = (dxl_present_position_new - dxl_present_position) / 0.01  # Assuming 0.008 seconds sleep time

                    print("[ID:%03d] GoalPos:%03d  PresPos:%03d  Speed:%.2f" % (dxl_id, goal_position, dxl_present_position, speed))

                    dxl_present_position = dxl_present_position_new

                    time.sleep(0.01)  # Adjust the sleep time as needed for smooth motion

                    # Break if the goal is reached
                    if not abs(goal_position - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                        break

except KeyboardInterrupt:
    pass

finally:
    for dxl_id in ID_MAT:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_AX_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to disable torque for ID:%03d" % dxl_id)
        elif dxl_error != 0:
            print("Error in disabling torque for ID:%03d" % dxl_id)

    portHandler.closePort()
