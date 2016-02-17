#!/usr/bin/env python

#This script takes each two files with PDB sequences, and makes pairwise alignments between each pair of sequences (one from each PDB version)

import os
import re
import sys
import argparse
from Bio import Seq
from Bio import Alphabet
import subprocess

#ARG HANDLING
parser = argparse.ArgumentParser(description="This script takes two files with FASTA sequences, and makes pairwise alignments from each sequence in the first file to every sequence in the second file")

parser.add_argument("-ali", "--alignment", help="Alignment algorithm to be used. Can choose between 'nw' (Needleman-Wunsch, default), and 'sw' (Smith-Waterman)", default='nw', choices=["nw","sw"])
parser.add_argument("query", help="FASTA file from which the query sequences will be taken")
parser.add_argument("subject",help="FASTA file from which the target sequences will be taken")
parser.add_argument("dictionary", help="path to dictionary with relationships from query to subject")
parser.add_argument("-o", "--ali_out_path", help="Path to the file where the full alignments will be dumped")
parser.add_argument("-go","--gap_open",help="Gap openning penalty for the alignment, in float format (default:10.0)",default=10.0,type=float)
parser.add_argument("-ge","--gap_extension",help="Gap extension penalty for the alignment, in float format (default:0.5)",default=0.5,type=float)
parser.add_argument("-m","--matrix", help="Path to the matrix used for the alignment. Default is EBLOSUM62",default="EBLOSUM62")

args = parser.parse_args()

#INPUT VERIFICATION
assert os.path.isfile(args.query), "Query file not detected. Please enter a valid path to the query file"
assert os.path.isfile(args.subject), "Subject file not detected. Please enter a valid path to the query file"

if args.alignment == "nw" or args.alignment == "needle":
	args.alignment = "needle"
elif args.alignment == "sw" or args.alignment == "water":
	args.alignment = "water"
#Load EMBOSS SUITE NECESSARY FOR ALIGNMENT
os.system("source $SRC/old_scripts/env/eb_misc.sh")
os.system("module load EMBOSS/6.5.7-goolf-1.4.10-no-OFED")


#BUILD DICTS
query_dict = {}

with open(args.query,"r") as query_file:
	count = 0
	for entry in query_file.read().split("\n#")[0].split("\n>"): #Remove comments in the end
		count +=1
		if entry.strip():
			try:
				entry_lines = entry.split("\n")
				header = entry_lines[0].lstrip(">").strip().split()[0]
				seq = ''.join(line.strip() for line in entry_lines[1:])
				bp_seq = Seq.Seq(seq, Alphabet.IUPAC.protein)
				query_dict[header] = bp_seq
			except IndexError:
				print entry
				print count
				raise


subject_dict = {}
with open(args.subject,"r") as subject_file:
	for entry in subject_file.read().split("\n#")[0].split("\n>"): #Remove comments in the end
		if entry.strip():
			entry_lines = entry.split("\n")
			header = entry_lines[0].lstrip(">").strip().split()[0]
			seq = ''.join(line.strip() for line in entry_lines[1:])
			bp_seq = Seq.Seq(seq,Alphabet.IUPAC.protein)
			subject_dict[header] = bp_seq


filter_dict = {}
with open(args.dictionary) as dict_file:
	for line in dict_file.readlines():
		k,v = line.strip().split("\t")
		filter_dict[k] = v


#ALIGN AND SAVE TO FILE
if args.ali_out_path:
	out_file = open(args.ali_out_path,"w")
else:
	out_file = sys.stdout


for query_key, query_value in sorted(query_dict.items()):

	for subject_key,subject_value in sorted(subject_dict.items()):
		if subject_key.split("-")[0].startswith(filter_dict[query_key]):

			sp_args = [args.alignment,
						"-aseq",
						"asis::{0}".format(str(query_value)),
						"-sprotein1",
						"-sid1",
						query_key,
						"-bseq",
						"asis::{0}".format(str(subject_value)),
						"-sprotein2",
						"-sid2",
						subject_key,
						"-stdout",
						"-gapopen",
						str(args.gap_open),
						"-gapextend",
						str(args.gap_extension),
						"-datafile",
						args.matrix,
						"-auto",
						"-aformat",
						"fasta"]

			alignment_output = subprocess.check_output(sp_args)

			#The full output goes to its file
			out_file.write(alignment_output + '\n')

if args.ali_out_path:
	out_file.close()



print "==============ALIGNMENT COMPLETE==============="
print "Full results in: {0}".format(args.ali_out_path)




