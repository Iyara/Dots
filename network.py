#network.py
import socket
import _pickle as pickle

class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.client.settimeout(10.0)
		self.server = "44.233.18.91"
		self.port = 5555
		self.addr = (self.server, self.port)

	def connect(self, name):
		self.client.connect(self.addr)
		self.client.send(str.encode(name))
		val = self.client.recv(8)
		return int(val.decode()) # can be int because will be an int id

	def disconnect(self):
		self.client.close()

	def send(self, data, pick=False):
		'''
		try:
			self.client.send(str.encode(data))
			reply = self.client.recv(2048).decode()
			return reply
		except socket.error as e:
			return str(e)
		'''
		try:
			if pick:
				self.client.send(pickle.dumps(data))
			else:
				self.client.send(str.encode(data))
			reply = self.client.recv(2048*4)
			try:
				reply = pickle.loads(reply)
			except Exception as e:
				print(e)

			return reply
		except socket.error as e:
			print(e)
