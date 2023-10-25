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

def get_motor_positions(motor_objects):
    """Get current positions of all motors and return as a list"""
    positions = []
    for motor_object in motor_objects:
        positions.append(motor_object.get_present_position())
    return positions

def user_input():
    """Check if the user wants to continue"""
    ans = input('Continue? (y/n): ')
    return ans.lower() == 'y'

def move_to_stored_positions_sequentially(motor_objects, positions_array):
    """Move motors to stored positions sequentially with a one-second interval"""
    for positions in positions_array:
        for j, motor_object in enumerate(motor_objects):
            motor_object.set_goal_position(positions[j])
            time.sleep(0.75)  # Wait for one second before moving to the next stored position
        
    # Return to the last recorded position after going through all positions
    for j, motor_object in enumerate(motor_objects):
        motor_object.set_goal_position(positions[j])
        time.sleep(0.75)  # Wait for one second before ending the program

def main(motor_objects):
    bool_test = True
    positions_array = []  # To store motor positions
    while bool_test:
        # Get current positions before setting new goal positions
        positions_array.append(get_motor_positions(motor_objects))
        
        speed = int(input("Enter moving speed for all motors: "))
        for motor_object in motor_objects:
            print("\nPosition of dxl ID %d is %d" % (motor_object.id, motor_object.get_present_position()))
            input_pos = int(input("Enter the goal position for ID %d: " % motor_object.id))
            motor_object.set_goal_position(input_pos)
        
        bool_test = user_input()

    # Get the last positions after the loop has finished
    positions_array.append(get_motor_positions(motor_objects))
    
    # When 'G' is pressed, move motors sequentially to stored positions with a one-second interval
    if input("Press 'G' to move motors sequentially to stored positions: ").upper() == 'G':
        move_to_stored_positions_sequentially(motors, positions_array)

    return positions_array

# Get positions after running motors
positions_array = main(motors)

# Perform other operations using positions_array
print("Motor Positions Recorded:")
print(positions_array)

# Disconnect and disable torque for all motors
for motor in motors:
    motor.set_torque_enable(0)

# Disconnect
Ax12.disconnect()

