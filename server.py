import socket
from _thread import *
import random
import _pickle as pickle
import time
import math


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
    game_time = 0

    #receive a name from the client
    data = conn.recv(16)
    name = data.decode("utf-8")
    print("[LOG]", name, "connected to the server")

    #properties for new player
    color = colors[current_id]
    x, y = get_start_location(players)
    players[current_id] = {"x":x, "y":y,"color":color,"score":0,"name":name}

    # pickle data and send initial info to clients
    conn.send(str.encode(str(current_id)))

    while True:
        if start:
            game_time = round(time.time()-start_time)
            #if the game time passes the round time the game will stop
            if game_time >= ROUND_TIME:
                start = False

        try:
            #receive data from client
            data = conn.recv(32)
            if not data:
                break

            data = data.decode("utf-8")
            print("[DATA] Received", data, "from client id", current_id)

            #look for specific commands from received data
            if data.split(" ")[0] == "move":
                split_data = data.split(" ")
                x = int(split_data[1])
                y = int(split_data[2])
                players[current_id]["x"] = x
                players[current_id]["y"] = y


            send_data = pickle.dumps((balls,players, game_time))

            #send data back to clients
            conn.send(send_data)

        except Exception as e:
            print(e)
            break #if exception, disconnect client

        time.sleep(0.001)

    #when user disconnects
    print("[DISCONNECT] Name:", name, " Client Id:", current_id, "disconnected")
    connections -= 1
    del players[current_id]
    conn.close()



def get_start_location(players):
    #returns a tuple (x,y)

    x = random.randrange(0,W)
    y = random.randrange(0,H)

    return (x,y)


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
            for player in players:
                p = players[player]
                dis = math.sqrt((x - p["x"])**2 + (y - p["y"])**2)
                if dis <= START_RADIUS + p["score"]:
                    stop = False

            if stop:
                break

        balls.append((x,y, random.choice(colors)))




# Game

BALL_RADIUS = 5
START_RADIUS = 7
W, H = 1600, 830
players = {}
balls = []
connections = 0
colors = [(255,0,0), (255, 128, 0), (255,255,0), (128,255,0),(0,255,0),(0,255,128),(0,255,255),(0, 128, 255), (0,0,255), (0,0,255), (128,0,255),(255,0,255), (255,0,128),(128,128,128), (0,0,0)]
_id = 0
start = False
nxt = 1



# MAIN LOOP

print("[GAME] Setting up level")
create_balls(balls, random.randrange(200,250))
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


