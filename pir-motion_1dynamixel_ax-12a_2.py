import RPi.GPIO as GPIO
import time
import threading
from dynamixel_sdk import *

# Control table addresses for AX-12A
ADDR_AX_TORQUE_ENABLE = 24
ADDR_AX_GOAL_POSITION = 30
ADDR_AX_PRESENT_POSITION = 36

# Protocol version
PROTOCOL_VERSION = 1.0

# Default setting
DXL_ID = 1         # ID of the AX-12A servo motor
BAUDRATE = 57600   # Default baudrate of the servo motor
DEVICENAME = '/dev/ttyUSB0'  # Replace with the serial port connected to the servo motor

# Set GPIO pin for PIR sensor
pir_pin = 12

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pir_pin, GPIO.IN)

# Initialize the Dynamixel SDK
port_handler = PortHandler(DEVICENAME)
packet_handler = PacketHandler(PROTOCOL_VERSION)

# Open the serial port
if port_handler.openPort():
    print("Succeeded to open the serial port")
else:
    print("Failed to open the serial port")
    quit()

# Set baudrate of the serial port
if port_handler.setBaudRate(BAUDRATE):
    print("Succeeded to set baudrate")
else:
    print("Failed to set baudrate")
    quit()
    
# Enable torque for the servo motor
dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(port_handler, DXL_ID, 24, 1)
# Define speed of the servo motor
dxl_comm_result, dxl_error = packet_handler.write2ByteTxRx(port_handler, DXL_ID, 32, 30)

# Flag to control servo behavior
motion_detected = False
servo_position = 200  # Last known angle of the servo motor
    
# Interrupt function
def motion_detected_callback(channel):
    global motion_detected
    motion_detected = True

# Set up interrupt for PIR sensor
GPIO.add_event_detect(pir_pin, GPIO.RISING, callback=motion_detected_callback,bouncetime=200)

def stop_motor():
    dxl_comm_result, dxl_error = packet_handler.write2ByteTxRx(port_handler, DXL_ID, 32, 0)
    # write 0 to the goal position register (address 32) to stop the motor

def move_servo(position):
    dxl_comm_result, dxl_error = packet_handler.write2ByteTxRx(port_handler, DXL_ID, 30, position)
    
def servo_control():
    global motion_detected, servo_position
    while True:
        if motion_detected:
            print("Motion detected!")
            stop_motor()
            time.sleep(5)  # Wait for 5 seconds
            print("STOP")
            motion_detected = False  # Reset the flag
            
#         if servo_position > 200:
#             dxl_comm_result, dxl_error = packet_handler.write2ByteTxRx(port_handler, DXL_ID, 32, 15)
#             move_servo(servo_position)
                    
# Create a new thread for servo control
servo_thread = threading.Thread(target=servo_control)
servo_thread.daemon = True
servo_thread.start()

try:
    servo_position = 200  # Initialize servo angle
    while True:
        for position in range(200, 800, 10):
            #print("A")
            servo_position = position
            move_servo(position)
            time.sleep(0.05)  # Delay for smooth movement
            

        # Move servo back to 0 degrees
        for position in range(800, 199, -10):
            #print("B")
            servo_position = position
            move_servo(position)
            time.sleep(0.05)  # Delay for smooth movement
            

except KeyboardInterrupt:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, 24, 0)
    portHandler.closePort()
    GPIO.cleanup()


