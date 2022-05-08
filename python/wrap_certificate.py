#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Author : Helvio Junior (M4v3r1cK)
Date : 2012-05-07

This code will wrap the certificates from an HTTPs server and generate sha256 used to Android certificate pinning

Inspiration: 
    https://stackoverflow.com/questions/19145097/getting-certificate-chain-with-python-3-3-ssl-module#58246407

Modules: 
    pip3 install pyopenssl certifi

Tags: 
    OpenSSL, Certificate pinning, sha256, wrap certificate, calculate hash pinning, calculate sha265 pinning
'''

import os, re, sys, getopt, random
import sys, struct
import base64, string
import socket
import hashlib
from collections import defaultdict
from OpenSSL import SSL
from OpenSSL.crypto import dump_certificate, dump_publickey, FILETYPE_ASN1, FILETYPE_PEM
from urllib.parse import urlparse
import certifi


######### Variables
#
url_api1 = "https://helviojunior.com.br"

######### Variables
#
# No changes is needed here 

ca_b64data=None
pin_domain=None
pin_hash=None

#v=$(openssl s_client -showcerts -connect server_ip:443 </dev/null | openssl x509 -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | openssl enc -base64); echo -e "\n\nsha256/$v\n"
def wrap_certificates():
    global ca_b64data, pin_domain, pin_hash
    print(f"Connecting to {url_api1} ...")
    uri = urlparse(url_api1)
    ca_cert = None
    server_cert = None

    context = SSL.Context(method=SSL.TLSv1_2_METHOD)
    context.load_verify_locations(cafile=certifi.where())

    conn = SSL.Connection(context, socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    conn.settimeout(5)
    conn.connect((uri.hostname, uri.port if uri.port != 0 and uri.port is not None else 443))
    conn.setblocking(1)
    conn.do_handshake()
    conn.set_tlsext_host_name(uri.hostname.encode())
    print(f"Certificate chain:")
    for (idx, cert) in enumerate(conn.get_peer_cert_chain()):
        print(f'{idx} subject: {cert.get_subject()}')
        print(f'  issuer: {cert.get_issuer()})')
        print(f'  fingerprint: {cert.digest("sha1")}')


        if cert.get_subject().commonName == cert.get_issuer().commonName:
            ca_cert = cert

        san = get_certificate_san(cert)
        if cert.get_subject().commonName.lower().replace('*.', '') in uri.hostname.lower() or uri.hostname.lower() in san:
            server_cert = cert

    conn.close()

    # Carrega o certificado da CA
    if ca_cert is not None:
        der = dump_certificate(FILETYPE_ASN1, ca_cert)
        if isinstance(der, str):
            der = der.encode("utf-8")

        ca_b64data = base64.b64encode(der)
        if isinstance(ca_b64data, bytes):
            ca_b64data = ca_b64data.decode("utf-8")
    else:
        ca_b64data = "Not found!"


    if server_cert is not None:
        pin_domain = server_cert.get_subject().commonName.lower()

        der = dump_publickey(FILETYPE_ASN1, server_cert.get_pubkey())
        if isinstance(der, str):
            der = der.encode("utf-8")

        sha256 = hashlib.sha256(der).digest()
        pin_hash = 'sha256/'+ base64.b64encode(sha256).decode("utf-8")
    else:
        pin_domain = "Not found!"

def get_certificate_san(x509cert):
    san = ''
    ext_count = x509cert.get_extension_count()
    for i in range(0, ext_count):
        ext = x509cert.get_extension(i)
        if 'subjectAltName' in str(ext.get_short_name()):
            san = ext.__str__()
    return san.lower()

def main():
    wrap_certificates()

    print()

    print(f'CA Base64 cert..: {ca_b64data}')
    print(f'Pinned domain...: {pin_domain}')
    print(f'Pinned hash  ...: {pin_hash}')
    


if __name__ == "__main__":
    main()
