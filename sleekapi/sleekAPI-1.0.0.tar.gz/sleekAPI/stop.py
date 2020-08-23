import requests
import json

class stop:
	def __init__(self, token, test_id):
		self.token = token
		self.test_id = test_id
	
	def attack(self):
		payload = { 'test_id' : self.test_id }
		r = requests.post('https://api.sleek.to/tests/stop?token=' + str(self.token), data=payload)
		return r
