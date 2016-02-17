#!/usr/bin/env python

import os
import sys
import argparse
import math

parser = argparse.ArgumentParser(description="This is a wrapper to split the content of a PDB folder into chunks, and measure distances from residues in the peptidic chains to every molecule in other chains if the distance is < 50A , using 'drug_interface_extraction_pepvsall_50_biopython.py'")
parser.add_argument("-pdb_dir",help="Path to the PDB raw download")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-chunks", help="number of jobs to be submitted",type=int)
group.add_argument("-chunk_size",help="number of PDBs to be analyzed in each  job",type=int)
parser.add_argument("-out_path",help="Path to the output file and default filename",default=sys.stdout)

args = parser.parse_args()

assert os.path.isdir(args.pdb_dir), "Invalid path to the PDB download. Please provide a valid path"

if args.out_path != sys.stdout:
	out_folder,out_base_fn = os.path.split(args.out_path)
	if not os.path.isdir(out_folder):
		os.system("mkdir -p {0}".format(out_folder))


paths_dict = {}
for root,dirs,files in os.walk(args.pdb_dir):
	for fname in files:
		if fname.endswith(".pdb"):
			paths_dict[fname[:-4]] = os.path.join(root,fname)

if args.chunks:
	chunk_size = chunk_size = int(math.ceil(len(paths_dict.items())/float(args.chunks)))
	in_chunks = [sorted(paths_dict.items())[offset:min(offset + chunk_size,len(paths_dict.items()))] for offset in range(0,len(paths_dict.items()),chunk_size)]

elif args.chunk_size:
	in_chunks = [sorted(paths_dict.items())[offset:min(offset + args.chunk_size,len(paths_dict.items()))] for offset in range(0,len(paths_dict.items()),args.chunk_size)]


for number,chunk in enumerate(in_chunks):
	chunk_path = os.path.join(out_folder,"pdb_chunk_file_{0}.tab".format(number))
	with open(chunk_path,"w") as chunk_file:
		for pdb_id,pdb_path in chunk:
			chunk_file.write('\t'.join([pdb_id,pdb_path]) + '\n')


for number,chunk in enumerate(in_chunks):
	chunk_path = os.path.join(out_folder,"pdb_chunk_file_{0}.tab".format(number))
	out_fn = os.path.splitext(out_base_fn)[0] + "_{0}".format(number) + os.path.splitext(out_base_fn)[1]
	out_path = os.path.join(out_folder,out_fn)

	os.system("submitjob.py -n pdb_extraction_{2} -q long -l h_rt=10:00:00 -b y $SRC/vastdb_maps/mapping_file_creation/drug_interface_extraction_pepvsall_50_biopython.py {0} {1}".format(chunk_path,out_path,number))



