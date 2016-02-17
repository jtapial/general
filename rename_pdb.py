#!/usr/bin/python

#This script renames all files in a gunzipped raw download of the PDB, to their right names

#Original name: "pdbXXXX.ent"
#Desired name: "XXXX.pdb"

import argparse
import os
import re

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description="This script renames all files in a gunzipped raw download of the PDB, to their right names.\nOriginal name: pdbXXXX.ent\nDesired name: XXXX.pdb")
parser.add_argument('path_to_pdb',help='path to the top directory where the PDB copy is downloaded')
args=parser.parse_args()

path_to_pdb = args.path_to_pdb

filename_regex = re.compile('pdb(\w{4})\.ent')

print "Renaming 'pdbXXXX.ent' to 'XXXX.pdb'..."
for root,dirs,files in os.walk(path_to_pdb):
	for filename in files:
		if filename_regex.match(filename):
			pdb_id = filename_regex.match(filename).group(1)
		 	os.rename(os.path.join(root,filename),os.path.join(root,pdb_id+".pdb"))
                 
print "Renaming finished"
