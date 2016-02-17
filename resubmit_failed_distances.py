#!/usr/bin/env python

import argparse
import os
import re

parser = argparse.ArgumentParser(description="This script takes a file with the names of log files of failed distance computation jobs, and resubmits them with the requirements at the bottom of the script, via submitjob.py")
parser.add_argument("in_path",help="Path to the file with the failed jobs log filenames")

args = parser.parse_args()

jobline_regex = re.compile("###Job line: qsub -j y -q (.*) -N (.*) -b y -o (.*) -l h_rt=(.*) -M (.*) -m (.*) (.*) (.*) (.*)$")

original_queue_dict = {"short":"short-sl65",
				"long":"long-sl65",
				"high_mem":"mem_512",
				"low_mem":"mem_256"}

reverse_queue_dict = {b:a for a,b in original_queue_dict.items()}


with open(args.in_path) as failed_jobs_file:
	for line in failed_jobs_file.readlines():
		job_log = line.strip().split(":")[0]
		with open(os.path.abspath(job_log)) as job_file:
			for line in job_file.readlines():
				if jobline_regex.match(line):
					queue, job_name, log_dir, job_time, email_address, email_criteria, script, in_path, out_path = jobline_regex.match(line).groups()

					queue = reverse_queue_dict[queue]

					#INSERT NEW CONDITIONS HERE
					#--------------------------
					#queue = 
					#(queue nickname, not real)

					#job_name = 
					#log_dir = 
					job_time = "180:00:00"
					#email_address = 
					#email_criteria =
					#script = 
					#in_path = 
					#out_path =

					cline = "submitjob.py -n {0} -q {1} -l h_rt={2} -b y {3} {4} {5}".format(job_name,queue,job_time,script,in_path,out_path)
					os.system(cline)
					break

print "Finished"
