from GitHubCommitsDownloader import GitHubCommitsDownloader
import os, sys, argparse

def getOptions(args=sys.argv[1:]):
	parser = argparse.ArgumentParser(usage=f"(ghcd or GitHubCommitDownloader) [-h] [-u USER] [-r REPO] [-b BRANCH]", description="GitHub Commit Downloader")
	parser.add_argument("-u", "--user", help="User's Github Name", required=True)
	parser.add_argument("-r", "--repo", help="User's Github Reposetory", required=True)
	parser.add_argument("-b", "--branch", help="User's Github Reposetory branch or \"all\"", default="all")
	parser.add_argument("-w", "--workingdir", help=f"Working directory for install github reposetories.", default=os.getcwd())
	options = parser.parse_args(args)
	return options

def run():
	options = getOptions()
	GitHubCommitsDownloader(options).parse()


if __name__ == "__main__":
	run()