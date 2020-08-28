#!python

#A script wrapper for manually calling the store_tools.py function store()

import argparse
from runmonitor import store_tools

parser = argparse.ArgumentParser()
parser.add_argument("--level",type=int,default=1,help="The level to get the name from. Defaults to 1 i.e. the rundir, 2 would be the dir the rundir is in, etc.")
parser.add_argument("--rundir",type=str,help="the run directory")
parser.add_argument("--event",type=str,help="the string representing the event being run on")
parser.add_argument("--rmbase",type=str,default=None,help="the base runmon directory. If RUNMON_BASE is already in the env variables (and you want to use this as your base), do not pass this")
parser.add_argument("--cluster",type=str,default=None,help="the cluster this is maintained on. This should be fixed, so you should probably just set the RUNMON_CLUSTER env, but this is an alternative if necessary")
parser.add_argument("--envsh",type=str,default=None,help="a path to a single script that sets up the environment, to allow for self healing")
opts = parser.parse_args()
   
store(opts.event,opts.rundir,level=opts.level,rmbase=opts.rmbase,cluster=opts.cluster,envsh=opts.envsh)
