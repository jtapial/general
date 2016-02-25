#!/usr/bin/env python
import os
import argparse
from Bio import SearchIO

parser = argparse.ArgumentParser(description="This script takes a .psl file from BLAT alignments, and returns a .tab file with the coordinates of each of the aligned segments in the target database (e.g. exon coordinates, in alignments of CDS vs whole-genome). Coordinates are in the format 'chr[chromosome_number]:[exon_start]-[exon_end]:[strand]'. The smallest coordinate is always the start, and the greatest coordinate is always the end")
parser.add_argument("in_path",help="Path to the input .psl file")
parser.add_argumnt("out_path",help="Path to the output .tab file. Directories will be created as needed")
args = parser.parse_args()


assert os.path.isfile(args.in_path), "Path to input file cannot be found. Please enter a valid path"

out_folder = os.path.dirname(args.out_path)
if not os.path.isdir(out_folder):
	os.system("mkdir -p {0}".format(out_folder))


exon_dict = {}
strand_dict = {1:"+",-1:"-"}


with open(args.in_path) as in_file:
	qr_gen = SearchIO.parse(in_file,'blat-psl')
	for qr in qr_gen:
		hsps = sorted(qr.hsps,key=lambda a: a.score,reverse=True)
		best_hsp = hsps[0]

		frags = sorted(best_hsp.fragments,key=lambda b: b.query_range[0]) #This solves exon ordering for negative strand genes. Smallest coordinate is always exon start, greatest coordinate is always exon end.

		for i in frags:
			qstart = i.query_start + 1 #Both BLAT and SearchIO use 0-based, half-open coords
			qend = i.query_end

			chr = i.hit_id
			s_start = i.hit_start + 1
			s_end = i.hit_end
			s_strand = strand_dict[i.query_strand]

			if i.query_id not in exon_dict:
				exon_dict[i.query_id] = []

			exon_dict[i.query_id].append("{0}:{1}-{2}:{3}".format(chr,s_start,s_end,s_strand))

with open(args.out_path,"w") as out_file:
	for i,j in exon_dict.iteritems():
		for k,exon in enumerate(j):
			out_list = ["{0}_{1}".format(i,k+1), exon]
			out_file.write("\t".join(out_list) + "\n")



