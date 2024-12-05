import rtde_control
import rtde_receive
import time

# Replace with your robot's IP address
ROBOT_IP = '192.168.0.51'

# Connect to the robot control and receive interfaces
rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

# Define target positions (X, Y, Z, Rx, Ry, Rz)
# X, Y, Z are in meters; Rx, Ry, Rz are in radians
positions = [
    [0.3, -0.2, 0.5, 2.2, 2.2, 0.0],  # Position 1
    [0.4, -0.1, 0.6, 2.0, 2.0, 0.0],  # Position 2
    [0.5, 0.0, 0.7, 1.8, 1.8, 0.0]    # Position 3
]

# Define speed and acceleration for motion
speed = 0.5        # Speed in m/s
acceleration = 0.3 # Acceleration in m/s^2

try:
    # Move to each position sequentially
    for position in positions:
        print(f"Moving to position: {position}")
        
        # Command robot to move in a linear path to the position
        rtde_c.moveL(position, speed, acceleration)
        
        # Optional: Wait for 1 second between movements
        time.sleep(1)

    # Retrieve and print the robot's current pose
    current_pose = rtde_r.getActualTCPPose()
    print("Final robot pose:", current_pose)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure the robot interfaces are cleanly disconnected
    rtde_c.disconnect()
    rtde_r.disconnect()
    print("Disconnected from the robot.")
