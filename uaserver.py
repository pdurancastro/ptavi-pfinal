#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

import sys

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


if __name__ == "__main__":
    parser = make_parser()
    cHandler = XMLhandler()
    xml = sys.argv[1] 
    
    
    if len(sys.argv) > 2:
        print("Usage: python uaserver.py config") 
        sys.exit()
        
    parser.setContentHandler(cHandler)   
    try:
        #Me abrira cualquier xml en funcion del argumento que le pase
        parser.parse(open(xml))
        mytags = cHandler.get_tags()    
        #Error en caso de no meter bien los parametros

    except FileNotFoundError:
        sys.exit('Usage: python uaserver.py config')

    print(mytags)
         
