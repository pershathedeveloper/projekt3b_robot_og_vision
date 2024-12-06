import socket
import numpy as np
import time

# Robot IP-adresse og port
robot_ip = "192.168.0.51"  # Skift til din robots IP-adresse
robot_port = 30000  # Typisk port for Universal Robots

# Funktion til at omregne grader til radianer
def grader_til_radianer(grader):
    return np.deg2rad(grader)

# Funktion til at sende kommandoer til robotten via socket
def send_command(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((robot_ip, robot_port))
            s.sendall(command.encode('utf-8'))
            response = s.recv(1024)
            print(f"Modtaget svar: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Fejl ved sending af kommando: {e}")

# Funktion til at håndtere klientforbindelser
def handle_client_connection(client_socket):
    try:
        while True:
            command = client_socket.recv(1024).decode('utf-8')
            if not command:
                break
            print(f"Modtaget kommando: {command}")
            send_command(command)
            client_socket.sendall(b"Kommando modtaget")
    except Exception as e:
        print(f"Fejl: {e}")
    finally:
        client_socket.close()

# Hovedfunktion til at starte serveren
def main():
    server_ip = "192.168.0.5"  # Lyt på alle netværksinterfaces
    server_port = 30000  # Port til serveren

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((server_ip, server_port))
            server_socket.listen(5)
            print(f"Server lytter på {server_ip}:{server_port}")

            while True:
                client_socket, addr = server_socket.accept()
                print(f"Forbundet til klient: {addr}")
                handle_client_connection(client_socket)

                # Positioner i radianer
                position1 = [
                    grader_til_radianer(132),
                    grader_til_radianer(-20.42),
                    grader_til_radianer(-17.94),
                    grader_til_radianer(-53.79),
                    grader_til_radianer(-86.37),
                    grader_til_radianer(333.03),
                ]

                position2 = [
                    grader_til_radianer(109.20),
                    grader_til_radianer(-82.60),
                    grader_til_radianer(87.71),
                    grader_til_radianer(-97.17),
                    grader_til_radianer(-89.53),
                ]

                # Send positioner til robotten
                command1 = f"movej([{','.join(map(str, position1))}], a=1.2, v=0.25)\n"
                command2 = f"movej([{','.join(map(str, position2))}], a=1.2, v=0.25)\n"

                send_command(command1)
                time.sleep(2)  # Vent lidt mellem bevægelserne
                send_command(command2)
    except Exception as e:
        print(f"Fejl ved opstart af server: {e}")

if __name__ == "__main__":
    main()