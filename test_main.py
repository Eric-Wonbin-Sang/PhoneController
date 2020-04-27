import socket
import random

host = socket.gethostname()
port = 12345                   # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    s.sendall(bytes(str(random.random()), "ascii"))
    data = s.recv(1024)
    print('Received', repr(data))


s.close()
