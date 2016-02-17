#!/usr/bin/env python

import argparse
import os
import re

parser = argparse.ArgumentParser(description="This script takes a FASTA file with ensembl proteins, and extracts the fake proteins to a new file")
parser.add_argument("in_path",help="Path to the FASTA file with the Ensembl download")
parser.add_argument("out_path",help="Path to the output file")

args = parser.parse_args()

fake_regexp = re.compile(r'>?(\w*f\w*)')

with open(args.in_path,"r") as in_file:
	fake_list = []
	for entry in in_file.read().rstrip().split("\n>"):
		if re.match(fake_regexp,entry):
			# print "HIT", re.match(fake_regexp,entry).group(1)

			entry_lines = entry.rstrip().split("\n")
			header = re.match(fake_regexp,entry).group(1)
			seq = "".join([i.rstrip() for i in entry_lines[1:]])
			fake_list.append((header,seq))


out_folder = os.path.dirname(args.out_path)
if not os.path.isdir(out_folder):
	os.system("mkdir -p {0}".format(out_folder))

with open(args.out_path,"w") as out_file:
	for h,s in sorted(fake_list,key=lambda a:a[0]):
		out_file.write(">{0}\n{1}\n".format(h,s))

print "Finished"



