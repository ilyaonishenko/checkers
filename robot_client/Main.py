import socket

while(True):
    sock = socket.socket()
    sock.connect(('localhost', 8080))
    sock.send(('I WANNA PLAY').encode())

    data = sock.recv(1024)
    sock.close()

    if(data is not 'OFF'):
        pass
        #perform move



