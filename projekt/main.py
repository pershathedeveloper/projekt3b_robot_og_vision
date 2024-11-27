import socket

class RobotClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_command(self, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.sendall(command.encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")
            return response

if __name__ == "__main__":
    host = "192.168.0.51"  # IP-adressen på serveren
    port = 30006  # Serverens port

    client = RobotClient(host, port)

    print("Indtast 'move_to_position' for at flytte robotten eller 'stop' for at stoppe")
    while True:
        command = input("> ")
        if command.lower() == "exit":
            print("Lukker klienten...")
            break
        response = client.send_command(command)
        print(f"Respons fra serveren: {response}")
        print(f"TEST")