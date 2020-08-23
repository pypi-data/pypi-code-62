import os, zipfile, requests, sys, shutil
from .log import log, Colors

class Downloader():
	def __init__(self, url, file):
		self.url = url
		self.filename = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(file))), "archive.zip")
		self.to = file

	def download(self):
		try:
			try:
				os.remove(self.filename)
			except:
				pass
			with open(self.filename, "wb") as f:
				log("Downloading from:\n  " + self.url, Colors.GREEN)
				response = requests.get(self.url, stream=True)
				total_length = response.headers.get('content-length')
				if total_length is None:
					f.write(response.content)
				else:
					dl = 0
					total_length = int(total_length)
					for data in response.iter_content(chunk_size=16384):
						dl += len(data)
						f.write(data)
						done = int(50 * dl / total_length)
						log("[%s%s]" % ('\u2588' * done, ' ' * (50 - done)), sep='\r', end='', flush=True)
		except KeyboardInterrupt:
			print(self.filename + " is not Downloaded Fully\nWe Delete the file")
			os.remove(self.filename)
			sys.exit(0)
		except Exception:
			print("Error Found")
			os.remove(self.filename)

	def unzip(self):
		try:
			log("\nUnzipping:\n  " + self.filename + "\n", Colors.YELLOW)
			with zipfile.ZipFile(self.filename, 'r') as zip_ref:
				zip_ref.extractall(self.to)
			os.remove(self.filename)
		except Exception:
			if os.path.isdir(self.to) is not False:
				shutil.rmtree(self.to)
