import os, sys
from .clear import clear
from .parse import parse
from .GitHub import GitHub
from .parseOptions import parseOptions
import argparse

clear()

class GitHubCommitsDownloader():
	def __init__(self, options):
		root, user, repo, branch = parseOptions(options)
		self.root = root
		self.user = user
		self.repo = repo
		self.branch = branch

	def parse(self):
		GitHub(*parse(self.user, self.repo, self.branch), self.root)