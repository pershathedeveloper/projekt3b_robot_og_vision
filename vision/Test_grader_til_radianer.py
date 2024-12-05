from rtde_receive import RTDEReceiveInterface
from rtde_control import RTDEControlInterface
import numpy as np
import time

# Robot IP-adresse
robot_ip = "192.168.0.51"  # Skift til din robots IP-adresse

# Funktion til at omregne grader til radianer
def grader_til_radianer(grader):
    return np.deg2rad(grader)

# Hovedfunktion til bevægelser og datalogning
def main():
    try:
        # Initialiser RTDE-forbindelser
        rtde_r = RTDEReceiveInterface(robot_ip)  # Til dataovervågning
        rtde_c = RTDEControlInterface(robot_ip)  # Til bevægelseskontrol
        print(f"Forbundet til robot på {robot_ip}")

        # Positioner i radianer
        position1 = [
            grader_til_radianer( 134),
            grader_til_radianer(-36.09),
            grader_til_radianer(27.55),
            grader_til_radianer(-83.57),
            grader_til_radianer(-88.17),
            grader_til_radianer(333.61)
        ]

        position2 = [
            grader_til_radianer(109.20),
            grader_til_radianer( -80.10),
            grader_til_radianer( 98.40),
            grader_til_radianer(-110.38),
            grader_til_radianer(-89.53),
            grader_til_radianer(309.77),
        ]

        position3 = [
            grader_til_radianer(171.79),
            grader_til_radianer(-49.67),
            grader_til_radianer(52.06),
            grader_til_radianer(-93.42),
            grader_til_radianer(-89.06),
            grader_til_radianer(11.92),

        ]     

        position4 = [
            grader_til_radianer(172.08),
            grader_til_radianer(-109.55),
            grader_til_radianer(123.86),
            grader_til_radianer(-104.70),
            grader_til_radianer(-91.92),
            grader_til_radianer(11.92),

        ]     


        # Bevægelser med datalogning
        print("Bevæger robot til første position...")
        rtde_c.moveJ(position1, 1.2, 0.25)  # Udfør bevægelse til position 1
        time.sleep(7)  # Vent til bevægelse er færdig
        tcp_pose1 = rtde_r.getActualTCPPose()  # Hent TCP-position
        print(f"TCP Position efter første bevægelse: {tcp_pose1}")

        print("Bevæger robot til anden position...")
        rtde_c.moveJ(position2, 1.2, 0.25)  # Udfør bevægelse til position 2
        time.sleep(7)
        tcp_pose2 = rtde_r.getActualTCPPose()
        print(f"TCP Position efter anden bevægelse: {tcp_pose2}")

       #Bevægelse til trejde position
        print("Bevæger robot til tredje position...")
        rtde_c.moveJ(position3, 1.2, 0.25)  # Udfør bevægelse til position 3
        time.sleep(7)
        tcp_pose3 = rtde_r.getActualTCPPose()
        print(f"TCP Position efter tredje bevægelse: {tcp_pose3}") 

        #Bevægelse til fjerde position
        print("Bevæger robot til fjerde position...")
        rtde_c.moveJ(position4, 1.2, 0.25)  # Udfør bevægelse til position 3
        time.sleep(7)
        tcp_pose4 = rtde_r.getActualTCPPose()
        print(f"TCP Position efter fjerde bevægelse: {tcp_pose4}")

        

        

        print("Robotten har fuldført alle bevægelser.")

    except Exception as e:
        print(f"Fejl under programkørsel: {e}")


# Start programmet
if __name__ == "__main__":
    main()