import urx

# Robot IP
ROBOT_IP = "192.168.0.51"

# Position 1 (fra første billede): X, Y, Z, RX, RY, RZ
position_1 = [55.97 / 1000, -147.28 / 1000, 520.91 / 1000, 1.430, -2.768, -0.010]

# Position 2 (fra andet billede): X, Y, Z, RX, RY, RZ
position_2 = [-48.59 / 1000, -279.85 / 1000, 281.44 / 1000, 0.029, -3.133, 0.033]

def move_to_position(robot, position, name):
    """Flyt robotten til en specifik position"""
    print(f"Flytter robotten til {name}: {position}")
    robot.movel(position, acc=0.1, vel=0.05)  # Sørg for, at position er en korrekt liste
    print(f"Robotten er nu i {name}")

try:
    # Opret forbindelse til robotten
    robot = urx.Robot(ROBOT_IP)
    print(f"Forbundet til UR3 på {ROBOT_IP}")

    # Flyt til Position 1
    move_to_position(robot, position_1, "Position 1")

    # Pause for at observere bevægelsen
    input("Tryk Enter for at fortsætte til Position 2...")

    # Flyt til Position 2
    move_to_position(robot, position_2, "Position 2")

except Exception as e:
    print(f"Fejl under bevægelse: {e}")
finally:
    # Luk forbindelsen til robotten
    robot.close()
    print("Forbindelse til UR3 lukket")
