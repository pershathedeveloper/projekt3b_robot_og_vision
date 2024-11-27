import socket

class DoosanRobot:
    def __init__(self, ip_address, port=12345):  # Standardporten til Doosan-robotter er 12345
        self.ip_address = ip_address
        self.port = port
        self.socket = None

    def connect(self):
        """Opret socket-forbindelse til robotten"""
        try:
            print(f"Prøver at forbinde til {self.ip_address} på port {self.port}...")
            self.socket = socket.create_connection((self.ip_address, self.port))
            print(f"Forbundet til Doosan robot på {self.ip_address}:{self.port}")
        except Exception as e:
            print(f"Fejl under forbindelse til Doosan robot: {e}")
            raise

    def move_to_position(self, position):
        """
        Flyt robotten til en kartesisk position.
        position: En liste [X, Y, Z, RX, RY, RZ] (X, Y, Z i meter, RX, RY, RZ i radianer)
        """
        try:
            # Formater positionen til en Doosan-kompatibel kommando
            x, y, z, rx, ry, rz = position
            command = f"movej([{x}, {y}, {z}, {rx}, {ry}, {rz}], 0.5, 0.5)\n"
            print(f"Sender kommando til robot: {command.strip()}")

            # Send kommandoen til robotten via socket
            self.socket.sendall(command.encode('utf-8'))
            print("Robotten bevæger sig til den angivne position")
        except Exception as e:
            print(f"Fejl under bevægelse: {e}")
            raise

    def disconnect(self):
        """Luk socket-forbindelsen"""
        if self.socket:
            try:
                print("Lukker forbindelsen til Doosan robot...")
                self.socket.close()
                print("Forbindelse til Doosan robot lukket")
            except Exception as e:
                print(f"Fejl under lukning af forbindelse: {e}")
