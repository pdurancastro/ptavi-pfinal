#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

from uaserver import XMLhandler

import sys
import uaserver
import socket

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
    
    
    #########SERVIDOR_PROXY############################################################
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    diccionario = mytags
    Proxy_IP = diccionario['regproxy_ip']
    Proxy_Puerto = int(diccionario['regproxy_puerto'])

    print(Proxy_IP)
    print(Proxy_Puerto)

    my_socket.connect((Proxy_IP, Proxy_Puerto))   
    ##################################################################################
