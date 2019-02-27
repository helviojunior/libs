#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Author : Helvio Junior (M4v3r1cK)
Date : 2019-01-15
https://github.com/helviojunior/libs/blob/master/python/xtext2stack.py
'''

import os, re, sys, getopt, argparse
import sys, struct

parser = argparse.ArgumentParser()
parser.add_argument('text', help='Text to encode')

args = parser.parse_args()


def print_err(text):
    sys.stderr.write(text)
    sys.stderr.flush()

def print_std(data):
    sys.stdout.buffer.write(data)
    sys.stdout.flush()


text=args.text

if text == "-":
    bdata = sys.stdin.buffer.read()
else:
    bdata = str.encode(text)

print_err("Input size: %d\n" % len(bdata))

if (len(bdata) % 4) > 0:
    bdata += str.encode("\0" * (4 - (len(bdata) % 4)))
else:
    bdata += str.encode("\0" * 4)

for k in range(len(bdata) - 1, 0, -4):
    print("PUSH 0x%02x%02x%02x%02x" % (bdata[k],bdata[k-1],bdata[k-2],bdata[k-3]))

#print_std(bdata)
