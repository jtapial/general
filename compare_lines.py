#!/usr/bin/env python
import argparse
import os

parser = argparse.ArgumentParser(description="This takes two TSV files, and returns three files: one with the common lines (common.txt), one with the lines only in the first file (only_a.txt), and one with the lines only in the second file (only_b.txt). An option to sort output for the case of VASTDB-ENSEMBL files is added")
parser.add_argument("in_path_a",help="Path to the first file")
parser.add_argument("in_path_b",help="Path to the second file")
parser.add_argument("-out", help="Path to the folder where the three files will be written. Default is cwd. Will be created if needed",default=".")
parser.add_argument("-sort_mappings",action="store_true")

args = parser.parse_args()

if not os.path.isdir(a) and args.out !=".":
	os.system("mkdir -p {0}")

with open(args.in_path_a) as in_file_1:
	a = [line for line in in_file_1.readlines() if line.strip()]

with open(args.in_path_b) as in_file_2:
	b = [line for line in in_file_2.readlines() if line.strip()]


a = set(a)
b = set(b)

c = a & b
d = a - b
e = b - a

c = list(c)
d = list(d)
e = list(e)

def sort_for_mappings(a):
	return a.sort(key=lambda a:(a.split("\t")[0],
					int(a.split("\t")[1]),
					a.split("\t")[2],
					a.split("\t")[3],
					int(a.split("\t")[4]),
					a.split("\t")[5],
					a.split("\t")[6],
					a.split("\t")[7],
					int(a.split("\t")[8]),
					a.split("\t")[9],
					int(a.split("\t")[10]),
					a.split("\t")[11],
					int(a.split("\t")[12])))


if args.sort_mappings:
	c = sort_for_mappings(c)
	d = sort_for_mappings(d)
	e = sort_for_mappings(e)

with open(os.path.join([args.out,"common.txt"]),"w" as out_file):	
	for x in c:
		out_file.write(x)

with open(os.path.join([args.out,"only_a.txt"]),"w" as out_file):	
	for x in d:
		out_file.write(x)

with open(os.path.join([args.out,"only_b.txt"]),"w" as out_file):	
	for x in e:
		out_file.write(x)





