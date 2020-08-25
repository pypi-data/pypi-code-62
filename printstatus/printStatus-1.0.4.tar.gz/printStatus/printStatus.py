import sys


def progressBar(iteration, total, prefix='', suffix='', decimals=2, barLength=80, color='g'):
    """
    Call in a loop to create a progress bar in the terminal.

    Parameters:
        iteration - Required: current iteration (int)
        total     - Required: total iterations (int)
        prefix    - Optional: prefix string (str)
        suffix    - Optional: suffix string (str)
        decimals  - Optional: number of printed decimals (int)
        barLength - Optional: length of the progress bar in the terminal (int)
        color     - Optional: color identifier (str)
    """
    if   color == 'y': color = '\033[43m'
    elif color == 'k': color = '\033[40m'
    elif color == 'r': color = '\033[41m'
    elif color == 'g': color = '\033[42m'
    elif color == 'b': color = '\033[44m'
    elif color == 'm': color = '\033[45m'
    elif color == 'c': color = '\033[46m'

    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = color + ' '*filledLength + '\033[49m' + ' '*(barLength - filledLength - 1)
    sys.stdout.write('\r%s |%s| %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()


def module(outputlabel):
    """
    Print the name of the currently active module. 

    Parameters: 
        outputlabel - Required: Message to be printed (str)
    """
    sys.stdout.write("\n\033[0;37m"+outputlabel+"\033[0;39m")
    sys.stdout.flush(); print("")


def running(outputlabel):
    """
    Print a new message to stdout with the tag "Running". 

    Parameters:
        outputlabel - Required: Message to be printed (str)
    """
    sys.stdout.write("\r [ "+'\033[0;37m'+"RUNNING "+'\033[0;39m'+"] "+outputlabel)
    sys.stdout.flush(); print("")


def updateDone(outputlabel, progressbar=False):
    """
    Overwrite the previous message in stdout with the tag "Done" and a new message. 

    Parameters: 
        outputlabel - Required: Message to be printed (str)
        progressbar - Optional: Set True if the previous message was the progress bar (bool)
    """
    if progressbar == True:
        sys.stdout.write("\033[K")
    sys.stdout.write("\033[F"); sys.stdout.write("\033[K")
    sys.stdout.write("\r\r [ "+'\033[0;32m'+"DONE    "+'\033[0;39m'+"] "+outputlabel)
    sys.stdout.flush(); print("")


def done(outputlabel):
    """
    Print a new message to stdout with the tag "Done". 

    Parameters: 
        outputlabel - Required: Message to be printed (str)
    """
    sys.stdout.write("\r\r [ "+'\033[0;32m'+"DONE    "+'\033[0;39m'+"] "+outputlabel)
    sys.stdout.flush(); print("")


def updateWarning(outputlabel, progressbar=False):
    """
    Overwrite the previous message in stdout with the tag "Warning" and a new message. 

    Parameters: 
        outputlabel - Required: Message to be printed (str)
        progressbar - Optional: Set True if the previous message was the progress bar (bool)
    """
    if progressbar == True:
        sys.stdout.write("\033[K")
    sys.stdout.write("\033[F"); sys.stdout.write("\033[K")
    sys.stdout.write("\r\r [ "+'\033[0;33m'+"WARNING "+'\033[0;39m'+"] "+outputlabel)
    sys.stdout.flush(); print("")


def warning(outputlabel):
    """
    Print a new message to stdout with the tag "Warning". 

    Parameters: 
        outputlabel - Required: Message to be printed (str)
    """
    sys.stdout.write("\r\r [ "+'\033[0;33m'+"WARNING "+'\033[0;39m'+"] "+outputlabel)
    sys.stdout.flush(); print("")


def updateFailed(outputlabel, progressbar=False):
    """
    Overwrite the previous message in stdout with the tag "Failed" and a new message. 

    Parameters: 
        outputlabel - Required: Message to be printed (str)
        progressbar - Optional: Set True if the previous message was the progress bar (bool)
    """
    if progressbar == True:
        sys.stdout.write("\033[K")
    sys.stdout.write("\033[F"); sys.stdout.write("\033[K")
    sys.stdout.write("\r\r [ "+'\033[0;31m'+"FAILED  "+'\033[0;39m'+"] "+outputlabel)
    sys.stdout.flush(); print("")


def failed(outputlabel):
    """
    Print a new message to stdout with the tag "Failed". 

    Parameters: 
        outputlabel - Required: Message to be printed (str)
    """
    sys.stdout.write("\r\r [ "+'\033[0;31m'+"FAILED  "+'\033[0;39m'+"] "+outputlabel)
    sys.stdout.flush(); print("")


