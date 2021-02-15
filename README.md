# Make-My-Threads

### Table of Contents
- ***[Introduction](#introduction)***
- ***[Quick Start](#quick-start)***
- ***[Usage](#usage)***
- ***[Arguments](#arguments)***
- ***[Author](#author)***

### Introduction
You have probably come across several tools that work well for you, but are unfortunately single-threaded, and so they take a long time to finish. You may have wished the developer would someday implement multi-concurrent threads.

Well now, you need not wish anymore.

**'Make-My-Threads' is a simple tool that spins up a specified number of concurrent threads and have them execute any specifed command; and supports dynamic arguments (from input-files) as well.**

##### Here's an example
Let's say a tool called 'slow-tool' needs 2 arguments, one of them is an alphabet, the other is a number, and you invoke it like:

```
./slow-tool a 1
```
And you have several argument sets to run (say, a-z, and for each one of them, corresponding 1-9, like 'a 2', 'a 3',...), but **writing a simple bash automation script would still execute the tool slowly**, since the commands would run one-by-one. **Make-My-Threads can solve this...**

### Quick Start
For the above example, you'd probably use Make-My-Threads as:
```
./make_my_threads.py --threads 50 --command "./slow-tool ARG1 ARG2" --mode clusterbomb -f alphabets.txt:ARG1 -f numbers.txt:ARG2
```
Where 'alphabets.txt' and 'numbers.txt' provide the first and second arguments to your chosen command *(Prepare these input text files first)*, and 'ARG1' and 'ARG2' are placeholders for these arguments. **You can use any arbitrary number of dynamic arguments.**

### Usage
There are **3 modes** in which 'Make-My-Threads' can work:
- **Clusterbomb**: *Uses every permutation of provided arguments, say 1st-1st,1st-2nd,...*
- **Pitchfork**: *Uses only corresponding arguments, say 1st-1st arg, 2nd-2nd,...*
- **Repeat**: *Repeats the same static command for specified number of times*

**Clusterbomb and Pitchfork** mode require input files from where to read each set of dynamic command arguments. **You can use any arbitrary number of dynamic arguments (and corresponding input-files)** Male sure to use proper placeholders that do not occur anywhere else in the command.

**Repeat** mode only works with static commands, i.e, you cannot use placeholders to have them replaced by inputs from a file.

Read the arguments needed, below.

### Arguments
```
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        Maximum number of concurrent threads to start
  -c COMMAND, --command COMMAND
                        Command to execute, with appropriate PLACEHOLDER[S] in
                        place of dynamic arguments
  -m {clusterbomb,pitchfork,repeat}, --mode {clusterbomb,pitchfork,repeat}
                        Clusterbomb for every single permutation of dynamic
                        arguments from each input-file; Pitchfork for only
                        corresponding dynamic arguments from input-file
                        (1st-1st,2nd-2nd,and so on); repeat for executing the
                        same static command (i.e, without dynamic args from
                        input-file) for chosen number of times; Except for
                        'repeat', all the other 2 require input-files with
                        distinct PLACEHOLDERS
  -f FILE, --file FILE  Input file from where to take arguments dynamically;
                        can be used multiple times; can be used only with
                        "pitchfork" or "clusterbomb" mode; Format: "-f
                        /path/to/file.txt:PLACEHOLDER"
  -r REPEAT, --repeat REPEAT
                        Number of times to repeat the supplied command; can be
                        used only with "repeat" mode.
  -q, --quiet           Suppress outputs from the commands and show only the
                        commands executed; default: false
```

### Author
*CaptainWoof*
**Twitter: [@realCaptainWoof](https://www.twitter.com/realCaptainWoof)**

