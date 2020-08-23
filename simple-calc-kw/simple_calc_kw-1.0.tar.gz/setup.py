# TODO: Fill out this file with information about your package

# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/

from setuptools import setup

setup(name='simple_calc_kw',
      version='1.0',
      description='To calculate the addition, subtraction, multiplication and division of two numbers. This exercise serves as a practice                       PyPi publishing',
      packages=['simple_calc'],
      author = 'Tan Ke Wei',
      author_email = 'keweiUTP@gmail.com',
      zip_safe=False #so that package can be run directly from a zipped file
     )
