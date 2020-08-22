from setuptools import setup

setup(
  name = 'GitHubCommitsDownloader',
  packages = ['GitHubCommitsDownloader', 'GHCD'],
  version = '0.1',
  license = 'MIT',
  description = 'Github Commits Downloader App',
  author = 'MDReal',
  author_email = 'vminecrafter2015@gmail.com',
  url = 'https://github.com/user/reponame',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],
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
