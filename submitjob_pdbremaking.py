#!/usr/bin/env python

import argparse
import os
import re
import math

#ARGUMENT HANDLING:
#----------------------------------------

parser = argparse.ArgumentParser(description="SUBMITJOB SCRIPT FOR PDB REFORMATTING")
parser.add_argument("-chunks",help="number of jobs that will be sent",default=1,type=int)
parser.add_argument("-job_name",help="generic name for the jobs",default="pdb_seq_filtering")
parser.add_argument("pdb_dir",help="path to the PDB raw download")
parser.add_argument("in_fasta_path",help="path to the FASTA containing the unfiltered PDB sequences")
parser.add_argument("out_dir",help="directory where all the output files will be created")
parser.add_argument("list_fname",help="generic filename for the PDB list files (<your_input>-<chunk_index>.txt)")
parser.add_argument("out_fname",help="generic filename for the output FASTA files (<your_input>-<chunk_index>.fasta")

args = parser.parse_args()

assert os.path.isdir(args.pdb_dir),"Path to PDB folder cannot be found. Please use a valid path"	
assert os.path.isfile(args.in_fasta_path),"Path to PDB FASTA file cannot be found. Please use a valid path"

print "Getting list of PDB entries to be parsed..."
path_list = []

for root,dirs,files in os.walk(args.pdb_dir):
	for filename in files:
		if filename.endswith(".pdb"):
			path_list.append(os.path.join(root,filename))

print len(path_list), "PDB files will be parsed using", args.chunks, "jobs"

#Ensure a number of chunks equal to args.chunks - 1:
chunk_size = int(math.ceil(len(path_list)/float(args.chunks)))
chunks_list = [path_list[offset:min(offset + chunk_size, len(path_list))] for offset in range(0,len(path_list),chunk_size)]

print "Chunk size:", chunk_size

print "Output directory:", args.out_dir
if not os.path.isdir(args.out_dir):
	os.system("mkdir -p {0}".format(args.out_dir))

print "Dumping PDB paths into files..."
list_files = []
for i,chunk in enumerate(chunks_list):
	fname = args.list_fname + "_" + str(i) + ".txt"
	print "File", os.path.join(args.out_dir,fname)
	with open(os.path.join(args.out_dir,fname),"w") as list_file:
		list_files.append(os.path.join(args.out_dir,fname))
		list_file.write("\n".join(chunk))

print "Sending jobs..."

for i,element in enumerate(list_files):
		os.system("submitjob.py -b y -q short -n {0}_{1} python -- $SRC/vastdb_maps/mapping_files_creation/pdb_remaking.py {2} {3} {4}/{5}{1}.fasta".format(args.job_name,i,element,args.in_fasta_path,args.out_dir,args.out_fname))

print "===========Jobs submitted==========="



