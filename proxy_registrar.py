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
import hashlib
import os

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
    Dicc_Pass = {}
    
    #def register2json(self):
     #   fich = json.dumps(self.dict)
      #  with open('registered.json', 'w') as fich:
       #     json.dump(self.dicc, fich ,sort_keys=True, indent=4)
            

        
    def json2register(self):
        try:
            with open('registered.json') as client_file:
                self.client_list = json.load(client_file)
        except:
            self.register2json()
    
    def register2json(self):
        fichero_json = open('registered.json', "w")
        json.dump(self.client_list, fichero_json, indent='\t')
    
 
    
    def handle(self):
        
        client = self.rfile.read().decode('utf-8').split()
        print("CLIENTE ----->")
        print(client)    
               
        #self.json2register(fich_json)
        #self.json2passwd(fich_pass)
        #self.register2json(fich_json)
        
        
        #Con esto extraigo los datos de mi fichero passwords.txt
        #print(diccionario_proxy_xml)
        fich_pass = diccionario_proxy_xml['Contraseñas']
        #print(fich_pass)
        passwords = open(fich_pass, 'r')
        passwords_datos = passwords.read()
        #print(passwords_datos)
        
        separo = passwords_datos.split(",")
        #print(separo)
        
        User1_passwd1 = separo[0].split(":")
        User1 = User1_passwd1[0]
        passwd1 = User1_passwd1[1]
        #print("Mi usuario es " + User1)
        #print("Mi contraseña es " + passwd1)
        
        User2_passwd2 = separo[1].split(":")
        User2 = User2_passwd2[0]
        passwd2 = User2_passwd2[1]
        
        #print("Mi usuario es " + User2)
        #print("Mi contraseña es " + passwd2)
        #Quito un \r\n que sobra
        passwd2 = passwd2.split("\n")
        passwd2 = passwd2[0]
             
               
        
                           
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
            
            

            self.Dicc_Pass[User_Name] = "98765434546545646542"
            Converbyts = bytes(str(self.Dicc_Pass[User_Name]), 'utf-8')
            noncebt = Converbyts            
            passwd1 = (bytes(passwd1, 'utf-8'))
            passwd2 = (bytes(passwd2, 'utf-8'))

            
              
            
            #########################################################################################################
            
            
            #Respuesta de cliente no Autorizado

                
                
                

            if len(client) == 8:
                print("Usuario Autorizado")
                #Si el tiempo de expiracion es distinto de 0
                if client[4] != "0":
                    print("Tiempo expiracion valido")
                    if client[7] != " ":
                        #print(client)
                        #print(client[7])
                        #print(client[1])
                        #print(User1)
                        #Necesito comparar mi 1 cliente con la información que me llega
                        cliente_1 = client[1].split(":")
                        cliente_1 = cliente_1[1]                        
                        
                        
                        #USUARIO_1 REGISTER##############################################
                        if cliente_1 == User1:
                            print("ESTAMOS CON EL CLIENTE " + cliente_1)
                            m = hashlib.sha1()
                            m.update(passwd1)
                            m.update(noncebt)
                            new_response = m.hexdigest()
                            response_1 = client[7].split("response=")
                            response_1 = response_1[1]
                            if response_1 == new_response:
                                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                                print("Enviando 200 OK.....")
                        
                        
                        #Necesito comparar mi 2 cliente con la información que me llega
                        cliente_2 = client[1].split(":")
                        cliente_2 = cliente_2[1]
                        print(cliente_2)
                        ###################################################################
                        
                        #USUARIO_2 REGISTER################################################
                        if cliente_2 == User2:
                            print("ESTAMOS CON EL CLIENTE " + cliente_2)
                            m = hashlib.sha1()
                            m.update(passwd2)
                            m.update(noncebt)
                            new_response = m.hexdigest()
                            response_2 = client[7].split("response=")
                            response_2 = response_2[1]
                            if response_2 == new_response:
                                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                                print("Enviando 200 OK.....")
                                
                            
                         
                         
                            
                            
                            
            elif len(client) != 8 and len(client) !=5:
                print("SIP/2.0 400 Bad Request")                
                            
            else:
                print("Usuario no Autorizado")               
                self.wfile.write(b"SIP/2.0 401 Unauthorized\r\n" + b"WWW Authenticate: Digest nonce=" + noncebt + \
                                 b"\r\n\r\n")

                        
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

    
    
    
    
    
    
    
