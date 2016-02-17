#!/usr/bin/env python

import argparse
import os
import subprocess
import re
import shlex

user_address = os.environ["EMAIL"]

user_email="-M " + user_address + " -m abe"

parser = argparse.ArgumentParser(description="SUBMITJOB SCRIPT\n---------------------------------------\nWrapper for the qsub command for SGE systems.\nSubmits a job to the scheduler, with the desired parameters.",
								epilog="To check queue lists, type \"qstat -g c\"\nTo check queue parameters, type \"qconf -sq <queue_name>\"",
								formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("-q","--queue",
					choices=["short","long","high_mem","low_mem"],
					default="short",
					help="queue to submit the job to (short-sl65,long-sl65,mem_512,mem_256)")

parser.add_argument("-n","--name",
					required=True,
					help="name of the job")

parser.add_argument("-o","--output",
					default=os.environ["JOBS"],
					help="folder for the log file (default: '$JOBS')")

parser.add_argument("-pe","--parallel",
					nargs=2,
					help="Parallel environment to use (\"smp\", \"mpich\",\"ompi\", and number of cores)",
					metavar=("MPE_ENV","CORES"))

parser.add_argument("-b","--binary",
					choices=["y","n"],
					default="n",
					help="Submit job as binary")

parser.add_argument("-l","--resource",
					nargs='*',
					#choices=["memory","time","disk"],
					help="Specific resources and values: memory (**G), time (hh:mm:ss), disk (**G)",
					dest="resources",
					metavar=("RESOURCE=VALUE"))

parser.add_argument("-m","--mail","--email",
					default="bea",
					help="Send emails about the job. Use \'b\' for beginning, \'e\' for end, \'a\' for aborted",
					dest="mail",
					action="store_true")

parser.add_argument("-cwd",
					help="Execute job from current directory instead of home",
					action="store_true")

parser.add_argument("script",
					nargs=argparse.REMAINDER,
					help="Bash script containing the job")

args = parser.parse_args()
print args

queue_dict = {"short":"short-sl65",
				"long":"long-sl65",
				"high_mem":"mem_512",
				"low_mem":"mem_256"}

if args.resources != None:
	resources_string = ''.join([" -l {0}".format(i) for i in args.resources])
else:
	resources_string = ''

if args.cwd:
	cwd_string = " -cwd"
else:
	cwd_string = ""

if args.parallel:
	parallel_string = " -pe " + ' '.join(args.parallel)
else:
	parallel_string = ''

if args.mail:
	email_string = ' ' + user_email
else:
	email_string = ''


cli = "qsub -j y -q {0} -N {1} -b {2} -o {3}{4}{5}{6}{7} {8}".format(queue_dict[args.queue],args.name,args.binary,args.output,resources_string,parallel_string,email_string,cwd_string,' '.join(args.script))

cli_args = shlex.split(cli)

print cli
confirmation = subprocess.check_output(cli_args)
print confirmation

jobline_regex = re.compile(r"^Your job (\d+) \(\"([^\s]*)\"\) has been submitted")

job_id = str(jobline_regex.match(confirmation).group(1))

with open(os.path.join(os.path.abspath(args.output),args.name+".o"+ job_id),"w") as out_file:
	out_file.write("###Command: " + ''.join(args.script) + '\n')
	out_file.write("###Job line: " + cli + '\n')
	out_file.write("###Confirmation: " + confirmation + '\n')







