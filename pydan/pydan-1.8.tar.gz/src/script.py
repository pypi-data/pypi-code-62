#!/usr/bin/env python3

import sys
import os

# Directorio del script principal
#scriptdir=sys.path[0]

# Cambiamos al directorio del script principal
#os.chdir(scriptdir)

# Utilizamos scriptdir/lib como path para los import
#sys.path.insert(1,scriptdir+'/lib')

# Cambiamos el nombre del proceso al del script
import setproctitle
setproctitle.setproctitle(os.path.basename(sys.argv[0]))

# Excepciones coloreadas
import colored_traceback.always

# Exportamos scriptdir al script principal
#import __main__
#__main__.scriptdir=scriptdir

def parsecmdline():
	cmdline={}
	cmdline["params"]=[]
	cmdline["options"]={}
	i=0
	while i < len(sys.argv)-1:
		i+=1
		s=sys.argv[i]
		if '=' in s:
			keyval=s.split("=")
			cmdline["options"][keyval[0]]=keyval[1]
		elif s[0]=='-':
			i+=1
			val=sys.argv[i]
			key=s[1:]
			if (key[0]=='-'):
				key=key[1:]
			cmdline["options"][key]=val
		else:
			cmdline["params"].append(s)
	if not cmdline["params"]:
		cmdline["cmd"]=""
	else:
		cmdline["cmd"]=cmdline["params"][0]
	return cmdline
