#!/usr/bin/env python
import argparse
import os

parser = argparse.ArgumentParser(description="This script takes a FASTA file and splits it in chunks of a given size. The size of the last chunk may be different. Output files append \"_\" and a number before the file extension")
parser.add_argument("input_path",help="Path to the input file")
parser.add_argument("chunk_size",help="Max number of sequences per output file",type=int)

args = parser.parse_args()

with open(args.input_path) as in_file:
	seq_dict = {}
	for line in in_file.readlines():
		line = line.strip()
		if line:
			if line.startswith(">"):
				header = line.lstrip(">")
				seq_dict[header] = ""
			else:
				seq = line.strip()
				seq_dict[header] = seq_dict[header] + seq

in_list = seq_dict.items()
chunk_list = [in_list[a:min(a+args.chunk_size,len(in_list))] for a in range(0,len(in_list),args.chunk_size)]


for a,chunk in enumerate(chunk_list):
	out_path = "_{0}".format(a).join(os.path.splitext(args.input_path))

	with open(out_path, "w") as out_file:
		for i,s in chunk:
			out_file.write(">{0}\n{1}\n".format(i,s))
