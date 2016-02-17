#!/usr/bin/env python

import os
import sys
import re
import argparse

jobs = os.environ["JOBS"]

parser = argparse.ArgumentParser(description="This script takes two numbers A and B, and a general filename C without extension. Then, it checks in jobs/outputs the exit status of all the job logs {C}{A}.* to {C}{B}.*.\n\nThe script returns the filename with the greatest job ID for every index D where no job {C}{D}.* has succeeded, so that these files can be used with \"scripts/resubmit_failed_distances.py\"",formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("fn",help="Generic filename")
parser.add_argument("min_no",help="Minimum job index",type=int)
parser.add_argument("max_no",help="Maximum job index",type=int)
parser.add_argument("-out",help="Path to output file. Default is STDOUT")
args = parser.parse_args()

exit_regex = re.compile("### Exit Status: (\d*)")
log_fn_regex = re.compile("{0}(\d*).o(\d*)".format(args.fn))

if args.out:
	out_file = open(args.out, "w")
else:
	out_file = sys.stdout

for i in range(args.min_no,args.max_no + 1):
	status = []
	job_ids = []
	for f in [a for a in os.listdir(jobs) if a.startswith("{0}{1}.".format(args.fn,i))]:
		if log_fn_regex.match(f):
			jid = log_fn_regex.match(f).group(2)
			with open(os.path.join(jobs,f)) as log_file:
				for line in log_file.readlines():
					if exit_regex.match(line):
						this_status= exit_regex.match(line).group(1)
						status.append(int(this_status))
						job_ids.append(int(jid))

	if 0 not in status:
		out_file.write("{0}{1}.o{2}\n".format(args.fn,i,max(job_ids)))

if args.out:
	out_file.close()


					



