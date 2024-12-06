import socket

# Opret en socket objekt
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket til din PC's IP-adresse og port
server_socket.bind(('192.168.0.5', 30000))  # Lyt på IP-adresse 192.168.0.5 på port 30002

# Lyt efter indkommende forbindelser
server_socket.listen(5)  # Tillad op til 5 ventende forbindelser
print("Server lytter på IP 192.168.0.5 og port 30000...")

try:
    while True:
        # Accepter en forbindelse
        client_socket, client_address = server_socket.accept()
        print(f"Forbundet til {client_address}")

        try:
            while True:
                # Modtag data fra klienten
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"Modtaget fra klient: {data}")

                # Send en besked tilbage til klienten
                response = "Hello from server\n"
                client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"En fejl opstod: {e}")
        finally:
            # Luk klientforbindelsen
            client_socket.close()
            print(f"Forbindelsen til {client_address} er lukket")

finally:
    # Luk serverforbindelsen
    server_socket.close()