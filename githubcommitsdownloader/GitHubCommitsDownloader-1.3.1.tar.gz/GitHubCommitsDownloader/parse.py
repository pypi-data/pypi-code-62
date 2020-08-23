from .log import log, Colors
from .request import request
from .clear import clear
from .ques import ques
import re

byURL = "Get repo from URL"
byOpt = "Get repo with questions"
def inp(q, i = 0, err = "Please try Again:"):
	x = ""
	while x == "":
		clear()
		if i == 1:
			q = f"{Colors.RED}{err}\n{q}{Colors.NONE}"
			i = 2
		else:
			i += 1
		q = f"{Colors.RED}{q}{Colors.NONE}  "
		print(Colors.YELLOW, sep="\r")
		x = input(q) or ""
		print(Colors.NONE, sep="\r")

	return x

def getRepoFromURL():
	q = "Enter URL:\n"
	url = inp(q)
	matches = re.match(r"^https:\/\/(?:www\.)?github\.com\/([^\s]+?)\/([^\s]+?)(?:$|\/(?:blob\/([^\s]+?)(?:\/|$))?)", url)
	if matches == None:
		while matches == None:
			url = inp(q, i = 1, err="Url's is not correct")
			matches = re.match(r"^https:\/\/(?:www\.)?github\.com\/([^\s]+?)\/([^\s]+?)(?:$|\/(?:blob\/([^\s]+?)(?:\/|$))?)", url)
	user, repo, branch = matches.groups()

	if not branch == None:
		resp = request(f"https://api.github.com/repos/{user}/{repo}/branches")
		branches = []

		for b in [*resp, {"name":"all"}]:
			branches.append(b.get('name'))

		branch = ques(f"{q}  {url}\nSelect Branch", branches)

	return user, repo, branch


def getRepoFromOpt(err = ""):
	user = inp(f"{err}Enter GitHub username:\n")
	userGitHub = f"https://api.github.com/users/{user}"
	resp = request(userGitHub)
	if resp.get('message') == "Not Found":
		return getRepoFromOpt(err = "Github Username not Found\n")
	resp = request(userGitHub + "/repos")
	repos = []
	if len(resp) > 0:
		for repo in resp:
			repos.append(repo.get('name'))
	
	repo = ques("Select an Reposetory", repos)

	resp = request(f"https://api.github.com/repos/{user}/{repo}/branches")
	branches = []

	for b in [*resp, {"name":"all"}]:
		branches.append(b.get('name'))

	branch = ques(f"Select Branch", branches)

	return user, repo, branch

def parse(_user, _repo, _branch):
	if _user or _repo or _branch:
		user, repo, branch = _user, _repo, _branch
		if not _user:
			raise Exception("User is empty use -u or --user ...")
		
		userGitHub = f"https://api.github.com/users/{user}"
		resp = request(userGitHub)
		if resp.get('message') == "Not Found":
			raise Exception("User Not Found")
		user = _user

		if not _repo:
			raise Exception("Reposetory is empty use -r or --repo ...")

		resp = request(userGitHub + "/repos")
		repos = []
		for repo in resp:
			repos.append(repo.get('name'))
		if not _repo in repos:
			raise Exception(f"User's have not Reposetory with named {_repo}")
		repo = _repo
		
		if not _branch:
			raise Exception("Branch is empty use -b or --branch ...")

		resp = request(f"https://api.github.com/repos/{user}/{_repo}/branches")
		branches = []

		for b in [*resp, {"name": "all"}]:
			branches.append(b.get('name'))

		for b in _branch.split(","):
			if not b.strip() in branches:
				raise Exception(f"Branch({b}) is not exists in this Reposetory")
		branch = _branch

	else:	
		parseMethod = ques("Please select parse method", [byURL, byOpt])
		if parseMethod == byURL:
			user, repo, branch = getRepoFromURL()
			
		elif parseMethod == byOpt:
			user, repo, branch = getRepoFromOpt()

		else:
			raise Exception("Select parse Method")
		
	return user, repo, branch