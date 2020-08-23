from .request import request 
from .Downloader import Downloader
from .mkdir import mkdir, initPath
from .log import log, Colors
import os, sys

def parseCommits(branch, root, user, repo, commits):
	commits = request(commits)
	commitIndex = 0

	for commit in commits:
		sha = commit.get('sha')
		commit = f"https://github.com/{user}/{repo}/archive/{sha}.zip"
		pathData = root, "github", user, repo, branch, f"{commitIndex}:{sha[:6]}"
		mkdir(*pathData)
		downloader = Downloader(commit, initPath(*pathData))
		downloader.download()
		downloader.unzip()
		commitIndex += 1


def GitHub(user, repo, branch, root):
	log(f"Hi. I'm Parsing {user}'s {repo}'s {branch} branch", Colors.PURPLE)
	if branch == "all":
		branch_urls = f"https://api.github.com/repos/{user}/{repo}/branches"
		branches = request(branch_urls)
		for branch in branches:
			branch = branch.get('name')
			log(f"Started Parse of {branch} branch", Colors.CYAN)
			parseCommits(branch, root, user, repo, f"https://api.github.com/repos/{user}/{repo}/commits?sha={branch}")

	else:
		for b in branch.split(","):
			log(f"Started Parse of {b} branch", Colors.CYAN)
			b = b.strip()
			parseCommits(b, root, user, repo, f"https://api.github.com/repos/{user}/{repo}/commits?sha={b}")