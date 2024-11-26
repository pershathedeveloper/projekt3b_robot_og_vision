import socket # Importer socket library

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Lav et socket objekt til TCP/IP

# En server skal bindes til en specifik port da den ikke skal connect med en specifik enhed, men lytte efter indkomne connections
s.bind(('', 50007)) # Socket bindes til port 50007 hvor IP sættes til at være '' da det gør at socketen kan nåes af alle enhedens addresser
s.listen(1) # Socket sættes til at lytte på port 50007, 1 bytder at der kan være en indkomne connection i kø før at nye indkomne connections bliver smidt

conn, addr = s.accept() # En ny connection accepteres, dette returnere et nyt socket objekt (conn) specifikt til kommunikation mellem denne server og den specifikke client der tilsluttede
print('Connection from', addr) # Printer den connectede enhed for debugging

while True: # Forever loop
    data = conn.recv(4096) # Modtag en besked fra clienten via. recv funktionen ('4096' og '8192' anvedes ofte som buffer størrelse)
    if not data: break # Hvis data er 0 betyder det connectionen er brudt og while true loopet brydes så programmet stopper
    conn.sendall(data) # Beskeden sendes tilbage gennem socket via. sendall funktionen

conn.close() # Forbindelsen til clienten lukkes
s.close() # Socket lukkes