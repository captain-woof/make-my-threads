#!/usr/bin/python3

from threading import Thread
from argparse import ArgumentParser
from queue import Queue, Empty
import subprocess

# Parse args first
parser = ArgumentParser(description="A simple tool that spins up a specified number of concurrent threads and have them execute any specifed command; supports dynamic arguments (from input-files) as well.",epilog="Author: @realCaptainWoof")
parser.add_argument('-t','--threads',required=True,type=int,help="Maximum number of concurrent threads to start",action='store')
parser.add_argument('-c','--command',required=True,type=str,help="Command to execute, with appropriate PLACEHOLDER[S] in place of dynamic arguments",action='store')
parser.add_argument('-m','--mode',required=True,type=str,choices=['clusterbomb','pitchfork','repeat'],help="Clusterbomb for every single permutation of dynamic arguments from each input-file; Pitchfork for only corresponding dynamic arguments from input-file (1st-1st,2nd-2nd,and so on); repeat for executing the same static command (i.e, without dynamic args from input-file) for chosen number of times; Except for 'repeat', all the other 2 require input-files with distinct PLACEHOLDERS",action='store')
sub = parser.add_mutually_exclusive_group(required=True)
sub.add_argument('-f','--file',type=str,action='append',help='Input file from where to take arguments dynamically; can be used multiple times; can be used only with "pitchfork" or "clusterbomb" mode; Format: "-f /path/to/file.txt:PLACEHOLDER"')
sub.add_argument('-r','--repeat',type=int,action='store',help='Number of times to repeat the supplied command; can be used only with "repeat" mode.')
parser.add_argument('-q','--quiet',action='store_true',required=False,default=False,help="Suppress outputs from the commands and show only the commands executed; default: false")
args = parser.parse_args()

max_threads = args.threads
command = args.command
files = args.file
repeat = args.repeat
mode = args.mode
quiet = args.quiet

# Initialize
def permute_lists(base,new):
	master = []
	for each_new in new:
		for each_base in base:
			each_base_copy = each_base.copy()
			each_base_copy.append(each_new)
			master.append(each_base_copy)
	return master

class InputFile:
	def __init__(self,file_path,placeholder):
		self.placeholder = placeholder		
		with open(file_path,'r') as file_pointer:
			self.all_lines = [line.strip() for line in file_pointer.readlines()]	
	
	def next_line(self):
		try:
			return self.all_lines.pop(0)
		except IndexError:
			return ''
if mode != 'repeat':
	input_files = []
	for each_file in files: # each_file = "path/to/file.txt:PLACEHOLDER"
		input_file = InputFile(each_file.split(":")[0],each_file.split(":")[1])
		input_files.append(input_file)

	for input_file in input_files:
		if input_file.placeholder not in command:
			print("Placeholder '{}' is not in supplied command".format(input_file.placeholder))
			exit(0)

queue = Queue()
if mode == 'repeat': # 'repeat' mode
	for i in range(0,repeat):
		queue.put(command)
elif mode == 'pitchfork': # 'pitchfork' mode	
	for i in range(0,len(input_files[0].all_lines)):
		cmd = command
		for input_file in input_files:
			nl = input_file.next_line()
			if nl != '':
				cmd = cmd.replace(input_file.placeholder,nl)
			else:
				cmd = ''
		if cmd != '':
			queue.put(cmd)
elif mode == 'clusterbomb': # 'clusterbomb' mode
	args = []
	for arg in input_files[0].all_lines:
		args.append([arg])

	for i in range(1,len(input_files)):
		args = permute_lists(args,input_files[i].all_lines)

	for each in args:
		cmd = command
		for i in range(0,len(each)):
			cmd = cmd.replace(input_files[i].placeholder,each[i])
		queue.put(cmd)


# EXECUTION BEGINS
def thread_func():
	output = subprocess.PIPE if quiet else None
	while True:
		try:
			cmd = queue.get(block=True,timeout=1)
		except Empty:
			return		
		print(cmd)
		p = subprocess.Popen(cmd,shell=True,stdout=output,stderr=output)
		while p.poll() is None:
			continue
threads = []
print("[+] Starting {} threads".format(max_threads))
for i in range(0,max_threads):
	thread = Thread(target=thread_func)
	threads.append(thread)
	thread.start()

for thread in threads:
	thread.join()

print("\n[+] All tasks finished!")
