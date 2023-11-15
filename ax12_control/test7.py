from Ax12 import Ax12
import time

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

def manual_teach_mode(motor_objects):
    """Enable manual teach mode and store positions"""
    print("Manual teach mode. Press 'M' to store positions.")
    stored_positions = []
    disable_torque(motor_objects)
    try:
        while True:
            positions = [motor.get_present_position() for motor in motor_objects]
            stored_positions.append(positions)
            print("Positions stored:", positions)  # Print the stored positions
            time.sleep(0.5)  # Wait for a short interval before storing the next position
    except KeyboardInterrupt:
        pass
    finally:
        enable_torque(motor_objects)
    return stored_positions

def move_to_stored_positions_sequentially(motor_objects, positions_array):
    """Move motors to stored positions sequentially with a one-second interval"""
    enable_torque(motor_objects)
    for positions in positions_array:
        for motor, pos in zip(motor_objects, positions):
            motor.set_goal_position(pos)
            time.sleep(1)  # Wait for one second before moving to the next stored position
    disable_torque(motor_objects)

if __name__ == '__main__':
    try:
        stored_positions = []
        user_input = input("Press 'M' to enter manual teach mode or 'U' to move to stored positions: ").upper()
        if user_input == 'M':
            stored_positions = manual_teach_mode(motors)
            print("Positions stored.")
        elif user_input == 'U':
            move_to_stored_positions_sequentially(motors, stored_positions)
            print("Moved to stored positions.")
        else:
            print("Invalid input. Please enter 'M' or 'U'.")
    except KeyboardInterrupt:
        pass
    finally:
        disable_torque(motors)
        Ax12.disconnect()
