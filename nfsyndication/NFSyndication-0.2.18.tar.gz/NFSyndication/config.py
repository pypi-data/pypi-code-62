#!/usr/bin/python 

def init():
  try:
   from NFSyndication import nfs_main, styles
  except Exception as e:
   print(f'Fatal: {e}')
  
  #return os.popen(f'{dir_path}/nfs_main.py').read()
  #run = lambda filename : exec(open(filename).read(), globals())
  #return run(f'{dir_path}/main.py')
  #fload = lambda filename : exec(open(filename).read(), globals())
  #return fload(f'{dir_path}/styles.py')
