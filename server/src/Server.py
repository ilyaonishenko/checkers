import socket

sock = socket.socket()
sock.bind(('', 8080))

sock.listen(5)
conn, addr = sock.accept()

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Server received: " + str(data))
    conn.send(("MR GRACHEV IS A DEFINETELY HUY").encode())

conn.close()
