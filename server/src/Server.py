import socket

sock = socket.socket()
sock.bind(('', 8080))

sock.listen(1)
conn, addr = sock.accept()

data = conn.recv(1024)

print("Server received: " + data)

conn.send(("MR GRACHEV IS A DEFINETELY HUY").encode())

conn.close()
