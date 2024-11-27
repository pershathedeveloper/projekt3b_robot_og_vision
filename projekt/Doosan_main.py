from robot_control import DoosanRobot

# Robot IP og port
ROBOT_IP = "192.168.0.51"
PORT = 12345  # Standardporten til Doosan-robotter

# Kartesisk position (X, Y, Z i meter; RX, RY, RZ i radianer)
TARGET_POSITION = [0.5, -0.2, 0.3, 0.0, 1.57, 0.0]  # Eksempelposition

if __name__ == "__main__":
    # Opret robot-objekt
    robot = DoosanRobot(ROBOT_IP, PORT)

    try:
        # Forbind til robotten
        robot.connect()

        # Flyt robotten til den angivne kartesiske position
        robot.move_to_position(TARGET_POSITION)

    except Exception as e:
        print(f"Fejl under programkørsel: {e}")

    finally:
        # Luk forbindelsen
        robot.disconnect()
