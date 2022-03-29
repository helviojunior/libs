#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
'''
Author : Helvio Junior (M4v3r1cK)
Date : 2020-11-02
Update : 2022-03-29

Utilization samples:
   python3 build_wordlist.py company > output.txt
   python3 build_wordlist.py company --min-lenght 6 --padding > output.txt

'''

import os, re, sys, getopt, argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('company_name', help='Company Name')
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
    "e":"eE32",
    "f":"fF",
    "g":"gG96",
    "h":"hH#",
    "i":"iI!1",
    "j":"jJ",
    "k":"kK",
    "l":"lL!1",
    "m":"mM",
    "n":"nN",
    "o":"oO04",
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
special = ["@", "#", "!", ".", "-", ",", "$", "%", "*", "+", "/", "\\", "<", ">", "=", "&"]
u = []

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
                    print(p)
                add_common(p)
            else:
                p = "%s%s%s" % (word[0:index], s, word[index+1:])
                proc2(p, index+1)

def process(l):
    print(l)
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
            print("%s%s" % (word, c))
            print("%s%s" % (c, word))

def add_common(word):

    year = datetime.now().year
    y2 = int(str(year)[2:4])

    if min_size <= len(word) + 1 <= max_size:
        for s in special:
            print("%s%s" % (word,s))
            print("%s%s" % (s,word))

    if min_size <= len(word) + 3<= max_size:
        for n in range(0, y2 + 15):
            print("%s%s" % (word, n))
            print("%s%s" % (n, word))
            for s in special:
                print("%s%s%s" % (word, s, n))
                print("%s%s%s" % (word, n, s))
                print("%s%s%s" % (n, s, word))
                print("%s%s%s" % (s, n, word))
                print("%s%s%02d" % (word, s, n))
                print("%s%02d%s" % (word, n, s))
                print("%02d%s%s" % (n, s, word))
                print("%s%02d%s" % (s, n, word))

    if min_size <= len(word) + 5 <= max_size:
        for n in range(year - 5, year + 15):
            print("%s%s" % (word, n))
            print("%s%s" % (n, word))
            for s in special:
                print("%s%s%s" % (word, s, n))
                print("%s%s%s" % (word, n, s))
                print("%s%s%s" % (n, s, word))
                print("%s%s%s" % (s, n, word))
                print("%s%s%04d" % (word, s, n))
                print("%s%04d%s" % (word, n, s))
                print("%04d%s%s" % (n, s, word))
                print("%s%04d%s" % (s, n, word))

def main():
    if args.company_name is None or args.company_name.strip() == "":
        print("Company name not provided '%s'" % args.wordlist_file)
        sys.exit(1)

    if len(args.company_name) < 3:
        print("Company name must have 3 or more characters '%s'" % args.company_name)
        sys.exit(1)

    company_name = args.company_name.strip().lower()

    if len(company_name) > max_size:
        print("Company name greater than defined max lenght '%s'" % args.company_name)
        sys.exit(1)

    calc_uniq()

    try:
        process(company_name)
    except KeyboardInterrupt:
        sys.stdout.flush()
        sys .exit(0)


if __name__ == "__main__":
    main()  
