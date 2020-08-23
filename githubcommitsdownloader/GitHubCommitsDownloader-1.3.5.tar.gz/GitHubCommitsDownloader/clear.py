import os, platform

def clear():
	if platform.system() == "Windows":
		clear = lambda: os.system('cls')
	else:
		clear = lambda: os.system('clear')
	clear()