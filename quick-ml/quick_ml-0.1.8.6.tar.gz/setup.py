from distutils.core import setup
setup(
  name = 'quick_ml',         # How you named your package folder (MyLib)
  packages = ['quick_ml'],   # Chose the same as "name"
  version = '0.1.8.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'quick_ml : ML For Everyone. Making Deep Learning through TPUs accessible to everyone. Lesser Code, faster computationm, better modelling.',   # Give a short description about your library
  author = 'Antoreep Jana',                   # Type in your name
  author_email = 'antoreepjana@gmail.com',      # Type in your E-Mail
  url = 'https://gitlab.com/antoreep_jana/quick_ml',   # Provide either the link to your github or to your website
  download_url = 'https://gitlab.com/antoreep_jana/quick_ml/-/archive/v0.1.8.6/quick_ml-v0.1.8.6.tar.gz',    # I explain this later on
  keywords = ['quick_ml', 'TPU', 'Deep Learning TPU', 'tensorflow', 'deep learning'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'tensorflow==2.2.0'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)