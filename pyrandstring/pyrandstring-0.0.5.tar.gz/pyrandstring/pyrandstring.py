#!/usr/bin/python

import sys
import random
import os
import time
 
class pyrandstring:
 
	length = 18
	seed = ''
	tmp_str =''
	file = ''
 
	def __init__(self):
		self.length = 18
		self.seed = 'all'

	def getStringUnique(self):
		return str(int(time.time())) + "_" + self.getString(16,'anum')
		
 
	def getString(self,length=None,seed=None):

		if length is not None:
			self.length = length
 		
 		'''
		if file is not None:
			self.file = file
		'''
		if seed is None:
			seed='all'
		
		options = { 'abc': self.__abc, 'num': self.__num, 'anum': self.__anum , 'all': self.__all, 'bash': self.__bash}
		options[seed]()

		self.tmp_str = ''

		stop = int(self.length)
		a = 0
		while a < stop:
			self.tmp_str = self.tmp_str + str(self.seed[random.randint(0,len(self.seed)-1)])
			a = a + 1
			
		return self.tmp_str

	def __abc(self):
		self.seed = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
		'a', 'b', 'c', 'd', 'e', 'f', 'g', '', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
 
	def __num(self):
		self.seed = ['0', '1' , '2', '3', '4', '5', '6', '7', '8', '9']
 
	def __anum(self):
		self.seed = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
		'a', 'b', 'c', 'd', 'e', 'f', 'g', '', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
		'0', '1' , '2', '3', '4', '5', '6', '7', '8', '9']
 
	def __all(self):
 
		self.seed = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
		'a', 'b', 'c', 'd', 'e', 'f', 'g', '', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
		'0', '1' , '2', '3', '4', '5', '6', '7', '8', '9',
		'!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', '{', '|', '}', '~', '@']

	def __bash(self):
 
		self.seed = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
		'a', 'b', 'c', 'd', 'e', 'f', 'g', '', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
		'0', '1' , '2', '3', '4', '5', '6', '7', '8', '9',
		'!', '#', '$', '%', '&', '*', '+', ',', '-', '.', '/', '{', '|', '}', '~', '@']
 

