from Ax12 import Ax12
import time
import threading

# e.g 'COM3' on Windows or '/dev/ttyUSB0' on Linux
Ax12.DEVICENAME = '/dev/ttyUSB0'
Ax12.BAUDRATE = 57600

# Set up an array of motor IDs
motor_ids = [1, 2, 3, 4]

# Connect to the Dynamixel motors
Ax12.connect()

# Create Ax12 instances for each motor
motors = [Ax12(motor_id) for motor_id in motor_ids]

def disable_torque(motor_objects):
    """Disable torque for all motors"""
    for motor_object in motor_objects:
        motor_object.set_torque_enable(0)

def enable_torque(motor_objects):
    """Enable torque for all motors"""
    for motor_object in motor_objects:
        motor_object.set_torque_enable(1)

def user_input_listener():
    global manual_teach_mode_active
    while True:
        if manual_teach_mode_active:
            user_input = input("Press 'U' to stop manual teach mode: ").upper()
            if user_input == 'U':
                manual_teach_mode_active = False
                break

def manual_teach_mode(motor_objects):
    """Enable manual teach mode and store positions until 'U' is pressed"""
    global manual_teach_mode_active
    #print("Manual teach mode. Press 'M' to start storing positions.")
    stored_positions = []
    disable_torque(motor_objects)
    manual_teach_mode_active = True
    input_thread = threading.Thread(target=user_input_listener)
    input_thread.start()
    try:
        while manual_teach_mode_active:
            positions = [motor.get_present_position() for motor in motor_objects]
            stored_positions.append(positions)
            print("Positions stored:", positions)
            time.sleep(1)  # Wait for a short interval before storing the next position
    except KeyboardInterrupt:
        pass
    finally:
        enable_torque(motor_objects)
        input_thread.join()  # Wait for the input thread to finish
    return stored_positions

def move_to_stored_positions_sequentially(motor_objects, positions_array):
    """Move motors to stored positions sequentially with a one-second interval"""
    enable_torque(motor_objects)
    for positions in positions_array:
        for motor, pos in zip(motor_objects, positions):
            motor.set_goal_position(pos)
            time.sleep(0.2)  # Wait for one second before moving to the next stored position

if __name__ == '__main__':
    try:
        stored_positions = []  # Initialize the stored_positions list
        manual_teach_mode_active = False  # Flag to indicate whether manual teach mode is active
        user_input = input("Press 'M' to enter manual teach mode: ").upper()
        if user_input == 'M':
            stored_positions = manual_teach_mode(motors)
            print("Positions stored:", stored_positions)
            user_input = input("Press 'U' to move to stored positions: ").upper()
            if user_input == 'U':
                move_to_stored_positions_sequentially(motors, stored_positions)
                print("Moved to stored positions.")
            else:
                print("Invalid input. Exiting program.")
        else:
            print("Invalid input. Exiting program.")
    except KeyboardInterrupt:
        pass
    finally:
        enable_torque(motors)
        Ax12.disconnect()
