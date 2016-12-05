#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

import sys
import socket
import socketserver

class XML_Prox_Handler(ContentHandler):
    def __init__(self):
        self.diccionario_proxy_xml = {}
    
    #Trato el xml###########################################################
    def startElement(self, etiqueta, attrs):
        if etiqueta == 'server':
            self.diccionario_proxy_xml['Mi_Servidor_Proxy'] = attrs.get('name',"")
            self.diccionario_proxy_xml['IP_Proxy_Registrar'] = attrs.get('ip',"")
            self.diccionario_proxy_xml['Puerto_Proxy'] = attrs.get('puerto',"")
        
        if etiqueta == 'database':
            self.diccionario_proxy_xml['Usuarios'] = attrs.get('path',"")
            self.diccionario_proxy_xml['Contraseñas'] = attrs.get('passwdpath',"")
            
        if etiqueta == 'log':
            self.diccionario_proxy_xml['Log_Proxy'] = attrs.get('path',"")
            
    def get_tags(self):
        return self.diccionario_proxy_xml
    #########################################################################   
        
###TRATO_LAS_PETICIONES_CLIENTE#############################################################        
class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dict = {}    
    list_client = []
    
    def handle(self):
        client = self.rfile.read().decode('utf-8').split()
        print("CLIENTE ----->")
        print(client)                       
        if client[0] == "REGISTER":
            print(client[0])
            
        if client[0] == "INVITE":
            print(client[1])    
            
            
            
            
            
#############################################################################
if __name__ == "__main__":

    xml_proxy = sys.argv[1]
    
    if len(sys.argv) > 2:
        print("Usage: python proxy_registrar.py config") 
        sys.exit()
    
    #######XML#######
    ###################################################################################
    parser = make_parser()
    cHandler_Proxy = XML_Prox_Handler()
    parser.setContentHandler(cHandler_Proxy)
    try:
        parser.parse(open(xml_proxy))
        mytags = cHandler_Proxy.get_tags()
    except FileNotFoundError:
        sys.exit('Usage: python proxy_registrar.py config')    

    #print(mytags)      
    ###################################################################################   
    
    ####RECEPCION_MSJ_CLIENTE##########################################################
    diccionario_proxy_xml = mytags
    puerto_proxy = int(diccionario_proxy_xml['Puerto_Proxy'])    
    proxy_serv = socketserver.UDPServer(('', puerto_proxy), SIPRegisterHandler)
    proxy_serv.serve_forever()

    
    
    
    
    
    
    
