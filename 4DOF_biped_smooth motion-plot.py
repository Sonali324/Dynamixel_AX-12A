import os
import time
import threading
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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

# Define CHECK_MAT and SPEED_MAT
CHECK_MAT = [[597, 512, 512, 512, 512, 597, 597, 512],
             [427, 427, 427, 512, 427, 512, 512, 512],
             [512, 512, 597, 597, 597, 597, 427, 427],
             [512, 597, 597, 597, 597, 597, 427, 427]]

# SPEED_MAT = [[80, 50, 50, 50, 50, 80, 50, 50],
#              [80, 50, 50, 50, 50, 80, 50, 50],
#              [80, 50, 50, 50, 50, 50, 50, 50],
#              [80, 50, 50, 50, 50, 50, 50, 50]]

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

# Variables for data recording
timestamps = []
goal_positions = {dxl_id: [] for dxl_id in ID_MAT}
present_positions = {dxl_id: [] for dxl_id in ID_MAT}
speeds = {dxl_id: [] for dxl_id in ID_MAT}

# Enable interactive mode for non-blocking plots
plt.ion()

# Create figure and axes
fig, axs = plt.subplots(2, 1)

# Line objects for plots
lines_goal = {dxl_id: axs[0].plot([], [], label=f"ID:{dxl_id} Goal")[0] for dxl_id in ID_MAT}
lines_present = {dxl_id: axs[0].plot([], [], label=f"ID:{dxl_id} Present")[0] for dxl_id in ID_MAT}
lines_speed = {dxl_id: axs[1].plot([], [], label=f"ID:{dxl_id} Speed")[0] for dxl_id in ID_MAT}

# Legends
axs[0].legend()
axs[1].legend()

# Set labels and title
axs[0].set(xlabel='Time (s)', ylabel='Position', title='Goal and Present Positions vs Time')
axs[1].set(xlabel='Time (s)', ylabel='Speed', title='Speed vs Time')

# Plot initialization
for dxl_id in ID_MAT:
    lines_goal[dxl_id].set_data([], [])
    lines_present[dxl_id].set_data([], [])
    lines_speed[dxl_id].set_data([], [])

# Function to update the plot
def update_plot(frame):
    elapsed_time = time.time() - start_time
    timestamps.append(elapsed_time)

    for dxl_index, dxl_id in enumerate(ID_MAT):
        goal_position = CHECK_MAT[dxl_index][frame]

        # Read present position
        dxl_present_position, _, _ = packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_AX_PRESENT_POSITION)

        # Calculate speed
        if timestamps:
            speed = (goal_positions[dxl_id][-1] - dxl_present_position) / (timestamps[-1] - elapsed_time)
        else:
            speed = 0

        # Set the goal position
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_AX_GOAL_POSITION, goal_position)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to set goal position for ID:%03d" % dxl_id)

        # Append data to lists
        goal_positions[dxl_id].append(goal_position)
        present_positions[dxl_id].append(dxl_present_position)
        speeds[dxl_id].append(speed)

        # Update plot data
        lines_goal[dxl_id].set_data(timestamps, goal_positions[dxl_id])
        lines_present[dxl_id].set_data(timestamps, present_positions[dxl_id])
        lines_speed[dxl_id].set_data(timestamps, speeds[dxl_id])

    # Adjust the plot limits
    for ax in axs:
        ax.relim()
        ax.autoscale_view()

    return lines_goal.values() + lines_present.values() + lines_speed.values()

# Start time for timestamping
start_time = time.time()

# Animate the plot
ani = FuncAnimation(fig, update_plot, frames=len(CHECK_MAT[0]), blit=True)

try:
    plt.show(block=True)
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
