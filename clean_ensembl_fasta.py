#!/usr/bin/env python

import os

db = os.environ["DB"]

with open(os.path.join(db,"ensembl_75_hsa_proteins_clean.fasta"),"w") as out_file, open(os.path.join(db,"blast_db/ensembl_75_prot/ensembl_75_hsa_proteins.fasta")) as in_file:
		fasta_dict = {}
		for line in in_file:
			line = line.rstrip()
			if line.startswith(">"):
				header = line.lstrip(">")
				fasta_dict[header] = ""
			else:
				if not line.startswith("Sequence unavailable"):
					fasta_dict[header] = fasta_dict[header] + line



	for k,v in fasta_dict.iteritems():
		if k:
			out_file.write(">{0}\n{1}\n".format(k,v))