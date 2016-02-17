#!/usr/bin/env python

import os
import subprocess

test = os.environ["TEST"]
db = os.environ["DB"]
data = os.environ["DATA"]


with open(os.path.join(db,"blast_db/ensembl_75_fake71_merged/ensembl_75_fake71_merged.fasta")) as ensembl_file:
	ensembl_fasta_dict = {}
	for entry in ensembl_file.read().rstrip().split("\n>"):
		entry_lines = [i.rstrip() for i in entry.split("\n")]
		if entry_lines[1] != "Sequence unavailable":
			header = entry_lines[0].split()[0].lstrip(">")
			seq = "".join(entry_lines[1:])
			ensembl_fasta_dict[header] = seq


with open(os.path.join(db, "blast_db/uniprot_human_isoforms/uniprot_human_splicevar.fasta")) as uniprot_file:
	uniprot_fasta_dict = {}
	for entry in uniprot_file.read().split("\n>"):
		entry_lines = [i.rstrip() for i in entry.split("\n")]
		header = entry_lines[0].split()[0].lstrip(">")
		seq = "".join(entry_lines[1:])
		uniprot_fasta_dict[header] = seq

with open(os.path.join(data,"ensembl_to_uniprot.tab")) as mapping_file:
	mapping_list = [tuple(i.strip().split("\t")) for i in mapping_file.readlines()]



with open(os.path.join(test,"nw_ensembl_uniprot.ali"),"w") as out_file:
	for ensembl_id, uniprot_id in mapping_list:
		if ensembl_id in ensembl_fasta_dict and uniprot_id in uniprot_fasta_dict:
			ensembl_seq = ensembl_fasta_dict[ensembl_id]
			uniprot_seq = uniprot_fasta_dict[uniprot_id]
			sp_args = ["needle",
						"asis::{0}".format(str(ensembl_seq)),
						"-sprotein1",
						"-sid1",
						ensembl_id,
						"-bseq",
						"asis::{0}".format(str(uniprot_seq)),
						"-sprotein2",
						"-sid2",
						uniprot_id,
						"-stdout",
						"-gapopen",
						"10",
						"-gapextend",
						"0.5",
						"-datafile",
						"EBLOSUM62",
						"-auto",
						"-aformat",
						"fasta"]
			#print " ".join(sp_args)

			ali_output = subprocess.check_output(sp_args)		
			out_file.write(ali_output + "\n")


print "==============ALIGNMENT COMPLETE==============="
print "Full results in: '$TEST/test/nw_ensembl_uniprot.ali'"




