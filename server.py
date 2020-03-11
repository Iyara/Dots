import socket
import time


server = ""
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    print(e)

s.listen()
print("Server started, waiting for a connection.")

while True:
    conn, addr = s.accept()
    print("[CONNECT] New Connection!")




