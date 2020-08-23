#!/usr/bin/python 
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

def init():
  #os.popen(f'{dir_path}/main.py')
  #return os.popen(f'{dir_path}/main.py').read()
  run = lambda filename : exec(open(filename).read(), globals())
  return run(f'{dir_path}/main.py')

def hold_stylesheet(): 
  fload = lambda filename : exec(open(filename).read(), globals())
  return fload(f'{dir_path}/styles.py')
