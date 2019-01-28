#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Author : Helvio Junior (M4v3r1cK)
Date : 2019-01-15
https://github.com/helviojunior/libs/blob/master/python/xor.py
'''

import os, re, sys, getopt, argparse
import sys, struct

parser = argparse.ArgumentParser()
parser.add_argument('text', help='Text to encode with xor')
parser.add_argument('key', help='xor key')

args = parser.parse_args()


def print_err(text):
    sys.stderr.write(text)
    sys.stderr.flush()

def print_std(data):
    sys.stdout.buffer.write(data)
    sys.stdout.flush()


ikey = int(args.key, 0)
if ikey < 0:
    ikey = 0

if ikey > 255:
    ikey = 255

key = (ikey).to_bytes(1, byteorder='big')[0]

text=args.text

if text == "-":
    bdata = sys.stdin.buffer.read()
else:
    bdata = str.encode(text)

print_err("Encoding data with key 0x%02x\n" % key)
print_err("Input size: %d\n" % len(bdata))

odata = bytearray()

for i in bdata:
    odata.append( i ^ key )

print_std(odata)
