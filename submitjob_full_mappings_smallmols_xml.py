#!/usr/bin/env python

import argparse
import os

#ARG HANDLING
parser = argparse.ArgumentParser(description="This script is an interface to parallelize full_mappings_smallmols.py")
parser.add_argument("-start_level",help="Starting biological information level (exon,prot_seq,prot_3d)",choices=["exon","prot_seq","prot_3d"])
parser.add_argument("-end_level",help="Target biological information level (exon,prot_seq,prot_3d)",choices=["exon","prot_seq","prot_3d"])
parser.add_argument("-in_path",help="Input with the IDs that will be mapped (VASTDB,ENSEMBL residues, PDB residues")
parser.add_argument("-out_path",help="Path to the output folder for chunk files and partial outputs")
parser.add_argument("-chunk_size",help="Number of chunks that will be made",type=int)
args = parser.parse_args()

def parse_residues_tochunks(in_path):
	#input: pdb_id	model	chain	res_name	res_no	i_code	target_chain	target_resname	target_resno	target_icode\n
	res_dict = {}
	with open(in_path,"r") as in_file:
		file_list = in_file.readlines()

	#output: {(pdb_id,model,chain,res_name,res_no,i_code):[(pdb_id,pdb_model,target_chain,target_rename,target_resno,target_icode)]}
	# print res_dict
	return file_list


if args.out_path and not os.path.isdir(args.out_path):
	os.system("mkdir -p {0}".format(args.out_path))

my_list = parse_residues_tochunks(args.in_path)

chunk_list = [my_list[a:min(a+args.chunk_size,len(my_list))] for a in range(0,len(my_list),args.chunk_size)]

for idx,chunk in enumerate(chunk_list):
	chunk_path = os.path.join(args.out_path,"chunk_input_{0}.tab".format(idx))
	with open(chunk_path,"w") as chunk_file:
		for i in chunk:
			chunk_file.write(i)

for idx,chunk in enumerate(chunk_list):
	chunk_path = os.path.join(args.out_path,"chunk_input_{0}.tab".format(idx))
	out_path = os.path.join(args.out_path,"output_file_{0}.tab".format(idx))
	os.system("submitjob.py -q long -n fullmaps_smallmols_revised_xml_5_{4} -l virtual_free=30G h_rt=24:00:00 -b y $SRC/vastdb_maps/parsing_pipeline/full_mappings_smallmols_blastxml.py -start_level {0} -end_level {1} -in_path {2} -out_path {3}".format(args.start_level,args.end_level,chunk_path,out_path,idx))

