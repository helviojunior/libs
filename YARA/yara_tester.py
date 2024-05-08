#python -m pip install yara-python pyccat

import os, re, sys, getopt, argparse, json, datetime, hashlib
import yara
from ccat.ccat import ColorCat

parser = argparse.ArgumentParser()
parser.add_argument('yara_rule', help='File with yara rule')
parser.add_argument('file', help='File to verify')

args = parser.parse_args()

rules = yara.compile(filepath=args.yara_rule)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode("UTF-8")

    try:
        tst = str(obj)
        try:
            return json.dumps(tst)
        except:
            return tst
    except:
        pass

    raise TypeError("Type %s not serializable" % type(obj))


def mycallback(data):
    cat = ColorCat()

    print(' ')
    cat.print_formatted(data=json.dumps(data, default=json_serial), title=f'Rule: {data["rule"]}', no_tab=True)
    return yara.CALLBACK_CONTINUE
 
with open(args.file, 'rb') as f:
    f_data = f.read()
    sha256_hash = hashlib.sha256(f_data).hexdigest().lower()
    
    print(' ')
    print(f'SHA256 Hash: {sha256_hash}')
    
    matches = rules.match(data=f_data, callback=mycallback, which_callbacks=yara.CALLBACK_MATCHES)
    print(f'Matches found: {len(matches)}')
 
