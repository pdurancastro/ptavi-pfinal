#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

from uaserver.py import XMLhandler

import sys

if __name__ == "__main__":

    try:
        xml = sys.argv[1]
        Metodo = sys.argv[2]
        Opcion = sys.argv[3] 
