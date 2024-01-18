from Ax12 import Ax12

# e.g 'COM3' on Windows or '/dev/ttyUSB0' on Linux
Ax12.DEVICENAME = '/dev/ttyUSB0'
Ax12.BAUDRATE = 57600

# Set up an array of motor IDs
motor_ids = [1, 2, 3, 4]

# Connect to the Dynamixel motors
Ax12.connect()

# Create Ax12 instances for each motor
motors = [Ax12(motor_id) for motor_id in motor_ids]

# Set initial moving speed for all motors
for motor in motors:
    motor.set_moving_speed(50)

def user_input():
    """Check if the user wants to continue"""
    ans = input('Continue? (y/n): ')
    return ans.lower() == 'y'

def main(motor_objects):
    bool_test = True
    while bool_test:
        for motor_object in motor_objects:
            print("\nPosition of dxl ID %d is %d" % (motor_object.id, motor_object.get_present_position()))
            input_pos = int(input("Enter the goal position for ID %d: " % motor_object.id))
            motor_object.set_goal_position(input_pos)
            print("Position of dxl ID %d is now: %d" % (motor_object.id, motor_object.get_present_position()))
        bool_test = user_input()

# Pass in the list of AX12 objects
main(motors)

# Disconnect and disable torque for all motors
for motor in motors:
    motor.set_torque_enable(0)

# Disconnect
Ax12.disconnect()