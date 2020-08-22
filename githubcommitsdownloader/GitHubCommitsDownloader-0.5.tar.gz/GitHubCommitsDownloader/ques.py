from .getTerminalSize import getTerminalSize
from termcolor import colored
from .clear import clear
from .wait import wait
import sys

def write(mess):
	sys.stdout.write(str(mess))

def ques(question, answers):
	width, height = getTerminalSize()
	l = t = 0

	def ml():
		maxLen = 0
		for answer in answers:
			maxLen = max(len(answer) + 5, maxLen)
		return maxLen
	
	if isinstance(question, str) and isinstance(answers, list):
		while True:
			width, height = getTerminalSize()
			mw = ml()
			count = width // mw
			spaceBettween = int(((width - count * mw) / count))
			x = count
			y = int(len(answers) / count) + 1

			print(question + "?")
			# print(l, t)
			for i in range(y):
				for j in range(x):
					index = i * x + j
					if index < len(answers):
						mess = (">" if l == j and t == i else " ") + f" {answers[index]} " + ("<" if l == j and t == i else " ")
						write(mess + " " * (mw - len(mess)))
				write("\n")
			write("\n")

			a = wait()
			clear()
			if a[0] == "\x1b":
				
				# Top
				if a[2] == "A":
					t -= 1
					if t < 0:
						t = y - 1

					if t * y + l >= len(answers):
						t = y - 1
					
				# Bottom
				if a[2] == "B":
					t += 1
					if t >= y:
						t = 0

					if t * y + l >= len(answers):
						t = 0

				# Right
				if a[2] == "C":
					l += 1
					if l >= x:
						t += 1
						l = 0
						if t >= y:
							t = 0
							
					if t * y + l >= len(answers):
						l = 0
						t = 0

				# Left
				if a[2] == "D":
					l -= 1
					if l < 0:
						t -= 1
						l = x - 1
						if t < 0:
							t = y - 1

					# print(l, t, x, y, t * y + l, len(answers))
					if t * y + l > len(answers):
						l = x + len(answers) - x * y - 1
						t = y - 1


			if a[0] == "\x03":
				raise KeyboardInterrupt()
			if a[0] == "\r":
				break
		return answers[t * y + l]

	elif isinstance(question, str):
		raise Exception("First Argument (question) Must be string")

	else:
		raise Exception("Second Argument (answers) Must be list")