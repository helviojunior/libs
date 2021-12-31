#!/bin/bash

cd /tmp
apt install python3-distutils
curl -s https://bootstrap.pypa.io/get-pip.py | python3.8 -
git clone https://github.com/SecureAuthCorp/impacket.git
cd /tmp/impacket
python3.8 -m pip install .
