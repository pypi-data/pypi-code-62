import os

### OS FUNCS ###
def ctermid():
	os.ctermid()

def environ():
	os.environ()

def environb():
	os.environb()

def chdir(path):
	os.chdir(path)

def fchdir(fd):
	os.fchdir(fd)

def getcwd():
	os.getcwd()

def fsencode(filename):
	os.fsencode(filename)

def fsdecode(filename):
	os.fsdecode(filename)

def fspath(path):
	os.fspath(path)

def __fspath__():
	os.__fspath__()

def getenv(key, default=None):
	os.getenv(key, default)

def getenvb(key, default=None):
	os.getenvb(key, default)

def get_exec_path(env=None):
	os.get_exec_path(env)

def getegid():
	os.getegid()

def geteuid():
	os.geteuid()

def getgrouplist(user,group):
	os.getgrouplist(user,group)

def getgroups():
	os.getgroups()

def getlogin():
	os.getlogin()

def getpgid(pid):
	os.getpgid(pid)

def getpgrp():
	os.getpgrp()

def getppid():
	os.getppid()

def getpriority(which,who):
	os.getpriority(which, who)

def getreusid():
	os.getresuid()

def getresgid():
	os.getresgid()

def getuid():
	os.getuid()

def initgroups(username,gid):
	os.initgroups(username,gid)

def putenv(key,value):
	os.putenv(key,value)

def setegid(egid):
	os.setegid(egid)

def seteuid(euid):
	os.seteuid(euid)

def setgid(gid):
	os.setegid(gid)

def setgroups(groups):
	os.setgroups(groups)

def setpgrp():
	os.setpgrp()

def setpgid(pid,pgrp):
	os.setpgid(pid, pgrp)

def setpriority(which,who,priority):
	os.setpriority(which,who,priority)

def setregid(rgid,egid):
	os.setregid(rgid,egid)

def setresgid(rgid,egid,sgid):
	os.setresgid(rgid, egid, sgid)

def setresuid(ruid,euid,suid):
	os.setresuid(ruid, euid, suid)

def setreuid(ruid,euid):
	os.setreuid(ruid, euid)






