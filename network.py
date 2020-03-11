#network.py
import socket

class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = "44.233.18.91"
		self.port = 5555
		self.addr = (self.server, self.port)
		self.name = name
		self.connect()

	def connect(self):
		self.client.connect(self.addr)
		return self.client.recv(2048).decode()

	def send(self, data):
		try:
			self.client.send(str.encode(data))
			reply = self.client.recv(2048).decode()
			return reply
		except socket.error as e:
			return str(e)
