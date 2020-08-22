import os
from .clear import clear
from .parse import parse
from .GitHub import GitHub

clear()

class GitHubCommitsDownloader():
	def __init__(self, options):
		try:
			self.root = options.workingdir
		except:
			self.root = os.getcwd()
		print(type(options))
		if not options.user:
			raise Exception("User is required; use { \"user\": \"UserName\" }")
		self.user = options.user
		if not options.repo:
			raise Exception("Repo is required; use { \"repo\": \"User's reposetory name\" }")
		self.repo = options.repo
		self.branch = options.branch

	def parse(self):
		user, repo, branch = parse(self.user, self.repo, self.branch)
		GitHub(user, repo, branch, self.root)