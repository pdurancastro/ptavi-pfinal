#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

import sys
import socket
import socketserver


#Defino la clase que tratara mi xml
class XMLhandler(ContentHandler):
    
    def __init__(self):
        self.diccionario_xml = {}
    
    #Trato el xml
    def startElement(self, etiqueta, attrs):
        if etiqueta == 'account':
            self.diccionario_xml['username'] = attrs.get('username',"")
            self.diccionario_xml['passwd'] = attrs.get('passwd',"")
            
        if etiqueta == 'uaserver':
            self.diccionario_xml['uaserver_ip'] = attrs.get('ip',"")
            self.diccionario_xml['uaserver_puerto'] = attrs.get('puerto',"")
        
        if etiqueta == 'rtpaudio':
            self.diccionario_xml['rtp_puerto'] = attrs.get('puerto',"")
        
        if etiqueta == 'regproxy':
            self.diccionario_xml['regproxy_ip'] = attrs.get('ip',"")
            self.diccionario_xml['regproxy_puerto'] = attrs.get('puerto',"")
            
        if etiqueta == 'log':
            self.diccionario_xml['log_path'] = attrs.get('path',"")
        
        if etiqueta == 'audio':
            self.diccionario_xml['audio_path'] = attrs.get('path',"")
            
                
    def get_tags(self):
        return self.diccionario_xml
        
class EchoHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        #while 1:
            #print("HOLA")
        client = self.rfile.read().decode('utf-8').split()
        print("CLIENTE ----->")
        print(client)
        

        


if __name__ == "__main__":
    
    xml = sys.argv[1] 
    
    
    
    if len(sys.argv) != 2:
        print("Usage: python uaserver.py config") 
        sys.exit()
    
    #######XML#######
    ###################################################################################
    parser = make_parser()
    cHandler = XMLhandler()    
    parser.setContentHandler(cHandler)   
    try:
        #Me abrira cualquier xml en funcion del argumento que le pase
        parser.parse(open(xml))
        mytags = cHandler.get_tags()    
        #Error en caso de no meter bien los parametros

    except FileNotFoundError:
        sys.exit('Usage: python uaserver.py config')

    print(mytags)
    ###################################################################################
    
    
    
    
    #########SERVIDOR_PROXY############################################################
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    diccionario = mytags
    
    Proxy_IP = diccionario['regproxy_ip']
    Proxy_Puerto = int(diccionario['regproxy_puerto'])
    Log = diccionario['log_path']
    
    my_socket.connect((Proxy_IP, Proxy_Puerto))
    
    IP_Server = diccionario['uaserver_ip']
    print(IP_Server)
    Port_server = int(diccionario['uaserver_puerto'])
    print(Port_server)
    
    
    
    
    serv = socketserver.UDPServer((IP_Server, Port_server), EchoHandler)
    print("Listening...")
    serv.serve_forever()
    ##################################################################################
    
    
    
         
