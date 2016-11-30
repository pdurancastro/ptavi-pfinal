#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

#Defino la clase que tratara mi xml
class XMLhandler(ContentHandler):
    
    def __init__(self):
