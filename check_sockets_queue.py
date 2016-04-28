#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import commands
import argparse

parser = argparse.ArgumentParser(description='Check socket queue length.')
parser.add_argument('-p','--port', help='Port to check',required=True)
parser.add_argument('-i','--ip',help='if socket listen only on an IP', required=False, default="*")
args = parser.parse_args()

ret = commands.getstatusoutput("netstat -Lan | grep "+args.port)

value = None
warn = None
crit = None
min = None
max = None

lines = ret[1].split("\n")
for line in lines:
    detail = line.split()
    if detail[2] == args.ip+'.'+args.port:
        queue = detail[1].split("/")
        value = queue[0]
        max = queue[2]
        min = 0

if not value:
    print "STATE UNKNOWN"
    sys.exit(3)

# Determine state to pass to Nagios
# CRITICAL = 2
# WARNING = 1
# OK = 0
if int(value) >= int(max):
    print "Socket listen queue overflow : %s/%s|%s;;%s;%s;%s" % (value, max, value, max, min, max)
    sys.exit(2)
elif int(value) > 0:
    print "Socket listen queue increase : %s/%s|%s;;%s;%s;%s" % (value, max, value, max, min, max)
    sys.exit(1)
else:
    print "Socket listen queue OK : %s/%s|%s;;%s;%s;%s" % (value, max, value, max, min, max)
    sys.exit(0)
