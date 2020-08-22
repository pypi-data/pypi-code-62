import os
from clear import clear
from parse import parse
from GitHub import GitHub

clear()

class GitHubCommitsDownloader():
	def __init__(self, options):
		self.root = options.workingdir
		self.user = options.user
		self.repo = options.repo
		self.branch = options.branch

	def parse(self):
		user, repo, branch = parse(self.user, self.repo, self.branch)
		GitHub(user, repo, branch, self.root)