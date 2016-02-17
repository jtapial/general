#!/usr/bin/env python

import os
import argparse
import math

parser = argparse.ArgumentParser(description="Submitjob script for the 'pdb_seqto3d_mapping_2.py' script. This takes a set of PDB files and a FASTA file with their sequences masked for 3D gaps, and creates a text string describind the correspondence between the FASTA residues and the PDB residues")

g = parser.add_mutually_exclusive_group()
g.add_argument("-chunks",help="Number of jobs to be submitted",type=int)
g.add_argument("-chunk_size",help="Maximum chunk size",type=int)

parser.add_argument("pdb_folder", help="Path to the download of the PDB")
parser.add_argument("fasta_path",help="Path to the complete FASTA file with the sequences")
parser.add_argument("chunk_path",help="Generic path to the chunk file with the FASTA sequences in each job. The format will be <your_input>_<chunk_no>.fasta")
parser.add_argument("out_path",help="Generic path to the output file")

args = parser.parse_args()

assert os.path.isdir(args.pdb_folder), "Invalid path to PDB folder. Please provide a valid path"

assert os.path.isfile(args.fasta_path), "Invalid path to input FASTA file. Please provide a valid path"

out_folder,out_gen_fname = os.path.split(args.out_path)
if out_folder and not os.path.isdir(out_folder):
	os.system("mkdir -p {0}".format(out_folder))

chunk_folder,chunk_gen_fname = os.path.split(args.chunk_path)
if chunk_folder and not os.path.isdir(chunk_folder):
	os.system("mkdir -p {0}".format(chunk_folder))

with open(args.fasta_path) as in_fasta_file:
	splitfasta = [">{0}".format(entry.rstrip("\n")) if not entry.startswith(">") else entry for entry in in_fasta_file.read().split("\n>")]

if args.chunks:
	chunk_size = chunk_size = int(math.ceil(len(splitfasta)/float(args.chunks)))
	in_chunks = [sorted(splitfasta)[offset:min(offset + chunk_size,len(splitfasta))] for offset in range(0,len(splitfasta),chunk_size)]

elif args.chunk_size:
	in_chunks = [sorted(splitfasta)[offset:min(offset + args.chunk_size,len(splitfasta))] for offset in range(0,len(splitfasta),args.chunk_size)]

for number,chunk in enumerate(in_chunks):
	chunk_path = os.path.join(chunk_folder,"{0}_{1}.fasta".format(os.path.splitext(chunk_gen_fname)[0],number))
	with open(chunk_path,"w") as chunk_file:
		chunk_file.write("\n".join(chunk))

for number,chunk in enumerate(in_chunks):
	chunk_path = os.path.join(chunk_folder,"{0}_{1}.fasta".format(os.path.splitext(chunk_gen_fname)[0],number))
	out_path = os.path.join(out_folder,"{0}_{1}.tab".format(os.path.splitext(out_gen_fname)[0],number))

	os.system("submitjob.py -q long -l h_rt=10:00:00 -l virtual_free=10G -n pdb_seqto3d_mapping_{0} -b y $SRC/vastdb_maps/mapping_files_creation/pdb_seqto3D_mapping_2.py {1} {2} {3}".format(number,args.pdb_folder,chunk_path,out_path))


