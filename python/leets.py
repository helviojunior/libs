#!/usr/bin/python
# -*- coding: utf-8 -*-
 
'''
Author : Helvio Junior (M4v3r1cK)
Date : 2018-10-23
https://github.com/helviojunior/libs/blob/master/python/leets.py
'''

import os, re, sys, getopt, argparse

parser = argparse.ArgumentParser()
parser.add_argument('wordlist_file', help='Input file with word list to leet')
parser.add_argument('-min', '--min-lenght', default=1, type=int, help='Minumin word lenght')
parser.add_argument('-max', '--max-lenght', default=32, type=int, help='Maximum word lenght.')
parser.add_argument('-p', '--padding', action='store_true', default=False, help='Add padding to fill string to match minimun leght')
#parser.add_argument('-h', '--help', help='Show this help message and exit')
args = parser.parse_args()

min_size = int(args.min_lenght)
max_size = int(args.max_lenght)
padding = args.padding

if min_size < 1:
	min_size = 1


d = {	
	"a":"aA@49",
	"b":"bB8",
	"c":"cC",
	"d":"dD",
	"e":"eE3",
	"f":"fF",
	"g":"gG96",
	"h":"hH#",
	"i":"iI!1",
	"j":"jJ",
	"k":"kK",
	"l":"lL!1",
	"m":"mM",
	"n":"nN",
	"o":"oO0",
	"p":"pP",
	"q":"qQ",
	"r":"rR",
	"s":"sS5$",
	"t":"tT7+",
	"u":"uU",
	"v":"vV",
	"w":"wW",
	"x":"xX",
	"y":"yY",
	"z":"zZ2",
	"0":"0",
	"1":"1",
	"2":"2",
	"3":"3",
	"4":"4",
	"5":"5",
	"6":"6",
	"7":"7",
	"8":"8",
	"9":"9"
	}
u = []
prt = True

def calc_uniq():
	for c in d:
		for i, s in enumerate(d.get(c)):
			if s not in u:
				u.append(s)

def proc2(word, index):
	c = word[index:index+1]
	if c in d:
		for i, s in enumerate(d.get(c)):
			if (index == len(word) - 1):
				p = "%s%s" % (word[0:index], s)
				if len(p) < min_size and padding:
					add_padding(p)
				else:
					print p
			else:
				p = "%s%s%s" % (word[0:index], s, word[index+1:])
				proc2(p, index+1)

def process(l):
	print l
	proc2(l,0)

def create_wl(l,d):
  if d<1:
    return
  for c in l:
    if d==1:
      yield c
    else:
      for k in create_wl(l,d-1):
        yield c+k

def add_padding(word):
	s1 = min_size - len(word)
	if s1 > 0:
		for c in create_wl(u,s1):
			print "%s%s" % (word, c)
			print "%s%s" % (c, word)

def main():
	if not os.path.isfile(args.wordlist_file):
		print "Wordlist file not found '%s'" % args.wordlist_file
		sys	.exit(1)

	calc_uniq()
	with open(args.wordlist_file) as f:
		try:
			global prt
			for line in f:
				l1 = line.rstrip().lstrip()
				if len(l1) > max_size:
					pass
				elif len(l1) < min_size and padding:
					process(l1.lower())
				elif len(l1) >= min_size:
					process(l1.lower())
		except KeyboardInterrupt:
			sys.stdout.flush()
			sys	.exit(0)


if __name__ == "__main__":
	main()	
