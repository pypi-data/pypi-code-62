from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name = 'GitHubCommitsDownloader',
	packages = ['GitHubCommitsDownloader'],
	version = '1.3.1',
	license = 'MIT',
	description = 'Github Commits Downloader App',
	author = 'MDReal',
	author_email = 'vminecrafter2015@gmail.com',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url = 'https://github.com/MDReal32/GitHubCommitsDownloader',
	download_url = 'https://github.com/MDReal32/GitHubCommitsDownloader/archive/master.zip',
	keywords = ['ss', 'github', 'commits', 'downloader', 'github commits downloader', 'githubcommitsdownloader'],
	install_requires=[
		'requests'
	],
	entry_points = {
		'console_scripts': [
			'GHCD=GitHubCommitsDownloader.exec:run',
			'GitHubCommitsDownloader=GitHubCommitsDownloader.exec:run'
		]
	},
	classifiers = [
		# 'Development Status :: 1 - Alpha',
		# 'Intended Audience :: Developers',
		# 'Topic :: Software Development :: Build Tools',
		# 'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.8',
	],
	python_requires='>=3.8',
)
