#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Author : Helvio Junior (M4v3r1cK)
Date : 2019-01-15
https://github.com/helviojunior/libs/blob/master/python/xor.py
'''

import os, re, sys, getopt, argparse
import sys

def print_err(text):
    sys.stderr.write(text)
    sys.stderr.flush()


parser = argparse.ArgumentParser()
parser.add_argument('text', help='Text to encode with xor')
parser.add_argument('key', help='xor key')

args = parser.parse_args()

key = int(args.key, 0)
if key < 0:
    key = 0

if key > 255:
    key = 255

text=args.text

if text == "-":
    #text = input()
    text = sys.stdin.buffer.read()

print_err("Encoding data with key 0x%02x\n" % key)
print_err("Input size: %d\n" % len(text))

text2 = ""

for i in range(len(text)):
    if isinstance(text[i], int):
        text2 += chr(text[i] ^ key)
    else:
        text2 += chr(ord(text[i]) ^ key)

print(text2, end='', flush=True)
