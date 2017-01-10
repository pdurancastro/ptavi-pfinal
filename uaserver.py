#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

import sys
import socket
import socketserver
import os
import time


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
                        
        
        #LOG############################
        Log = diccionario['audio_path']
        
        fichero_log = Log
        fichero = open(fichero_log, 'a')
        hora = time.strftime('%Y%m%d%H%M%S', time.gmtime(time.time()))
        
        
        if client[0] == "INVITE":
            print("INVITE RECIBIDO")
            
            #LOG
            informacion = hora + " Recived from" + " " + client[6] + " " + "SIP/2.0 INVITE" + "\r\n"
            fichero.write(informacion)
            
            respuesta = "SIP/2.0 100 TRYING\r\n\r\n"
            respuesta += "SIP/2.0 180 RINGING\r\n\r\n"
            respuesta += "SIP/2.0 200 OK\r\n\r\n"
            cabecera_sdp = "Content-Type: application/sdp\r\n\r\n"
            sdp = 'v=0\r\n' + 'o=' + Nombre_usuario + " " + IP_Server + "\r\n"
            sdp += 's=misesion\r\n' + 't=0\r\n' + "m=audio " + Puerto_RTP + " RTP\r\n\r\n"
            print(respuesta + sdp)
            paquete = respuesta + cabecera_sdp + sdp
            
            self.wfile.write(bytes(paquete, 'utf-8'))
            
            #LOG
            informacion = hora + " Sent to " + " " + client[6] + " " + "SIP/2.0 INVITE" + "\r\n"
            fichero.write(informacion)
        
        if client[0] == "ACK":
            print("ACK RECIBIDO")
            
            #LOG
            informacion = hora + " Received from" + " " + str(Proxy_IP) + str(Puerto_RTP) + "SIP/2.0 ACK" + "\r\n"
            fichero.write(informacion)
            
            
            aEjecutar= './mp32rtp -i ' + IP_Client + ' -p ' + str(Puerto_RTP) 
            aEjecutar+= ' < ' + audio_path
            print ("Vamos a ejecutar", aEjecutar)
            os.system(aEjecutar)
            print("Ejecutado")
            
        if client[0] == "BYE":
            print("BYE RECIBIDO")
            respuesta = "SIP/2.0 200 OK\r\n\r\n"
            self.wfile.write(bytes(respuesta, 'utf-8'))   
            
            #LOG
            informacion = hora + " Received " + "BYE" + " " + respuesta
            fichero.write(informacion)     
                
        


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
    
    audio_path = diccionario['audio_path']
    Nombre_usuario = diccionario['username']
    Puerto_RTP = diccionario['rtp_puerto']
    
    Proxy_IP = diccionario['regproxy_ip']
    Proxy_Puerto = int(diccionario['regproxy_puerto'])
    Log = diccionario['log_path']
    
    my_socket.connect((Proxy_IP, Proxy_Puerto))
    
    IP_Server = diccionario['uaserver_ip']
    IP_Client = IP_Server
    Port_server = int(diccionario['uaserver_puerto'])
    
    
    
    
    serv = socketserver.UDPServer((IP_Server, Port_server), EchoHandler)
    print("Listening...")
    serv.serve_forever()
    ##################################################################################
    
    
    
         
