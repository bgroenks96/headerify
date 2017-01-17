import argparse
import os
import sys
import fnmatch
from headerify_processors import *

parser = argparse.ArgumentParser(description="Generate and prepend header text to files.")
parser.add_argument("inputfile", help="input file to read header text from")
parser.add_argument("-o", "--output", default="", help="oputput file to prepend header to; use -r to recurse over a directory")
parser.add_argument("-r", "--recurse", action="store_true", help="recurse over all subdirectories in output (must be a directory)")
parser.add_argument("-i", "--include", default='**/*', help="inclusion pattern for file matching")
parser.add_argument("-e", "--exclude", default='', help="exclusion pattern for file matching")
parser.add_argument("-f", "--force", action="store_true", help="replace existing file header, if one already exists")
parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose stdout logging")

args = parser.parse_args()

def printv(msg):
  if args.verbose:
    print(msg)

def prepend(f, headerstr):
  with open(f, 'r+') as outfile:
    datain = outfile.read()
    if datain.startswith(header) and not args.force:
      printv("%s already has header; skipping" % f)
      return
    elif datain.startswith(header):
      printv("%s already has header; replacing")
      datain = datain.replace(header, '')
    dataout = header + "\n\n" + datain
    outfile.seek(0)
    outfile.write(dataout)

inputstr = ""
with open(args.inputfile, 'r') as inputfile:
  inputstr = inputfile.read()
    
processor = CStyleProcessor()
header = processor.headerify(inputstr)

if not any(args.output):
  print(header)
  exit()

printv(header)

if not args.recurse:
  printv("Prepending target file %s" % args.output)
  prepend(os.path.join(os.getcwd(), args.output), header)
  exit()

printv("Recursing %s..." % args.output)
count = 0
for root,dirs,files in os.walk(os.path.join(os.getcwd(), args.output)):
  printv("Found %d files (%d sub-directories)" % (len(files), len(dirs)))
  matches = [f for f in fnmatch.filter(files, args.include) if f not in fnmatch.filter(files, args.exclude)]
  for f in matches:
    path = os.path.join(root, f)
    printv("Matched %s ... prepending header" % path)
    prepend(path, header)
    count += 1

if count > 0:
  printv("Finished! (%d files processed)" % count)
else:
  printv("Nothing to do.")

