#!/usr/bin/env python

"""This script takes a multi-FASTA file, splits it in chunks, and then sends
an individual job to BLAST it against a target database.
The target must be individually formatted"""

import argparse
import os
import shlex, subprocess
import StringIO

#Required args
parser = argparse.ArgumentParser(description="Takes a multi-FASTA file and BLAST it in separate jobs vs. a target DB") 

parser.add_argument('input_file', help="query multi-FASTA file")
parser.add_argument('target_db', help="path to the target database. Must be already formatted (see 'makeblastdb -help')")
parser.add_argument('output_path', help="destination folder for the output (split input files and output alignment file)",
					default=".")

#Optional args to the script
parser.add_argument('-blast_type',
					default="blastp",
					choices=['blastp','blastn','blastx','tblastx','tblastn','psiblast'],
					help="BLAST flavour to be used"
					)
parser.add_argument('-chunk_size', help="maximum number of seqs in each chunk",
					default="100",type=int)
parser.add_argument('-threads', help="number of threads for each BLAST job",
					default=4, type=int)
parser.add_argument('-job',help="include this flag to submit the jobs to a cluster scheduler. Otherwise they will be sent as subprocesses to the current shell", action='store_true')

#Arguments to BLAST
parser.add_argument('blast_arguments',
					help="additional arguments to BLAST (See '<BLAST_FLAVOUR> -help for a list of available options",
					nargs=argparse.REMAINDER)



args = parser.parse_args()

#Filter entries
try:
	with open(args.input_file,"r") as in_file:
		entry_list = in_file.read().split('\n>')
except IOError:
	print "ERROR: File not found"
	raise

if not os.path.isdir(args.output_path):
	os.system("mkdir -p {0}".format(args.output_path))
pre_filter_length = len(entry_list)

entries_to_filter = []

for counter in range(0,len(entry_list)):
	if entry_list[counter].strip() == None:
		entries_to_filter.append(counter)

	else:
		if not entry_list[counter].strip().startswith(">"):
			entry_list[counter] = ">" + entry_list[counter]
		
		entry_list[counter] = '|'.join(entry_list[counter].split('\n')[0].split("|")[:2]) + '\n' + ''.join(entry_list[counter].split('\n')[1:])

		if entry_list[counter].split("\n")[-1].startswith("Sequence unavailable"):
			entries_to_filter.append(counter)

for element in sorted(entries_to_filter,reverse=True):
	entry_list.pop(element)

post_filter_length = len(entry_list)
#Filtering report
print "Detected", pre_filter_length, "entries"
print "After filtering:", post_filter_length

#Create directory if not present
if not os.path.exists(args.output_path):
	os.system("mkdir -p {0}".format(args.output_path))

#Split into chunk files
chunks = [entry_list[offset:min(offset+args.chunk_size,len(entry_list))] for offset in range(0,post_filter_length,args.chunk_size)]

chunk_paths = []

for chunk_index,chunk in enumerate(chunks):
	chunk_filename = os.path.split(args.input_file)[1] + "-" + str(chunk_index)
	chunk_path = os.path.join(args.output_path,chunk_filename)

	with open(chunk_path,"w") as chunk_file:
		chunk_file.write('\n'.join(chunk))

	chunk_paths.append(chunk_path)

#Split report:
print "Input has been split into", len(chunks), "files"

default_filename = os.path.split(chunk_path[:chunk_path.rfind("-")])[-1] + "-X"
print "Filename: ", default_filename


if args.threads != 1:
	threads_string = " -pe smp {0}".format(args.threads + 1)
else:
	threads_string = ""

for chunk_index,chunk_path in enumerate(chunk_paths):
	output_path = os.path.join(args.output_path,default_filename[:default_filename.rfind("-")]+"-"+os.path.split(args.target_db)[-1]+"-"+str(chunk_index))

	bash_cline = "{0} -query {1} -db {2} -out {3} -num_threads {4} {5}".format(args.blast_type,chunk_path,args.target_db,output_path,args.threads,' '.join(args.blast_arguments))

	output_filename = os.path.split(output_path)[-1]

	if args.job == True:
		submitjob_line = "submitjob.py -b y -q short -n {0}{2} \"$(echo \"{1}\")\"".format(args.blast_type,bash_cline,threads_string)
		
		print bash_cline + '\n'
		print submitjob_line + '\n'
		os.system(submitjob_line)

	else:
		print bash_cline
		subprocess.call(shlex.split(bash_cline))
		









