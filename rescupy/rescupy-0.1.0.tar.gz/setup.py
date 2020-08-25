# Source:
# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
# Example:
# pip install --user twine
# python setup.py sdist
# twine upload dist/*
from distutils.core import setup
setup(
   name = 'rescupy',         # How you named your package folder (MyLib)
   packages = ['rescupy'],   # Chose the same as "name"
   version = '0.1.0',      # Start with a small number and increase it with every change you make
   license='Proprietary',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
   description = 'RESCUPy is a Python interface for the Fortran-2008 version of RESCU.',   # Give a short description about your library
   author = 'Vincent Michaud-Rioux',                   # Type in your name
   author_email = 'vincentm@nanoacademic.com',      # Type in your E-Mail
   url = 'https://github.com/vincentmr/rescupy',   # Provide either the link to your github or to your website
   download_url = 'https://github.com/vincentmr/rescupy/archive/v0.1.0.tar.gz',    # I explain this later on
   keywords = ['RESCU', 'RESCUF08', 'RESCUPy', 'DFT'],   # Keywords that define your package best
   install_requires=[            # I get to this in a second
      'h5py',
      'matplotlib',
      'numpy',
      'scipy',
         ],
   classifiers=[
      'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
      'Intended Audience :: Developers',      # Define that your audience are developers
      'Topic :: Software Development :: Build Tools',
      'License :: Other/Proprietary License',   # Again, pick a license
      'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
  ],
)