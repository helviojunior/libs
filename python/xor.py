#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Author : Helvio Junior (M4v3r1cK)
Date : 2019-01-15
Updated: 2021-09-17
https://github.com/helviojunior/libs/blob/master/python/xor.py
'''

import os, re, sys, getopt, argparse
import sys, struct

parser = argparse.ArgumentParser()
parser.add_argument('-text', help='Text to encode with xor')
parser.add_argument('-key', help='xor key')
parser.add_argument('-f', '--format', default='raw', help='Format to output (raw, c, csharp, python)')
parser.add_argument('-v', '--variable', default='buffer', help='Buffer variable Name')

args = parser.parse_args()

def print_err(text):
    sys.stderr.write(text)
    sys.stderr.flush()

def print_std(data):
    sys.stdout.buffer.write(data)
    sys.stdout.flush()

def print_output(data):

    fmt = args.format
    if fmt != "raw":
        var_name = args.variable

        if fmt == "c":
            txtdata = "unsigned char %s[] =" % var_name
            txtdata += "\n\""
            for idx, val in enumerate(data):

                if idx != 0 and idx % 16 == 0:
                    txtdata += "\"\n\""

                txtdata += "\\x{0:02x}".format(val)

            txtdata += "\";\n"
            print(txtdata)

        elif fmt == "csharp":
            txtdata = "byte[] %s = new byte[%d] {" % (var_name, len(data))
            for idx, val in enumerate(data):

                if idx % 16 == 0:
                    txtdata += "\n"

                txtdata += "0x{0:02x},".format(val)

            txtdata = txtdata.strip(",")
            txtdata += " };\n"
            print(txtdata)

        elif fmt == "python":
            txtdata = "%s =  b\"\"\n" % var_name
            for idx, val in enumerate(data):

                if idx % 16 == 0:
                    txtdata += "%s += b\"" % var_name

                txtdata += "\\x{0:02x}".format(val)

            txtdata = txtdata.strip(",")
            txtdata += "\"\n"
            print(txtdata)

    else: # raw
        print_std(data)


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

print_output(odata)
