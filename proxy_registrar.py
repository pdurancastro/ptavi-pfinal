#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

import sys
import socket
import socketserver
import time
import random
import json

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
    NoAuthDicc = {}
    
    def register2json(self):
        fich = json.dumps(self.dict)
        with open('registered.json', 'w') as fich:
            json.dump(self.dicc, fich ,sort_keys=True, indent=4)

    
    def handle(self):
        
        client = self.rfile.read().decode('utf-8').split()
        print("CLIENTE ----->")
        print(client)                       
        if client[0] == "REGISTER":
            print("Compruebo que mi procedimiento es " + client[0])
            #Con esto chopeo mediante los : y me quedo con el elemento que quiero de ello
            User_Name = client[1].split(':')[1]
            User_Port = client[1].split(':')[2]
            User_IP = self.client_address[0]
            Expires = time.time() + int(client[4])
            #Con esto tengo todos los datos de mi cliente nuevo       
            #print(User_Name)
            #print(User_Port)
            #print(User_IP)
            #print(client[4])
            #print(Expires)
            
            
            ########################################################################################################
            #Genero numero random
            self.NoAuthDicc[User_Name] = random.getrandbits(100)
            Converbyts = bytes(str(self.NoAuthDicc[User_Name]), 'utf-8')
            
            
            
            #fich_passwd = diccionario_proxy_xml['passwdpath']
            
            
            
            
            #noncebt = Converbyts
            passwdbt = diccionario_proxy_xml['Contraseñas']
            print(passwdbt)
            
            print(diccionario_proxy_xml)
            #print("Esta es la contraseña" + passwdbt)
            #m = hashlib.md5()
            #m.update(passwdbt + noncebt)
            #response = m.hexdigest()
            #########################################################################################################
            
            
            #Respuesta de cliente no Autorizado
            if len(client) == 5:
                print("Usuario no Autorizado")               
                self.wfile.write(b"SIP/2.0 401 Unauthorized\r\n" + b"WWW Authenticate: Digest nonce=" + Converbyts + \
                                 b"\r\n\r\n")

            if len(client) == 8:
                print("Usuario Autorizado")
                print(client[4])
                
                if client[4] != "0":
                    print("Tiempo expiracion valido")
                    if client[7] != " ":
                        print(client[7])
                        response = client[7].split("response=")
                        response = response[1]
                        print(response)
                        #print(response_1)
                        
                        #if response == response_1:
                            #print("Vamos bien")
                        
                        
                        #self.registered2json()
                        
                       
                
                                 
           
                
                

            
        if client[0] == "INVITE":
            print(client[0])
        
        if client[0] == "BYE":
            print(client[0])
            
                
            
            
            
            
            
            
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
    
    MyServer = "Server MiServidorProxy listening at port"
    print(MyServer + " " + str(puerto_proxy) + "...")
    
    proxy_serv.serve_forever()

    
    
    
    
    
    
    
