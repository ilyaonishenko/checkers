import socket

sock = socket.socket()
sock.bind(('', 8080))

sock.listen(1)

while True:
    conn, addr = sock.accept()
    data = conn.recv(1024)

    if not data:
        continue
    print("Server received: " + str(data))

    conn.send(("MR GRACHEV IS A DEFINETELY HUY").encode())

print('closed')
conn.close()

