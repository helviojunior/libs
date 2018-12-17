#!/usr/bin/python
# -*- coding: utf-8 -*-
 
'''
Author : Helvio Junior (M4v3r1cK)
Date : 2018-10-28
https://github.com/helviojunior/libs/blob/master/python/wordlistpadding.py
'''

import os, re, sys, getopt, argparse

parser = argparse.ArgumentParser()
parser.add_argument('wordlist_file', help='Input file with word list')
parser.add_argument('padding_file', help='Input file with word list to be inserted as padding')
args = parser.parse_args()

def main():
	if not os.path.isfile(args.wordlist_file):
		print "Wordlist file not found '%s'" % args.wordlist_file
		sys	.exit(1)

	if not os.path.isfile(args.padding_file):
		print "Wordlist padding file not found '%s'" % args.padding_file
		sys	.exit(1)

	with open(args.wordlist_file) as wf:
		try:
			for wordlist_line in wf:
				wll = wordlist_line.rstrip().lstrip()
				print wll
				if len(wll) > 0:
					with open(args.padding_file) as pf:
						for padding_line in pf:
							pl = padding_line.rstrip().lstrip()
							if len(pl) > 0:
								print "%s%s" % (wll, pl)
								print "%s%s" % (pl, wll)
		except KeyboardInterrupt:
			sys.stdout.flush()
			sys	.exit(0)


if __name__ == "__main__":
	main()	
