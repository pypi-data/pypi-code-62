#!/usr/bin/python3

import aimslib.detailed_roster.process as dr

s = open("/home/jon/tmp/DW401_1333717754.htm").read()
l = dr.lines(s)
bstream = dr.basic_stream(dr.extract_date(l), dr.columns(l))
for e in bstream:
    print(e)
