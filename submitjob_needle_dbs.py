#!/usr/bin/env python

import argparse
import os
import sys
import re

from Bio import Seq, Alphabet

#ARG HANDLING
parser = argparse.ArgumentParser(description="This script takes two files with FASTA sequences, and makes pairwise alignments from each sequence in the first file to every sequence in the second file")

parser.add_argument("-ali", "--alignment", help="Alignment algorithm to be used. Can choose between 'nw' (Needleman-Wunsch, default), and 'sw' (Smith-Waterman)", default='nw', choices=["nw","sw"])
parser.add_argument("query", help="FASTA file from which the query sequences will be taken")
parser.add_argument("subject",help="FASTA file from which the target sequences will be taken")
parser.add_argument("dictionary",help="dict showing query to subject relationships")
parser.add_argument("-o", "--ali_out_path", help="Generic path to the directory where the full alignments and chunk input files will be dumped")
parser.add_argument("-go","--gap_open",help="Gap openning penalty for the alignment, in float format (default:10.0)",default=10.0,type=float)
parser.add_argument("-ge","--gap_extension",help="Gap extension penalty for the alignment, in float format (default:0.5)",default=0.5,type=float)
parser.add_argument("-m","--matrix", help="Path to the matrix used for the alignment. Default is EBLOSUM62",default="EBLOSUM62")
parser.add_argument("-chunk_size",help="Number of chunks to split the query FASTA",type=int)

args = parser.parse_args()

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

chunks_list = [query_dict.items()[offset:min(offset + args.chunk_size,len(query_dict.items()))] for offset in range(0,len(query_dict.items()),args.chunk_size)]

for i,chunk in enumerate(chunks_list):
	chunk_fname = os.path.join(os.path.abspath(args.ali_out_path),"input_{0}.fasta".format(i))
	with open(chunk_fname,"w") as chunk_file:
		for h in chunk:
			chunk_file.write(">" + str(h[0]) + "\n" + str(h[1]) + "\n")


for i,chunk in enumerate(chunks_list):
	out_fname = os.path.join(os.path.abspath(args.ali_out_path),"ali_file_{0}.ali".format(i))
	chunk_fname = os.path.join(os.path.abspath(args.ali_out_path),"input_{0}.fasta".format(i))
	qn = os.path.split(args.query)[-1]
	sn = os.path.split(args.subject)[-1]

	os.system("submitjob.py -q long -n {0}_{1}_{2}_{3} -l h_rt=48:00:00 virtual_free=40G -b y needle_dbs.py -ali {0} --ali_out_path {4} -go {5} -ge {6} --matrix {7} {8} {9} {10}".format(args.alignment,qn,sn,i,out_fname,args.gap_open,args.gap_extension,args.matrix,chunk_fname,args.subject,args.dictionary))

