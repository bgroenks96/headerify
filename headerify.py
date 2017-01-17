import os
import sys
import argparse
from headerify_processors import *

parser = argparse.ArgumentParser(description="Generate and prepend header text to files.")
parser.add_argument("inputfile", help="input file to read header text from")
parser.add_argument("-o", "--output", default="", help="oputput file to prepend header to; use -r to recurse over a directory")
parser.add_argument("-r", "--recurse", action="store_true", help="recurse over all subdirectories in output (must be a directory)")
parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose stdout logging")

args = parser.parse_args();

def printv(msg):
  if args.verbose:
    print(msg)

inputstr = ""
with open(args.inputfile, 'r') as inputfile:
  inputstr = inputfile.read()
    
processor = CStyleProcessor()
print(args.output)
printv(processor.headerify(inputstr))

def prepend(f, headerstr):
  pass


