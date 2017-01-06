#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

from uaserver import XMLhandler

import sys
import uaserver
import socket
import time
import hashlib

if __name__ == "__main__":

            
    if len(sys.argv) != 4:
        print("Usage: python uaclient.py config method option") 
        sys.exit()
        
        
    xml = sys.argv[1]
    Metodo = sys.argv[2]
    Opcion = sys.argv[3]    
    
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
    Log = diccionario['log_path']


    #print(Proxy_IP)
    #print(Proxy_Puerto)

    my_socket.connect((Proxy_IP, Proxy_Puerto))   
    ##################################################################################
    
    #########MANDAR_PETICION####################################################
    username = diccionario['username']
    if Metodo == 'REGISTER':        
        puerto_server = diccionario['uaserver_puerto']            
        Peticion = Metodo + " " + 'sip:' + username + ":" + puerto_server +' SIP/2.0\r\n'
        Cabecera = "Expires: " + str(Opcion) + '\r\n\r\n'
        MENSAJE = Peticion + Cabecera
        print("Enviando----->")
        print(MENSAJE)
        my_socket.send(bytes(MENSAJE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        data_1 = data.decode('utf-8')
        print(data_1)
        data_1 = data_1.split(' ')
        
        if data_1[1] == "401":
            print("Entra en el reenvio del register")
            #Cojo el codigo que me entrego el proxy
            nonce = data_1[5].split("nonce=")
            nonce = nonce[1]
            #print(nonce)
            passwd = diccionario['passwd']
            #print(passwd)
            passwdbt = (bytes(passwd, 'utf-8'))
            noncebt = (bytes(nonce, 'utf-8'))
            #Cifrado de la contraseña y codigo
            m = hashlib.md5()
            m.update(passwdbt + noncebt)
            response = m.hexdigest()
            print("Mandando el REGISTER con clave " + response + " ------>" + "\r\n" )
            Cabecera_noesp = "Expires: " + str(Opcion) + "\r\n"
            MENSAJE = Peticion + Cabecera_noesp            
            MENSAJE = MENSAJE + "Authorization: Digest response=" + response + "\r\n"
            print(MENSAJE)
            my_socket.send(bytes(MENSAJE, 'utf-8') + b'\r\n')
        
    
    elif Metodo == 'INVITE':
        ip_servidor = diccionario['uaserver_ip']
        puerto_rtp=diccionario['rtp_puerto']
        Peticion = Metodo + " " + 'sip:' + Opcion + ' SIP/2.0\r\n'
        Cabecera = 'Content-Type: application/sdp\r\n\r\n'
        Paq_sdp = 'v=0 ' + 'o=' + username + ' ' + ip_servidor + '\r\n' + 's=misesion\r\n' + 't=0' + '\r\n' + 'm = audio ' + str(puerto_rtp) + ' RTP'
        MENSAJE = Peticion + Cabecera + Paq_sdp
        print("Enviando----->")
        print(MENSAJE)
        my_socket.send(bytes(MENSAJE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print(data.decode('utf-8'))
         
    
    elif Metodo == 'BYE':
        Peticion = Metodo + " " + 'sip:' + Opcion + ' SIP/2.0\r\n'
        MENSAJE = Peticion
        print("Enviando----->")
        print(MENSAJE)
        my_socket.send(bytes(MENSAJE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print(data.decode('utf-8'))
    
    #else:
    

    
    
    
    
    
    
    
    
