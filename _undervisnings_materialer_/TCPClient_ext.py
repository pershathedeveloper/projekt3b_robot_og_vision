import socket # Importer socket library
import time # Importer time library til at lave delays
import pickle

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Lav et socket objekt til TCP/IP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Setup socket to be able to reconnect if program is crashed
s.connect(("127.0.0.1", 50007)) # Connect til lokal server via. IP = 127.0.0.1 og Port = 50007

msgToSend = "Hello World" # Beskeden der skal sendes
msgToSendInBinary = msgToSend.encode('ascii') # Beskeden konverteres fra en string til bytes

s.sendall(msgToSendInBinary) # Beskeden sendes gennem socket via. sendall funktionen

time.sleep(0.5) # Delay programmet med 0.5 sekunder (giver modtageren tid til at svarer)

d = {1:"hi", 2: "there"}
msg = pickle.dumps(d)
msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
print(msg)
s.send(msg)

receivedMsg = s.recv(16) # Modtag en besked fra serveren via. recv funktionen (4096 eller 8192 anvedes ofte som buffer størrelse)
receivedMsgAsString = receivedMsg.decode('ascii') # Beskeden konverteres fra bytes til en string

print("Server said:", receivedMsgAsString) # Beskeden printes i terminalen for debugging

while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        print(f"full message length: {msglen}")

        full_msg += msg

        print(len(full_msg))

        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            print(pickle.loads(full_msg[HEADERSIZE:]))
            new_msg = True
            full_msg = b""
            break
    break

s.shutdown(socket.SHUT_RDWR) # Socket sender information til serveren om at den bliver lukket
s.close() # Socket lukkes