#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

from uaserver import XMLhandler

import sys
import uaserver

if __name__ == "__main__":

    xml = sys.argv[1]
    Metodo = sys.argv[2]
    Opcion = sys.argv[3]
    
    
    if len(sys.argv) > 4:
        print("Usage: python uaclient.py config method option") 
        sys.exit()
    
    #######XML#######
    ###################################################################################            
    parser = make_parser()
    Xml_Handler = uaserver.XMLhandler()
    parser.setContentHandler(Xml_Handler)
    
    try:
        parser.parse(open(xml))
        mytags = Xml_Handler.get_tags()
    except FileNotFoundError: 
       print("Usage: python uaclient.py config method option")
       sys.exit()
    print(mytags)
    ###################################################################################
