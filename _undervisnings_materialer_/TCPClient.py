import socket # Importer socket library
import time # Importer time library til at lave delays

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Lav et socket objekt til TCP/IP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Setup socket to be able to reconnect if program is crashed
s.connect(("127.0.0.1", 50007)) # Connect til lokal server via. IP = 127.0.0.1 og Port = 50007

msgToSend = "Hello World" # Beskeden der skal sendes
msgToSendInBinary = msgToSend.encode('ascii') # Beskeden konverteres fra en string til bytes

s.sendall(msgToSendInBinary) # Beskeden sendes gennem socket via. sendall funktionen

time.sleep(0.5) # Delay programmet med 0.5 sekunder (giver modtageren tid til at svarer)

receivedMsg = s.recv(4096) # Modtag en besked fra serveren via. recv funktionen (4096 eller 8192 anvedes ofte som buffer størrelse)
receivedMsgAsString = receivedMsg.decode('ascii') # Beskeden konverteres fra bytes til en string

print("Server said:", receivedMsgAsString) # Beskeden printes i terminalen for debugging

s.shutdown(socket.SHUT_RDWR) # Socket sender information til serveren om at den bliver lukket
s.close() # Socket lukkes