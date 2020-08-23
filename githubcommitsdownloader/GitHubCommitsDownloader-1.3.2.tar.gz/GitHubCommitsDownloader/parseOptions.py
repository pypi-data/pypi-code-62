import os, argparse
from .request import request

def get(opts, key):
	try:
		return opts.get(key)
	except:
		return opts[key]

def checkUser(username):
	request()

def parseOptions(options):
	try:
		root = options.workingdir
	except:
		root = os.getcwd()
	
	if type(options) == str:
		user, repo, _ = options.split("/")
		if not user:
			raise Exception("User is not correctly entered")
		if not repo:
			raise Exception("Reposetory is not correctly entered")
		if _ is not None:
			raise Exception("Enter only support \"user/repo\" format")


	package = get(options, "package")
	if package:
		user, repo, _ = options.split("/")
		if not user:
			raise Exception("User is not correctly entered")
		if not repo:
			raise Exception("Reposetory is not correctly entered")
		if _ is not None:
			raise Exception("Enter only support \"user/repo\" format")

	else:
		user = get(options, "user")
		repo = get(options, "repo")
		
		if not user:
			raise Exception("User is not correctly entered")
		if not repo:
			raise Exception("Reposetory is not correctly entered")
	
	userData = request(f"https://api.github.com/users/{user}")
	if userData.get("message") == "Not Found":
		raise Exception("User is not Defined")

	repoData = request(f"https://api.github.com/users/{user}/repos")
	repos = []
	for _repo in repoData:
		repos.append(repo.name)
	
	if not repo in repos:
		raise Exception("Entered reposetory is not Defined")

	branch = get("options", "branch")
	if not branch:
		branch = "all"
	
	return root, user, repo, branch