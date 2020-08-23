import os, argparse
from .request import request

def toDict(opts):
	if type(opts) == argparse.Namespace:
		return vars(opts)
	else:
		return opts

def checkUser(username):
	request()

def parseOptions(options):
	options = toDict(options)
	
	try:
		root = options.get('workingdir')
	except:
		root = os.getcwd()
	
	if isinstance(options, str):
		try:
			user, repo = options.split("/")
		except ValueError as exc:
			raise Exception("Enter only support \"user/repo\" format")

		if not user:
			raise Exception("User is not correctly entered")
		if not repo:
			raise Exception("Reposetory is not correctly entered")


	package = options.get("package")
	if package:
		try:
			user, repo = package.split("/")
		except ValueError as exc:
			raise Exception("Enter only support \"user/repo\" format")

		if not user:
			raise Exception("User is not correctly entered")
		if not repo:
			raise Exception("Reposetory is not correctly entered")

	else:
		user = options.get("user")
		repo = options.get("repo")
		
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
		repos.append(_repo.get('name'))
	
	if not repo in repos:
		raise Exception("Entered reposetory is not Defined")

	branch = options.get("branch")
	if not branch:
		branch = "all"
	
	return root, user, repo, branch