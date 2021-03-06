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
import os


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: python uaclient.py config method option")
        sys.exit()

    xml = sys.argv[1]
    Metodo = sys.argv[2]
    Opcion = sys.argv[3]

#   ######XML#######
#   ##################################################################################
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
#   ##################################################################################

#   #########SERVIDOR_PROXY############################################################
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    diccionario = mytags
    Proxy_IP = diccionario['regproxy_ip']
    Proxy_Puerto = int(diccionario['regproxy_puerto'])
    Log = diccionario['log_path']
    audio_path = diccionario['audio_path']

    my_socket.connect((Proxy_IP, Proxy_Puerto))
#   ##################################################################################

#   #LOG############################
    fichero_log = Log
    fichero = open(fichero_log, 'a')
    hora = time.strftime('%Y%m%d%H%M%S', time.gmtime(time.time()))


#   #########MANDAR_PETICION####################################################
    username = diccionario['username']
    if Metodo == 'REGISTER':
#       #LOG
        informacion = hora + " Starting... \r\n"
        fichero.write(informacion)

        puerto_server = diccionario['uaserver_puerto']
        Peticion = Metodo + " " + 'sip:' + username \
            + ":" + puerto_server + ' SIP/2.0\r\n'
        Cabecera = "Expires: " + str(Opcion) + '\r\n\r\n'
        MENSAJE = Peticion + Cabecera
        print("Enviando----->")
        print(MENSAJE)
        my_socket.send(bytes(MENSAJE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        data_1 = data.decode('utf-8')
        print(data_1)
        data_1 = data_1.split(' ')

#       #LOG
        informacion = hora + " Sent to " + str(Proxy_IP) \
            + ":" + str(Proxy_Puerto) + " " \
            + MENSAJE.replace("\r\n", " ") + "\r\n"
        fichero.write(informacion)

        if data_1[1] == "401":
            print("Entra en el reenvio del register")
#           #Cojo el codigo que me entrego el proxy
            nonce = data_1[5].split("\r\n")
            nonce = nonce[0]
            passwd = diccionario['passwd']
            nonce = nonce.split("nonce=")
            nonce = nonce[1]

            passwd = diccionario['passwd']
            passwdbt = (bytes(passwd, 'utf-8'))
            noncebt = (bytes(nonce, 'utf-8'))
#           #Cifrado de la contraseña y codigo
            print(passwdbt)
            print(noncebt)
            m = hashlib.sha1()
            m.update(passwdbt)
            m.update(noncebt)
            response = m.hexdigest()
            print("Mandando el REGISTER con clave " + response + "\r\n")
            Cabecera_noesp = "Expires: " + str(Opcion) + "\r\n"
            MENSAJE = Peticion + Cabecera_noesp
            MENSAJE = MENSAJE + "Authorization: Digest response=" \
                + response + "\r\n"
            print(MENSAJE)
            my_socket.send(bytes(MENSAJE, 'utf-8') + b'\r\n')

#           #LOG
            informacion = hora + " Received from " + str(Proxy_IP) \
                + ":" + str(Proxy_Puerto) + "\r\n"
            fichero.write(informacion)

        if data_1[1] == "404":
            print("SIP/2.0 404 User Not Found")

#           #LOG
            informacion = hora + " SIP/2.0 404 User Not Found"
            fichero.write(informacion)

        if data_1[1] == "405":
            print("SIP/2.0 405 Method Not Allowed")

#           #LOG
            informacion = hora + " SIP/2.0 405 Method Not Allowed"
            fichero.write(informacion)

    elif Metodo == 'INVITE':
        ip_servidor = diccionario['uaserver_ip']
        puerto_rtp = diccionario['rtp_puerto']
        Peticion = Metodo + " " + 'sip:' + Opcion + ' SIP/2.0\r\n'
        Cabecera = 'Content-Type: application/sdp\r\n\r\n'
        Paq_sdp = 'v=0 ' + 'o=' + username + ' ' + ip_servidor \
            + '\r\n' + 's=misesion\r\n' + 't=0' + '\r\n' \
            + 'm=audio ' + str(puerto_rtp) + ' RTP' + '\r\n'
        MENSAJE = Peticion + Cabecera + Paq_sdp
        print("Enviando INVITE----->")
        print(MENSAJE)
        my_socket.send(bytes(MENSAJE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        recepcion = data.decode('utf-8')
        print(recepcion)
        my_reception = recepcion.split("\r\n")
        print(my_reception)

#       LOG
        informacion = hora + " Sent to" + str(Proxy_IP) + ":" \
            + str(Proxy_Puerto) + ": " + MENSAJE.replace("\r\n", " ") + "\r\n"
        fichero.write(informacion)

        if my_reception[0] == "SIP/2.0 100 TRYING" \
            and my_reception[2] == "SIP/2.0 180 RINGING" \
                and my_reception[4] == "SIP/2.0 200 OK":
            respuesta = 'ACK sip:' + Opcion + ' SIP/2.0'
            print("Enviando ACK----->")
            my_socket.send(bytes(respuesta, 'utf-8'))

            aEjecutar = './mp32rtp -i  127.0.0.1 -p ' + str(puerto_rtp)
            aEjecutar += ' < ' + audio_path
            print("Vamos a ejecutar", aEjecutar)
            os.system(aEjecutar)
            print("Ejecutado")

#           LOG
            informacion = hora + " " + "Sent to" + str(Proxy_IP) + ":" \
                + str(Proxy_Puerto) + " " + respuesta.replace("\r\n", " ") \
                + "RTP" "\r\n"
            fichero.write(informacion)

    elif Metodo == 'BYE':
        Peticion = Metodo + " " + 'sip:' + Opcion + ' SIP/2.0\r\n'
        MENSAJE = Peticion
        print("Enviando BYE----->")
        print(MENSAJE)
        print("Para finalizar la conexion terminala con ua1")
        my_socket.send(bytes(MENSAJE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        recepcion = data.decode('utf-8')
        print(recepcion)
        my_reception = recepcion.split("\r\n")
        print(my_reception)

#       LOG
        informacion = hora + " " + "Sent to" + str(Proxy_IP) + ":"  \
            + str(Proxy_Puerto) + " " + MENSAJE.replace("\r\n", " ") + "\r\n"
        fichero.write(informacion)

        if my_reception[0] == "SIP/2.0 200 OK":
            print("Recibo el SIP/2.0 200 OK ")

#           LOG
            informacion = hora + " Received from" + str(Proxy_IP) + ":" \
                + str(Proxy_Puerto) + " " + "Recibo el SIP/2.0 200 OK \r\n"
