import os
from .clear import clear
from .parse import parse
from .GitHub import GitHub
import argparse

clear()

class GitHubCommitsDownloader():
	def __init__(self, options):
		try:
			self.root = options.workingdir
		except:
			self.root = os.getcwd()

		if type(options) == argparse.Namespace:
			if not options.user:
				raise Exception("User is required; use -u/--user UserName")
			self.user = options.user
			if not options.repo:
				raise Exception("Repo is required; use -r/--repo repo")
			self.repo = options.repo
		else:
			if not options.get('user'):
				raise Exception("User is required; use { \"user\": \"UserName\" }")
			self.user = options.get('user')
			if not options.get('repo'):
				raise Exception("Repo is required; use { \"repo\": \"User's reposetory name\" }")
			self.repo = options.get('repo')

		try:
			self.branch = options.branch
		except:
			self.branch = options.get('branch')

	def parse(self):
		user, repo, branch = parse(self.user, self.repo, self.branch)
		GitHub(user, repo, branch, self.root)