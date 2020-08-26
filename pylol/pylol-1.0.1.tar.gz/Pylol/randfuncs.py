import random

### time, os, sys, math, datetime, random, json, asyncio, datetime

## Random Functions ###
def seed(a=None, version=2):
	random.seed(a, version)

def getstate():
	random.getstate()

def setstate(state):
	random.setstate(state)

def getrandbits(k):
		random.getrandbits(k)

def randrange(start, stop):
	random.randrange(start, stop)

def randint(a, b):
	random.randint(a, b)

def choice(seq):
	random.choice(seq)

def choices(population, weights=None, *, cum_weights=None, k=1):
	random.choices(population, weights, cum_weights, k)

def shuffle(x):
	random.shuffle(x)

def sample(population, k):
	random.sample(population, k)

def random():
	random.random()

def uniform(a,b):
	random.uniform(a, b)

def triangular(low, high, mode):
	random.triangular(low, high, mode)

def betavariate(alpha, beta):
	random.betavariate(alpha, beta)

def expovariate(lambd):
	random.expovariate(lambd)

def gammavariate(alpha, beta):
	random.gammavariate(alpha, beta)

def gauss(mu, sigma):
	random.gauss(mu, sigma)

def lognormvariate(mu, sigma):
	random.lognormvariate(mu, sigma)

def normalvariate(mu, sigma):
	random.normalvariate(mu, sigma)

def vonmisesvariate(mu, kappa):
	random.vonmisesvariate(mu, kappa)

def paretovariate(alpha):
	random.paretovariate(alpha)

def weibullvariate(alpha, beta):
	random.weibullvariate(alpha, beta)
