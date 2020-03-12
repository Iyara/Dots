import socket
from _thread import *
import random

server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    print(e)
    quit()

s.listen()
print("Server started at ", server, ", waiting for a connection.")


# Functions

def threaded_client(conn, _id):
    global connections, players, balls, nxt, start

    current_id = _id

    #receive a name from the client
    data = conn.recv(16)
    name = data.decode("utf-8")
    print("[LOG]", name, "connected to the server")

    #properties for new player
    color = colors[current_id]

    players[current_id] = {"x":x, "y":y,"color":color,"score":0,"name":name}

    # pickle data and send initial info to clients
    conn.send(str.encode(str(current_id)))




# Game

BALL_RADIUS = 5
START_RADIUS = 7

players = {}
balls = []
connections = 0
colors = [(255,0,0), (255, 128, 0), (255,255,0), (128,255,0),(0,255,0),(0,255,128),(0,255,255),(0, 128, 255), (0,0,255), (0,0,255), (128,0,255),(255,0,255), (255,0,128),(128,128,128), (0,0,0)]
_id = 0
start = False
nxt = 1

def create_balls(balls, n):
    print("n", n)
    '''
    creates orbs/balls on the screen
    balls: a list to add balls/orbs to
    n: the amount of balls to make
    '''
    for i in range(n):
        while True:
            stop = True
            x = random.randrange(0,W)
            y = random.randrange(0,H)
            balls.append((x,y, random.choice(colors)))


# MAIN LOOP

print("[GAME] Setting up level")
create_balls(balls, random.randrange(200,250)
print("[SERVER] Waiting for connections")

# keep looking for new connections
while True:
    host, addr = s.accept()
    print("[CONNECTION] Connected to:", addr)

    #start game when client connects
    if addr[0] == server and not(start):
        start = True
        start_time = time.time()
        print("[GAME] Game started")

    connections += 1
    start_new_thread(threaded_client,(host, _id))
    _id += 1

# program ends
print("[SERVER] Server offline")


