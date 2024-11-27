from robot_control import UR3Robot

# Robot IP
ROBOT_IP = "192.168.0.51"
PORT = 12345  # Standardport til URScript

if __name__ == "__main__":
    # Opret robot-objekt
    robot = UR3Robot(ROBOT_IP, PORT)

    try:
        # Forbind til robotten
        robot.connect()

        # Flyt robotten til joint positions
        robot.move_to_joint_positions()

    except Exception as e:
        print(f"Fejl under programkørsel: {e}")

    finally:
        # Luk forbindelsen
        robot.disconnect()

