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

from dynamixel_sdk import *                    # Uses Dynamixel SDK library
import RPi.GPIO as GPIO
from time import sleep

# Control table address
ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_AX_GOAL_SPEED_L = 32

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL1_ID                      = 4                #Dynamixel ID : 4
DXL2_ID                      = 3                #Dynamixel ID : 3
DXL3_ID                      = 2                #Dynamixel ID : 2
DXL4_ID                      = 1                #Dynamixel ID : 1
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

TRIG = 23
ECHO = 24

GPIO.setwarnings(False)
#This means we will refer to the GPIO pins
GPIO.setmode(GPIO.BCM)
#This sets up the GPIO pin as an output or an input pin
GPIO.setup(18, GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
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
    
print ("Distance Measurement In Progress")    
while 1:
        
        GPIO.output(TRIG, False)
        time.sleep(2)
        
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
        
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print ("Distance: ",distance,"cm")
        
        if distance >=10:
            print ("No Object Detected")
            # Enable Dynamixel Torque
            dxl1_comm_result, dxl1_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)

            if dxl1_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl1_comm_result))
            elif dxl1_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl1_error))
            else:
                print("Dynamixel_1 has been successfully connected")
                
                
            dxl2_comm_result, dxl2_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)

            if dxl2_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl2_comm_result))
            elif dxl2_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl2_error))
            else:
                print("Dynamixel_2 has been successfully connected")
             
             
            dxl3_comm_result, dxl3_error = packetHandler.write1ByteTxRx(portHandler, DXL3_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)

            if dxl3_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl3_comm_result))
            elif dxl3_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl3_error))
            else:
                print("Dynamixel_3 has been successfully connected")

            dxl4_comm_result, dxl4_error = packetHandler.write1ByteTxRx(portHandler, DXL4_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)

            if dxl4_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl4_comm_result))
            elif dxl4_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl4_error))
            else:
                print("Dynamixel_4 has been successfully connected")
                
            while 1:
                
                check1 = [0,   90,  120,  930, 960, 990, 0]
                check2 = [750, 575, 800,  800, 600, 750, 750]
                check3 = [750, 710, 710,  710, 720, 710, 750]
                check4 = [820, 80,  80,   30,  80,  820, 820]
                speed1 = [120,  120, 50,   120, 120, 50,  150]
                speed2 = [50,  90,  70,   90,  120, 90,  50]
                speed3 = [50,  90,  70,   90,  90,  90,  50]
                speed4 = [180, 120, 50,   20,  120, 120, 180]

                #while 1:
                #print("Press any key to continue! (or press ESC to quit!)")
                #if getch() == chr(0x1b):
                        #break

                #x = len(dxl_goal_position)
                for x in range(len(check1)):
            #         print(x)
                    if x == 2:
                        GPIO.output(18, 0)
                        time.sleep(2)
                    elif x == 5:
                        GPIO.output(18, 1)
                        time.sleep(1)
                    
                    #dxl1_goal_position = check1[x]
                    print("%03d" %(check1[x]))     
                            
                    
                    dxl1_comm_result, dxl1_error = packetHandler.write2ByteTxRx(portHandler, DXL1_ID, ADDR_AX_GOAL_SPEED_L, speed1[x])

                    while 1:
                        # Read present position
                        dxl1_present_position, dxl1_comm_result, dxl1_error = packetHandler.read2ByteTxRx(portHandler, DXL1_ID, ADDR_MX_PRESENT_POSITION)
                        if dxl1_comm_result != COMM_SUCCESS:
                            print("%s" % packetHandler.getTxRxResult(dxl1_comm_result))
                        elif dxl1_error != 0:
                            print("%s" % packetHandler.getRxPacketError(dxl1_error))

                        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL1_ID, check1[x], dxl1_present_position))
                        
                            # Write goal position
                        dxl1_comm1_result, dxl1_error = packetHandler.write2ByteTxRx(portHandler, DXL1_ID, ADDR_MX_GOAL_POSITION, check1[x])
                        if dxl1_comm_result != COMM_SUCCESS:
                            print("%s" % packetHandler.getTxRxResult(dxl1_comm_result))
                        elif dxl1_error != 0:
                            print("%s" % packetHandler.getRxPacketError(dxl1_error))

                        if not abs(check1[x] - dxl1_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                            break
                    
                        dxl2_comm_result, dxl2_error = packetHandler.write2ByteTxRx(portHandler, DXL2_ID, ADDR_AX_GOAL_SPEED_L, speed2[x])

                        while 1:
                            # Read present position
                            dxl2_present_position, dxl2_comm_result, dxl2_error = packetHandler.read2ByteTxRx(portHandler, DXL2_ID, ADDR_MX_PRESENT_POSITION)
                            if dxl2_comm_result != COMM_SUCCESS:
                                print("%s" % packetHandler.getTxRxResult(dxl2_comm_result))
                            elif dxl1_error != 0:
                                print("%s" % packetHandler.getRxPacketError(dxl2_error))

                            print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL2_ID, check2[x], dxl2_present_position))
                            
                                # Write goal position
                            dxl2_comm1_result, dxl2_error = packetHandler.write2ByteTxRx(portHandler, DXL2_ID, ADDR_MX_GOAL_POSITION, check2[x])
                            if dxl2_comm_result != COMM_SUCCESS:
                                print("%s" % packetHandler.getTxRxResult(dxl2_comm_result))
                            elif dxl2_error != 0:
                                print("%s" % packetHandler.getRxPacketError(dxl2_error))

                            if not abs(check2[x] - dxl2_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                                break
                            
                        dxl3_comm_result, dxl3_error = packetHandler.write2ByteTxRx(portHandler, DXL3_ID, ADDR_AX_GOAL_SPEED_L, speed3[x])
                            
                        while 1:
                            # Read present position
                            dxl3_present_position, dxl3_comm_result, dxl3_error = packetHandler.read2ByteTxRx(portHandler, DXL3_ID, ADDR_MX_PRESENT_POSITION)
                            if dxl3_comm_result != COMM_SUCCESS:
                                print("%s" % packetHandler.getTxRxResult(dxl3_comm_result))
                            elif dxl3_error != 0:
                                print("%s" % packetHandler.getRxPacketError(dxl3_error))

                            print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL3_ID, check3[x], dxl3_present_position))
                            
                                # Write goal position
                            dxl3_comm1_result, dxl3_error = packetHandler.write2ByteTxRx(portHandler, DXL3_ID, ADDR_MX_GOAL_POSITION, check3[x])
                            if dxl3_comm_result != COMM_SUCCESS:
                                print("%s" % packetHandler.getTxRxResult(dxl3_comm_result))
                            elif dxl3_error != 0:
                                print("%s" % packetHandler.getRxPacketError(dxl3_error))

                            if not abs(check3[x] - dxl3_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                                break
                            
                            
                            dxl4_comm_result, dxl4_error = packetHandler.write2ByteTxRx(portHandler, DXL4_ID, ADDR_AX_GOAL_SPEED_L, speed4[x])
                            
                        while 1:
                            # Read present position
                            dxl4_present_position, dxl4_comm_result, dxl4_error = packetHandler.read2ByteTxRx(portHandler, DXL4_ID, ADDR_MX_PRESENT_POSITION)
                            if dxl4_comm_result != COMM_SUCCESS:
                                print("%s" % packetHandler.getTxRxResult(dxl4_comm_result))
                            elif dxl4_error != 0:
                                print("%s" % packetHandler.getRxPacketError(dxl4_error))

                            print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL4_ID, check4[x], dxl4_present_position))
                            
                                # Write goal position
                            dxl4_comm1_result, dxl4_error = packetHandler.write2ByteTxRx(portHandler, DXL4_ID, ADDR_MX_GOAL_POSITION, check4[x])
                            if dxl4_comm_result != COMM_SUCCESS:
                                print("%s" % packetHandler.getTxRxResult(dxl4_comm_result))
                            elif dxl4_error != 0:
                                print("%s" % packetHandler.getRxPacketError(dxl4_error))

                            if not abs(check4[x] - dxl4_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                                break
                
        else:
            print ("Object Detected")
            # Disable Dynamixel Torque
            dxl1_comm_result, dxl1_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
            if dxl1_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl1_comm_result))
            elif dxl1_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl1_error))
                
            dxl2_comm_result, dxl2_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
            if dxl2_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl2_comm_result))
            elif dxl2_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl2_error))
                
            dxl3_comm_result, dxl3_error = packetHandler.write1ByteTxRx(portHandler, DXL3_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
            if dxl3_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl3_comm_result))
            elif dxl3_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl3_error))
                
            dxl4_comm_result, dxl4_error = packetHandler.write1ByteTxRx(portHandler, DXL4_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
            if dxl4_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl4_comm_result))
            elif dxl4_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl4_error))
                
    
# Close port
portHandler.closePort()





