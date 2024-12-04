import socket

class RobotArmRTDE:
    def __init__(self, ip_address="192.168.1.10", port=30004):
        self.ip_address = ip_address
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip_address, self.port))
        print(f"Connected to robot at {self.ip_address}:{self.port}")

    def sendCommand(self, command):
        if self.socket:
            self.socket.sendall(command.encode('utf-8'))
            print(f"Sent command: {command}")

    def receiveData(self):
        if self.socket:
            return self.socket.recv(4096).decode('utf-8')

    def close(self):
        if self.socket:
            self.socket.close()
            print("Connection closed.")
