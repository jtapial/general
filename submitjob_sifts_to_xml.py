#!/usr/bin/env python
import argparse
import os
import sys

parser = argparse.ArgumentParser(description="This is the batch job interface for the script \"sifts_xml_to_table.py\"")

parser.add_argument("-chunk_length",help="Number of XML files to be processed in each batch",type=int,default=10000)
parser.add_argument("-time",help="Time to be assigned to each job on the LONG queue, in hours",default=24,type=int)
parser.add_argument("-name",help="Generic job name. The index will be appended to the end")

parser.add_argument("in_path",help="Root folder with the XML files (the script will walk down the sub-directories looking for XML files")
parser.add_argument("chunk_path",help="Path for the txt files with the input for each job. Index will be appended before the extension. Folders will be created as needed")
parser.add_argument("out_path",help="Generic name for the .tab files that will be generated (the index will be appended before the extension) (folders will be created as needed)")


args = parser.parse_args()

assert os.path.isdir(args.in_path), "Invalid input path: {0}".format(args.in_path)

chunk_folder,chunk_fname = os.path.split(args.chunk_path)
chunk_stem,chunk_ext = os.path.splitext(chunk_fname)

if chunk_folder and not os.path.isdir(chunk_folder):
	os.system("mkdir -p {0}".format(chunk_folder))


out_folder,out_fname = os.path.split(args.out_path)
out_stem,out_ext = os.path.splitext(out_fname)

if out_folder and not os.path.isdir(out_folder):
	os.system("mkdir -p {0}".format(out_folder))

xml_paths = []
for root,dirs,files in os.walk(args.in_path):
	for f in files:
		if os.path.splitext(f)[1] == ".xml":
			xml_paths.append(os.path.join(root,f))


chunk_list = [xml_paths[offset:min(offset+args.chunk_length,len(xml_paths))] for offset in range(0,len(xml_paths),args.chunk_length)]

for i,chunk in enumerate(chunk_list):
	job_name = args.name + "_{0}".format(i)
	out_fn = os.path.join(out_folder,"{0}_{1}{2}".format(out_stem,i,out_ext))
	chunk_fn = os.path.join(chunk_folder,"{0}_{1}{2}".format(chunk_stem,i,chunk_ext))
	with open(chunk_fn, "w") as chunk_file:
		t = [a + "\n" for a in chunk]
		chunk_file.write("".join(t))


	os.system("submitjob.py -q long -n {0} -l h_rt={1}:00:00 -b y python ~/scripts/sifts_xml_to_table.py {2} {3}".format(job_name,args.time,chunk_fn,out_fn))






