import sys


def main():

    if sys.argv[1] == "-u":
        print("HELLO WORLD")
    elif sys.argv[1] == "-l":
        print("hello world")
    else:
        print("Please enter -l or -u as arguments ")
