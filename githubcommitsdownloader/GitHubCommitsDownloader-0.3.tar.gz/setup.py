from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()


setup(
  name = 'GitHubCommitsDownloader',
  packages = ['GitHubCommitsDownloader', 'GHCD'],
  version = '0.3',
  license = 'MIT',
  description = 'Github Commits Downloader App',
  author = 'MDReal',
  author_email = 'vminecrafter2015@gmail.com',
	long_description=long_description,
	long_description_content_type="text/markdown",
  url = 'https://github.com/MDReal32/GitHubCommitsDownloader',
  download_url = 'https://github.com/MDReal32/GitHubCommitsDownloader/archive/master.zip',
  keywords = ['ss', 'github', 'commits', 'downloder', 'github commits downloader', 'githubcommitsdownloader'],
  install_requires=[
		'requests',
		'termcolor'
	],
	entry_points = {
		'console_scripts': [
			'ghcd=exec:run',
			'GitHubCommitDownloader=exec:run'
		]
	},
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
