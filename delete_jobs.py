#!/usr/bin/python
import os
import argparse

parser = argparse.ArgumentParser(description="This script takes two numbers, and deletes from the queue all the jobs with IDs in between those values, including both extremes")
parser.add_argument("start",help="First job to be deleted",type=int)
parser.add_argument("end",help="Last job to be deleted",type=int)
args = parser.parse_args()


for counter in range(args.start,args.end+1):
	cline = "qdel {0}".format(str(counter))
	print cline
	os.system(cline)

