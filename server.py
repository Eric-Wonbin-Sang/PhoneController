import socket

host = ''        # Symbolic name meaning all available interfaces
port = 12345     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print("HOST IP: ", socket.gethostbyname(socket.gethostname()))
print(host, port)

s.listen(1)
conn, address = s.accept()
print('Connected by', address)

while True:

    try:
        data = conn.recv(1024)
        if data:
            print("Client Says: " + str(data))
            conn.sendall(b"Server received data")

    except socket.error:
        print("Disconnected with device")
        s.listen(1)
        conn, address = s.accept()


# conn.close()
