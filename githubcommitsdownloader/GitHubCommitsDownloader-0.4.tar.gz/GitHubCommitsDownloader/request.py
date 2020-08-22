import requests, json, sys
from datetime import datetime

def request(url):
	req = requests.get(url)
	try:
		if int(req.headers.get("X-Ratelimit-Remaining")) == 0:
			raise ""
		return json.loads(req.content)
	except:
		raise Exception(f"Please wait to {datetime.fromtimestamp(int(req.headers.get('X-Ratelimit-Reset'))).strftime('%Y-%m-%d %H:%M:%S')}")